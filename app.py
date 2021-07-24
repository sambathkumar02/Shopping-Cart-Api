from flask import Flask,json,request
import argparse
from pymongo import MongoClient
import classes


app=Flask(__name__)


#DataBase Connection
try:
    connection=MongoClient('localhost',27017)
    database=connection.shoppingapi
    usercart_collection=database.usercart
    items_collection=database.items
    print("Conenction suceed!")
except Exception as e:
    print(e)


#Route for Creating user
@app.route("/createuser",methods=['POST'])
def CreateUser():
    data=request.json
    try:
        user_obj=classes.User(name=data['name'],age=data['age'],mobile=data['mobile'])
        result=usercart_collection.insert_one(user_obj.__dict__)
        return "ok",201
    except Exception as e:
        return "Error",400

#Route for Creating cart
@app.route("/createcart/",methods=['post'])
def CreateCart():
    username=request.args.get('username')
    data=request.json
    try:
        cart_obj=classes.cart(cartname=data['name'],total_items=0,items=[],total_price=0.0)
        result=usercart_collection.update({"name":username},{"$push":{"carts":cart_obj.__dict__}})
        return "ok",201
    except Exception as e:
        return "Error",400


#Route for adding item to cart
@app.route("/additem",methods=['POST'])    
def AddItem():
    data=request.json
    username=data['username']
    cartname=data['cartname']
    result=items_collection.find_one(data['item'])
    if result==None:
        return "Error",400
    item_price=result['price']
    additemresult=usercart_collection.update({"name":username,"carts.cartname":cartname},{"$push":{"carts.$.items":result}})
    additemresult=usercart_collection.update({"name":username,"carts.cartname":cartname},{"$inc":{"carts.$.total_price":item_price}})
    additemresult=usercart_collection.update({"name":username,"carts.cartname":cartname},{"$inc":{"carts.$.total_items":1}})
    return "ok",202
    

#Route for Delete item
@app.route("/deleteitem",methods=['POST'])
def DeleteItem():
    data=request.json
    username=data['username']
    cartname=data['cartname']
    result=items_collection.find_one(data['item'])
    if result==None:
        return "Error",400
    item_price=result['price']

    delitemresult=usercart_collection.update({"name":username,"carts.cartname":cartname},{"$pull":{"carts.$.items":data['item']}})
    delitemresult=usercart_collection.update({"name":username,"carts.cartname":cartname},{"$inc":{"carts.$.total_price":-(item_price)}})
    delitemresult=usercart_collection.update({"name":username,"carts.cartname":cartname},{"$inc":{"carts.$.total_items":-1}})
    return "ok",202


 #Route for Checkout cart   
@app.route("/checkoutcart/",methods=['GET'])
def CheckoutCart():
    cartname=request.args.get("cartname")
    username=request.args.get("username")
    result=usercart_collection.find_one({"name":username})
    cart=result['carts']
    result_cart={}
    for i in cart:
        if i['cartname']==cartname:
            result_cart=i
    return json.dumps(result_cart)

    

#route for create item
@app.route("/createitem",methods=['POST'])
def CreateItem():
    data=request.json
    try:
        item_object=classes.Item(name=data['name'],seller=data['seller'],price=data['price'])
        result=items_collection.insert_one(item_object.__dict__)
        return "ok",201
    except Exception as e:
        return "error",400


#Route for List all Items
@app.route("/listitems",methods=['GET'])
def ListItems():
    result=items_collection.find()
    if result==None:
        return json.jsonify([])
    items=[]
    for i in result:
        i.pop('_id')
        items.append(i)
    
    return json.jsonify(items)


if __name__=="__main__":
    app.run(debug=True)