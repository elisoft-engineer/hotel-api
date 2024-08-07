from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from db.models import users as models
from db.schemas import users as schemas
from core.security import get_password_hash


"""
The following are the admin CRUD utilities
"""


async def get_admins(db: AsyncSession, offset: int | None = None, limit: int | None = None):
    results = await db.execute(select(models.Admin).offset(offset).limit(limit))
    return results.scalars().all()


async def get_admin(db: AsyncSession, id: UUID):
    result = await db.execute(select(models.Admin).where(models.Admin.id == id))
    return result.scalars().first()


async def get_admin_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.Admin).where(models.Admin.email == email))
    return result.scalars().first()


async def create_admin(db: AsyncSession, admin: schemas.AdminCreate):
    admin_data = admin.model_dump()
    admin_data['password'] = get_password_hash(admin.password)
    db_admin = models.Admin(**admin_data)
    db.add(db_admin)
    await db.commit()
    await db.refresh(db_admin)
    return db_admin


async def update_admin(db: AsyncSession, id: UUID, admin_update: schemas.AdminUpdate):
    admin = await get_admin(db, id)
    if not admin:
        return None
    
    update_data = admin_update.model_dump(exclude_unset=True)
    for key, value in update_data:
        setattr(admin, key, value)


    db.add(admin)
    await db.commit()
    await db.refresh(admin)
    return admin


async def delete_admin(db: AsyncSession, id: UUID):
    admin = await get_admin(db, id)
    if not admin:
        return None
    
    await db.delete(admin)
    await db.commit()
    return {"message": "Admin account deleted successfully"}


"""
The following are the customer CRUD utilities
"""


async def get_customers(db: AsyncSession, offset: int | None = None, limit: int | None = None):
    results = await db.execute(select(models.Customer).offset(offset).limit(limit))
    return results.scalars().all()


async def get_customer(db: AsyncSession, id: UUID):
    result = await db.execute(select(models.Customer).where(models.Customer.id == id))
    return result.scalars().first()


async def get_customer_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.Customer).where(models.Customer.email == email))
    return result.scalars().first()


async def create_customer(db: AsyncSession, customer: schemas.CustomerCreate):
    customer_data = customer.model_dump()
    customer_data['password'] = get_password_hash(customer.password)
    db_customer = models.Customer(**customer_data)
    db.add(db_customer)
    await db.commit()
    await db.refresh(db_customer)
    return db_customer


async def update_customer(db: AsyncSession, id: UUID, customer_update: schemas.CustomerUpdate):
    customer = await get_customer(db, id)
    if not customer:
        return None
    
    update_data = customer_update.model_dump(exclude_unset=True)
    for key, value in update_data:
        setattr(customer, key, value)


    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    return customer


async def delete_customer(db: AsyncSession, id: UUID):
    customer = await get_customer(db, id)
    if not customer:
        return None
    
    await db.delete(customer)
    await db.commit()
    return {"message": "Customer account deleted successfully"}
