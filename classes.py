class User:
    def __init__(self,name,age,mobile):
        self.name=name
        self.age=age
        self.mobile=mobile
        self.carts=[]


class Item:
    def __init__(self,name,seller,price):
        self.name=name
        self.seller=seller
        self.price=price


class cart:
    def __init__(self,cartname,total_items,items,total_price):
        self.cartname=cartname
        self.total_items=total_items
        self.items=items
        self.total_price=total_price


