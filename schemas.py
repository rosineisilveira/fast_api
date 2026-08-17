from pydantic import BaseModel
from typing import Optional, List


class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    active: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True

class OrderSchema(BaseModel):
    id_user: int

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

class ItemOrderSchema(BaseModel):
    amount: int
    flavor: str
    size: str
    price_unity: float

    class Config:
        from_attributes = True
    
class ResponseOrderSchema(BaseModel):
    id : int
    status : str
    price : float
    Items: List[ItemOrderSchema]

    class Config:
        from_attributes = True
    