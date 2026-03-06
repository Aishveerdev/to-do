# FINAL TOKEN: header.payload.signature
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi import HTTPException , Depends , status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user_model import User
from services.database import get_db

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")      
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/auth/login")


if not JWT_SECRET_KEY or not ALGORITHM or not ACCESS_TOKEN_EXPIRE_MINUTES:
    raise ValueError("Missing JWT configuration in environment variables.")



def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return token

#############################################################

def verify_access_token(token: str):
    try:
        print("TOKEN RECEIVED:", token)
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception as e:
        print("JWT ERROR:", e)
        raise HTTPException(status_code=401, detail="Invalid token")


# ETHE TOKEN AYA TE TOKEN VICHO USER.ID KADD KE DB CH OHO USER LBBEYA , TE PORA USER WAPIS BHEJ TA.
# REMEMBER EHE SARA BAHRO BAHRI HO REHA , HUN JO USER RETUNR KITA , SARE CRUD OPERATIONS US TE HI HONGE.

async def get_current_user(token = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    payload = verify_access_token(token)
    #getting user_id form payload
    user_id = int(payload.get("sub"))
    print(f"✅ Authentication completed for user_id={user_id}")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token(no user_id found)")
    try:
        user_id = int(user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    #getting user from database

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user