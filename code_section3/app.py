from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "My Item",
                "price": 15.99
            }
        ]
    }
]


@app.route("/")
def home():
    return render_template("index.html")


# POST /store data: {name:}
@app.route('/store', methods=['POST'])  # @app.route('/store', methods=['POST', 'GET'])
def create_store():
    request_data = request.get_json()
    new_store = {
        "name": request_data["name"],
        "items": []
    }
    stores.append(new_store)
    return jsonify(new_store)


# GET /store/<string:name>
@app.route("/store/<string:name>")  # special flask syntax for http-address/name
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify(store)
    return jsonify({"message": "store not found"})


# GET /store
@app.route("/store")
def get_stores():
    return jsonify({"stores": stores})


# POST /store/<string:name>/item {name:, price:}
@app.route("/store/<string:name>/item", methods=["POST"])  # 127.0.0.1:11112/name/item
def create_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            item = request.get_json()
            store["items"].append(item)
            return jsonify(item)
    return jsonify({"message": "store not found"})


# GET /store/<string:name>/item
@app.route("/store/<string:name>/item")  # 127.0.0.1:11112/name/item
def get_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify({"items": store["items"]})
    return jsonify({"message": "store not found"})


app.run(port=11112)
