from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session as DBSession
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
import bcrypt
import pyotp
import qrcode
from io import BytesIO
import base64
import time

# JWT Configuration
SECRET_KEY = "your-secret-key-change-this-in-production-09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

Base = declarative_base()

# Pydantic Models
class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str
    requires_2fa: bool

class UserResponse(BaseModel):
    id: int
    username: str
    enabled: bool

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
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    secret = Column(String, nullable=False)
    enabled = Column(Boolean, default=False)

Base.metadata.create_all(engine)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper functions
def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: DBSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

@app.get("/")
def root():
    return {"status": "ok", "message": "2FA API is running"}

@app.post("/register")
def register(username: str, password: str, db: DBSession = Depends(get_db)):
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

@app.post("/login", response_model=Token)
def login(username: str, password: str, db: DBSession = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    print(f"✓ User logged in: {username}")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
        "requires_2fa": user.enabled
    }

@app.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "enabled": current_user.enabled
    }

@app.post("/2fa/enable")
def enable_2fa(user_id: int, db: DBSession = Depends(get_db)):
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

@app.post("/2fa/verify")
def verify_2fa(user_id: int, code: str, db: DBSession = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    totp = pyotp.TOTP(user.secret)
    if totp.verify(code):
        user.enabled = True
        db.commit()
        
        # Return JWT token after 2FA verification
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        print(f"✓ 2FA enabled for: {user.username}")
        return {
            "ok": True,
            "message": "2FA enabled successfully",
            "access_token": access_token,
            "token_type": "bearer"
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid 2FA code")

print("🚀 FastAPI application started")
