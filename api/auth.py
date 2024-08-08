from fastapi import APIRouter, Depends, status, HTTPException
from db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas.auth import Token
from db.schemas.users import CustomerCreate, CustomerSignin, AdminCreate, AdminSignin
from db.crud.users import create_customer, get_customer_by_email, create_admin, get_admin_by_email
from core.security import create_access_token, verify_password

router = APIRouter()

"""
This file handles all the endpoints for user account creation and signin
"""


# Customer routes

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_new_customer(customer: CustomerCreate, db: AsyncSession = Depends(get_db)):
    if get_customer_by_email(db, customer.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Customer with that email already exists"
        )

    db_customer = await create_customer(db, customer)
    if not db_customer:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating account")

    return {"detail": "Account created successfully"}


@router.post("/signin", status_code=status.HTTP_200_OK, response_model=Token)
async def signin(customer: CustomerSignin, db: AsyncSession = Depends(get_db)):
    db_customer = await get_customer_by_email(db, customer.email)
    if not db_customer or not verify_password(customer.password, db_customer.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Confirm that the object returned by the coroutine above is compatible with the create_access_token
    access_token = create_access_token(data={"sub": db_customer})
    return {"access_token": access_token, "token_type": "bearer"}


# Admin routes

@router.post("/signup/admin", status_code=status.HTTP_201_CREATED)
async def create_new_admin(admin: AdminCreate, db: AsyncSession = Depends(get_db)):
    if get_admin_by_email(db, admin.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Admin with that email already exists"
        )

    db_admin = await create_admin(db, admin)
    if not db_admin:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating account"
        )

    return {"detail": "Account created successfully"}


@router.post("/signin/admin", response_model=Token, status_code=status.HTTP_200_OK)
async def admin_signin(admin: AdminSignin, db: AsyncSession = Depends(get_db)):
    db_admin = await get_admin_by_email(db, admin.email)
    if not db_admin or not verify_password(admin.password, db_admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Confirm that the object returned by the coroutine above is compatible with the create_access_token
    access_token = create_access_token(data={"sub": db_admin})
    return {"access_token": access_token, "token_type": "bearer"}
