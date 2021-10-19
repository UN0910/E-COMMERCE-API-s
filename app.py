# IMPORTING LIBRARIES
from flask import Flask, jsonify, request, json
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_pymongo import PyMongo

# CREATING A FLASK SERVER AND CONNECTING WITH MONGODB
app = Flask(__name__)

# WHEN MONGODB IS RUNNING LOCALLY
# app.config["MONGO_URI"] = "mongodb://localhost:27017/GreendeckTask"

# WHEN BOTH MONGODB AND THIS API APPLICATION IS RUNNING ON DOCKER
app.config["MONGO_URI"] = "mongodb://db:27017/GreendeckTask"
mongo = PyMongo(app)

# DEFINING THE CRUD HTTP METHODS
# BASE ROUTE
@app.route("/")
def base():
    output = jsonify("Welcome to the GREENDECK E-COMMERCE WEBSITE!!!")
    return output


# ROUTE FOR ADDING A NEW PRODUCT
@app.route("/add", methods=["POST"])
def add_product():
    data = request.json
    name = data["name"]
    brand_name = data["brand_name"]
    regular_price_value = data["regular_price_value"]
    offer_price_value = data["offer_price_value"]
    currency = data["currency"]
    classification_l1 = data["classification_l1"]
    classification_l2 = data["classification_l2"]
    classification_l3 = data["classification_l3"]
    classification_l4 = data["classification_l4"]
    image_url = data["image_url"]

    if (
        name
        and brand_name
        and regular_price_value
        and offer_price_value
        and currency
        and classification_l1
        and classification_l2
        and image_url
        and request.method == "POST"
    ):
        mongo.db.eCommerceProducts.insert_one(
            {
                "name": name,
                "brand_name": brand_name,
                "regular_price_value": regular_price_value,
                "offer_price_value": offer_price_value,
                "currency": currency,
                "classification_l1": classification_l1,
                "classification_l2": classification_l2,
                "classification_l3": classification_l3,
                "classification_l4": classification_l4,
                "image_url": image_url,
            }
        )
        output = jsonify("Product added successfully")
        output.status_code = 200
        return output

    else:
        return insufficient_details()


# ROUTE FOR GETTING PRODUCTS LIST
@app.route("/products", methods=["GET"])
def get_products():
    products = mongo.db.eCommerceProducts.find()
    output = dumps(products)
    return output


# ROUTE FOR GETTING A SINGLE PRODUCT
@app.route("/product/<id>", methods=["GET"])
def get_product(id):
    product = mongo.db.eCommerceProducts.find_one({"_id": ObjectId(id)})
    if product:
        resp = dumps(product)
        output = {"MESSAGE": "Product Found!!!", "PRODUCT": resp}
        # output.status_code = 200
        return output

    else:
        return product_not_found()


# ROUTE FOR DELETING A PRODUCT
@app.route("/delete/<id>", methods=["DELETE"])
def delete_product(id):
    product = mongo.db.eCommerceProducts.find_one({"_id": ObjectId(id)})
    if product:
        mongo.db.eCommerceProducts.delete_one({"_id": ObjectId(id)})
        output = jsonify("Product has been deleted!!!")
        output.status_code = 200
        return output

    else:
        return product_not_found()


# ROUTE FOR UPDATING A PRODUCT
@app.route("/update/<id>", methods=["PUT"])
def update_product(id):
    product = mongo.db.eCommerceProducts.find_one({"_id": ObjectId(id)})
    if product:
        data = request.json
        name = data["name"]
        brand_name = data["brand_name"]
        regular_price_value = data["regular_price_value"]
        offer_price_value = data["offer_price_value"]
        currency = data["currency"]
        classification_l1 = data["classification_l1"]
        classification_l2 = data["classification_l2"]
        classification_l3 = data["classification_l3"]
        classification_l4 = data["classification_l4"]
        image_url = data["image_url"]

        if request.method == "PUT":
            mongo.db.eCommerceProducts.update_one(
                {"_id": ObjectId(id["$oid"]) if "$oid" in id else ObjectId(id)},
                {
                    "$set": {
                        "name": name,
                        "brand_name": brand_name,
                        "regular_price_value": regular_price_value,
                        "offer_price_value": offer_price_value,
                        "currency": currency,
                        "classification_l1": classification_l1,
                        "classification_l2": classification_l2,
                        "classification_l3": classification_l3,
                        "classification_l4": classification_l4,
                        "image_url": image_url,
                    }
                },
            )
            output = jsonify("Product updated successfully")
            output.status_code = 200
            return output

        else:
            return insufficient_details()

    else:
        return product_not_found()


# BONUS ROUTES

#  1. How many products have a discount on them?
@app.route("/count_discounted_products", methods=["GET"])
def count_discounted_products():
    products = mongo.db.eCommerceProducts.find(
        {"$expr": {"$lt": ["$offer_price_value", "$regular_price_value"]}}
    ).count()
    output = dumps(products)
    return output


#  2. How many unique brands are present in the collection?
@app.route("/list_unique_brands", methods=["GET"])
def list_unique_brands():
    products = mongo.db.eCommerceProducts.distinct("brand_name")
    output = dumps(products)
    return output


#  3. How many products have offer price greater than 300?
@app.route("/count_high_offer_price", methods=["GET"])
def count_high_offer_price():
    products = mongo.db.eCommerceProducts.find(
        {"offer_price_value": {"$gt": 300}}
    ).count()
    output = dumps(products)
    return output


#  4. How many products have discount % greater than 30%?
@app.route("/count_high_discount", methods=["GET"])
def count_high_discount():
    products = mongo.db.eCommerceProducts.count().where({})
    output = dumps(products)
    return output


# ERROR HANDLERS:
@app.errorhandler(404)
# 1. FOR INSUFFICIENT DETAILS PROVIDED BY THE USER
def insufficient_details(error=None):
    result = {"status": 404, "message": "Sufficient Details were not Provided!!!"}
    output = jsonify(result)
    output.status_code = 404
    return output


# 2. CALLED WHEN THE PRODUCT IS NOT FOUND
def product_not_found(error=None):
    result = {"status": 404, "message": "Product Not found!!!"}
    output = jsonify(result)
    output.status_code = 404
    return output


# INITIALIZING THE DRIVER CODE AT PORT 5050
if __name__ == "__main__":
    app.run(debug=True, port=5050, host="0.0.0.0")
