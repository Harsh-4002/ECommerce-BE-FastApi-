from fastapi import APIRouter,status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from database import get_dB
from schemas import Seller,DisplaySeller
import models
from passlib.context import CryptContext



router=APIRouter(tags=['Sellers'],prefix='/seller')
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")


# creating seller
@router.post('/',status_code=status.HTTP_201_CREATED,response_model=DisplaySeller)
def  create_seller(request:Seller, db:Session=Depends(get_dB)):
   hashedPassword=pwd_context.hash(request.password)
   new_seller=models.Seller(username=request.username,email=request.email,password=hashedPassword)
   db.add(new_seller)
   db.commit()
   db.refresh(new_seller)
   return new_seller
