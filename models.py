from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils import ChoiceType

db = create_engine("sqlite:///banco.db")

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email", String, )
    password = Column("password",String)
    active = Column ("active", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.active = active
        self.email = email
        self.admin= admin
        self.password = password

class Order(Base):
    __tablename__ = "orders" 
  

    # STATUS_ORDERS = (
    #     ("PENDING", "PENDING"),
    #     ("CANCEL", "CANCEL"),
    #     ("FINALIZED","FINALIZED")

    # )

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String)
    user = Column("user", ForeignKey("users.id"))
    price = Column("price", Float)
    Items = relationship("ItemOrder", cascade="all, delete")

    def __init__(self, user, status=True, price=0):
        self.user = user
        self.price = price
        self.status = status

    def calculate_price(self):
       self.price = sum(item.price_unity * item.amount for item in self.Items)
        
class ItemOrder(Base):
    __tablename__ = "items_order"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    amount = Column("amount", Integer)
    size = Column("size", String)
    flavor = Column("flavor", String)
    price_unity = Column("price_unity", Float)
    order = Column("order",ForeignKey("orders.id"))

    def __init__ (self, amount, flavor, size, price_unity, order ):
        self.amount = amount
        self.flavor = flavor
        self.order = order
        self.size = size
        self.price_unity = price_unity