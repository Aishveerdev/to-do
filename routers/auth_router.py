from fastapi import APIRouter, HTTPException , status ,Depends   
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from services.database import get_db
from utils.jwt_management import create_access_token, verify_access_token
from utils.pw_hashing import hash_password, verify_password
from schemas.auth_schema import SignUpRequest, LoginRequest
from models.user_model import User
from sqlalchemy import select



router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup")
async def SignUp_user (request: SignUpRequest, db: AsyncSession = Depends(get_db)):
    
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == request.email))
    existing_user = result.scalar_one_or_none() # either return user or None
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(request.password) # hashing the password before storing it in database
    # Create new user
    new_user = User(
        username=request.username,
        email=request.email,
        hashed_password = hashed_password # hashing the password before storing it in database
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message": "User created successfully"}

@router.post("/login")
async def Login_user(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    try:
            
        # Check if user exists
        result = await db.execute(select(User).where(User.email == request.email))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=401, detail="No user found")
    
        # Verify password
        if not verify_password(request.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid password")
    
        # Create JWT token
        token_data = {"sub": str(user.id) , "email": user.email}
        token = create_access_token(token_data)

        #return token with json response
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Login successful",
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "access_token": token
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during login: {str(e)}"
        )
     