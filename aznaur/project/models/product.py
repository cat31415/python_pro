from pydantic import BaseModel


class Product(BaseModel):
    product_id : id
    name : str
    pric : int