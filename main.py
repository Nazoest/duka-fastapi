from typing import Union, List
from fastapi import FastAPI, Depends,HTTPException, status
from sqlalchemy.orm import Session,selectinload
from models import Base,engine,SessionLocal
from sqlalchemy import select
from jsonmap import ProductGetMap, ProductPostMap, SaleGetMap, SalePostMap, UserPostRegister, UserPostLogin
from models import Product,Sale,User


app = FastAPI()

# Create tables on startup
@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"Duka FastAPI": "Version 1.0"}

@app.post("/register",response_model=UserPostRegister)
def register_user(user: UserPostRegister):
    if SessionLocal.execute(
        select(User).where(User.email==user.email)
    ).scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    model_obj=User(
        email=user.email,
        username=user.username,
        password=user.password
    )
    SessionLocal.add(model_obj)
    SessionLocal.commit()
    return model_obj

@app.post("/login",response_model=UserPostLogin)
def login_user(user: UserPostLogin):
    db_user=SessionLocal.execute(
    select(User).where(User.email==user.email, User.password==user.password)
    ).scalar_one_or_none()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    return db_user
   

@app.get("/products", response_model=List[ProductGetMap])
def get_products():
    products=select(Product)
    return SessionLocal.scalars(products)

@app.post("/products", response_model=ProductGetMap)
def create_product(json_product_obj: ProductPostMap):
    model_obj=Product(
        name=json_product_obj.name,
        buying_price=json_product_obj.buying_price,
        selling_price=json_product_obj.selling_price
    )
    SessionLocal.add(model_obj)
    SessionLocal.commit()
    return model_obj

    

@app.get("/sales",response_model=List[SaleGetMap])
def get_sales():
    sales=select(Sale).options(selectinload(Sale.product))
    return SessionLocal.scalars(sales).all()

@app.post("/sales", response_model=SaleGetMap)
def create_sale(json_sale_obj: SalePostMap):
    model_obj=Sale(
        product_id=json_sale_obj.product_id,
        quantity=json_sale_obj.quantity
    )
    SessionLocal.add(model_obj)
    SessionLocal.commit()
    return model_obj
