from fastapi import FastAPI
from routers import product,sellers,login
import models
from database import engine,Base


app=FastAPI(
    title="Products Api",
    description="Get details of alll products on our website",
    terms_of_service="http://www.google.com",
    contact={
        "Developer Name":"Website",
        "website":"http://www.google.com",
        "email":"Dummy@gmail.compile"
    },
    license_info={
        "name":"xyz",
        "url":"http://google.com"},
        docs_url="/documentation",redoc_url=None
)



app.include_router(login.router)
app.include_router(product.router)
app.include_router(sellers.router)


models.Base.metadata.create_all(engine)

