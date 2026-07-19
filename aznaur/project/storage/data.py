from models.product import Product

class ProdDB():
    def add_product(self, prod: Product):
        pass

    def get_prod_id(self, id: int):
        pass

    def get_prod(self):
        pass



class ProductBD(ProdDB):
    product = [
        Product(id = 1, name = "iPhone 17", pric = 10000, description = ""),
        Product(id = 2, name = "Keybord", pric = 2500, description = "")
    ]

    def add_product(self, prod: Product):
        for p in self.product:
            if p.id == prod.id:
                raise ValueError
        self.product.append(prod)

    def get_prod_id(self, id: int):
        for p in self.product:
            if p == id:
                return p
            
            pass

    def get_prod(self):
        return self.product
    



