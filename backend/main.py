from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt
import pyotp
import qrcode
from io import BytesIO
import base64
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base = declarative_base()

def get_engine():
    for i in range(5):
        try:
            engine = create_engine("postgresql://user:pass@db:5432/app")
            conn = engine.connect()
            conn.close()
            print("✓ Database connected")
            return engine
        except Exception as e:
            print(f"DB retry {i+1}/5: {e}")
            time.sleep(2)
    raise Exception("Failed to connect to database")

engine = get_engine()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    secret = Column(String, nullable=False)
    enabled = Column(Boolean, default=False)

Base.metadata.create_all(engine)

# Helper functions using bcrypt directly
def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)

@app.get("/")
def root():
    return {"status": "ok", "message": "2FA API is running"}

@app.post("/register")
def register(username: str, password: str):
    db = Session()
    try:
        if not username or len(username) < 3:
            raise HTTPException(status_code=400, detail="Username must be at least 3 characters")
        
        existing = db.query(User).filter(User.username == username).first()
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")
        
        hashed_password = hash_password(password)
        secret = pyotp.random_base32()
        
        user = User(username=username, password=hashed_password, secret=secret)
        db.add(user)
        db.commit()
        db.refresh(user)
        
        print(f"✓ User registered: {username} (ID: {user.id})")
        return {"id": user.id, "username": username}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"✗ Registration error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.post("/login")
def login(username: str, password: str):
    db = Session()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        print(f"✓ User logged in: {username}")
        return {"user_id": user.id, "requires_2fa": user.enabled}
    finally:
        db.close()

@app.post("/2fa/enable")
def enable_2fa(user_id: int):
    db = Session()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        totp = pyotp.TOTP(user.secret)
        uri = totp.provisioning_uri(name=user.username, issuer_name="MyApp")
        
        qr = qrcode.make(uri)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        qr_base64 = base64.b64encode(buf.getvalue()).decode()
        
        print(f"✓ 2FA QR generated for: {user.username}")
        return {
            "qr_code": f"data:image/png;base64,{qr_base64}",
            "secret": user.secret
        }
    finally:
        db.close()

@app.post("/2fa/verify")
def verify_2fa(user_id: int, code: str):
    db = Session()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        totp = pyotp.TOTP(user.secret)
        if totp.verify(code):
            user.enabled = True
            db.commit()
            print(f"✓ 2FA enabled for: {user.username}")
            return {"ok": True, "message": "2FA enabled successfully"}
        else:
            raise HTTPException(status_code=401, detail="Invalid 2FA code")
    finally:
        db.close()

print("🚀 FastAPI application started")
