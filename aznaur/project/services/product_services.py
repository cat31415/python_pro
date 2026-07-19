from pydantic import BaseModel
import storage.data as db 
from models.product import Product



class ProductServices :

    def __init__(self, prod_db : db.ProdDB,):
        self.prod_db = prod_db

    def add_prod(
            self,
            prod_id : int,
            prod_name : str,
            pric : int,
            description : str 
            ):
        
        if prod_name is None:
            raise ValueError("")        
        