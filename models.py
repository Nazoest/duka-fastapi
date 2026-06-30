from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship,Session,sessionmaker
from datetime import datetime

from sqlalchemy import create_engine
DATABASE_URL="postgresql://postgres:Nazo@my_postgres:5432/flaskapi"
#DATABASE_URL = "sqlite:///./pos.db"


engine = create_engine(
    DATABASE_URL
) 

""" engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
) """

SessionFactory = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    """Create a new session per request."""
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


class Base(DeclarativeBase):
     pass

class User(Base):
    __tablename__ = "fastapiusers"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    fullname: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    buying_price: Mapped[float] = mapped_column(nullable=False)
    selling_price: Mapped[float] = mapped_column(nullable=False)

    sales: Mapped[List["Sale"]] = relationship(back_populates="product")


class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    product: Mapped["Product"] = relationship(back_populates="sales")
    payment: Mapped[Optional["Payment"]] = relationship(back_populates="sale", uselist=False)

class Purchase(Base):
    __tablename__ = "purchases"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    stock_quantity: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    product: Mapped["Product"] = relationship()

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    sale_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sales.id"), nullable=True)
    mrid: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    crid: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    trans_code: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    trans_amount: Mapped[float] = mapped_column(nullable=False)
    phone_paid: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    sale: Mapped[Optional["Sale"]] = relationship(back_populates="payment")

