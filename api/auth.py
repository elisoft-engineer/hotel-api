from fastapi import APIRouter, Depends, status, HTTPException
from db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas.auth import Token
from db.schemas.users import CustomerCreate, AdminCreate
from db.crud.users import create_customer, get_customer_by_email, create_admin, get_admin_by_email
from core.security import create_access_token


router = APIRouter()


@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def create_new_customer(customer: CustomerCreate, db: AsyncSession = Depends(get_db)):
    if get_customer_by_email(db, customer.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Customer with that email already exists"
        )
    
    db_customer = await create_customer(db, customer)
    if not db_customer:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating account"
        )
    
    access_token = create_access_token(data={"sub": customer})
    return {"access_token": access_token, "token_type": "bearer"}
