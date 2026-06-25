from models.product import Product

class ProdDB():
    pass

class ProductBD():
    product = [
        Product(id = 1, name = "iPhone 17", pric = 10000),
        Product(id = 2, name = "Keybord", pric = 2500)
    ]

    def add_product(self, prod: Product):
        