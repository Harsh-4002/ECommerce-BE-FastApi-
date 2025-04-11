from fastapi import APIRouter,status ,Depends,HTTPException
from schemas import Login,TokenData
from sqlalchemy.orm import Session
from database import get_dB
from passlib.context import CryptContext
import models
from datetime import datetime,timedelta
from jose import jwt,JWTError
from fastapi.security.oauth2 import OAuth2PasswordBearer,OAuth2PasswordRequestForm

router=APIRouter(tags=['Login'])

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2scheme=OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY="84cfa49faef9368b07064e283f2bcd9830952f5bb38ef64aa2fc4610bf14b9bd"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=20



def generate_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

@router.post('/login')
def login(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_dB)):
    seller=db.query(models.Seller).filter(
        models.Seller.username==request.username
    ).first()

    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found/invalid user")
    
    if pwd_context.verify(request.password,seller.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password")
    access_token=generate_token(data={"sub":seller.username})
    return {"access_token":access_token,"token_type":"bearer"}


def get_current_user(token:str=Depends(oauth2scheme)):
    credentialsException=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid auth credentials",
        headers={'WWW-Authenticate':"Bearer"},
    )
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload.get("sub")
        if username is None:
            raise credentialsException
        token_data=TokenData(username=username)
    except JWTError:
        raise credentialsException

