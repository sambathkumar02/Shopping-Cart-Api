# Shopping Cart API
API for shopping cart operations of users such as create cart,add and delete items and checkout cart.


## Endpoints

|Endpoint    |Request-Method|data|
|--------    |--------------|----|
|createitem  |POST          |JSON-name,seller,price|
|listitems   |GET           |nil|
|createuser  |POST          |JSON-name,age,mobile|
|createcart  |POST          |URL-username,JSON-name(for cart)|
|additem     |POST          |URL-username,cartname,JSON-name(item)|
|removeitem  |POST          |URL-username,cartname,JSON-name(item)|
|checkoutcart|GET           |URL-username,cartname|


## Instructions for Use
    prerequisits-Python3,MongoDB

## Steps to Run
Clone the Repo and Create a Virutal Environment and go to the application folder and run 

    pip install -r requirements.txt
After the dependencies were installed , run 

    py app.py or python app.py

