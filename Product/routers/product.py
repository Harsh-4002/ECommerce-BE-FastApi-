from fastapi import APIRouter,status,HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from database import get_dB
import models
from typing import List
from schemas import Product,DisplayProduct,Seller
from routers.login import get_current_user




router=APIRouter(
    tags=['Products'],
    prefix="/product"

)



# sending database instance to add data to db   for connection with db using session and depends
# add product
@router.post('/',status_code=status.HTTP_201_CREATED)
def addProducts(request:Product, db:Session=Depends(get_dB)):
    new_product=models.Product(name=request.name, description=request.description,price=request.price,seller_id=1)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# update product by id
@router.put('/{id}',)
def updateProduct(id:int,request:Product, db:Session=Depends(get_dB)):
    product=db.query(models.Product).filter(models.Product.id==id)
    if not product.first():
        pass
    product.update(request.dict())
    db.commit()
    return {'Product successfully updated'}
    
# get all product
@router.get('/',response_model=List[DisplayProduct])
def products(db:Session=Depends(get_dB),current_user:Seller=Depends(get_current_user)):
    products=db.query(models.Product).all()
    return products 

# get product by id
@router.get('/{id}',response_model=DisplayProduct)
def productById(id:int,db:Session=Depends(get_dB)):
    product=db.query(models.Product).filter(models.Product.id==id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Product not found')
    return product

# delete product
@router.delete('/{id}',)
def deleteProduct(id:int,db:Session=Depends(get_dB)):
    db.query(models.Product).filter(models.Product.id==id).delete(synchronize_session=False)
    db.commit()
    return "product removed succefully"

