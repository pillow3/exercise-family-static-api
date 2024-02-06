"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

family= []

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# GET /member/id
@app.route('/member/<int:member_id>', methods=['POST'])
def method_name():
    pass

# POST /member
@app.route('/member', methods=['POST'])
def add():
    request_body = request.json

    # Obtenemos el parametro que introducimos en el json body
    first_name = request_body.get("first_name")
    last_name = request_body.get("last_name")
    age = request_body.get("age")
    lucky_numbers = request_body.get("lucky_numbers")

    member = jackson_family.add_member(first_name, last_name, age, lucky_numbers)

    return jsonify({"message": f"New member added{member}"}), 201

# DELETE /member/<id>
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete(member_id):
    jackson_family.delete_member(member_id)

    return jsonify({"message":f"Member has beend delete {member_id}"})

# GET /member/<id>
@app.route('/member/<int:member_id>', methods=['GET'])
def get_id(member_id):
    jackson_family.get_member(member_id)

    return jsonify({"message":f"The member {member_id}"})
    

# GET /members
@app.route('/members', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }


    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
