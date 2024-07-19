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

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

jackson_family.add_member(
    {"first_name":"Gabriela", "age":24, "luky_number":[30,33,13]}
)
(
    {"first_name":"Valentina", "age":26, "luky_number":[20,22,12]}
)
(
    {"first_name":"Rocket", "age":1, "luky_number":[1,2,3]}
)
(
    {"first_name":"Fausto", "age":2, "luky_number":[4,5,6]}
)
(
    {"first_name":"Emma", "age":1, "luky_number":[7,8,9]}
)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    try:
        members = jackson_family.get_all_members()
        if member is not None:
            return jsonify(members), 200
        else: 
            return jsonify({"error": "No existen miembros"}),400

    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.router ('/members', methods=['POST'])
def  create_member():
     try: 
        body = request.get_json()
        if body is None:
             return jsonify({"error": "El cuerpo no existe"}), 400

        first_name = body.get("first_name", None)
        age = body.get("age",None)
        luky_number = body.get("luky_number", None)
        id = body.get("id" , None)

        if firts_name is None:
            return({"error": "El primer nombre es necesario"}),400
        if age is None:
            return({"error": "La edad es necesario"}),400
        if luky_number is None:
            return({"error": "El numero es necesario"}),400 

        member ={
            "first_name": first_name,
            "age": age,
            "luky_number":luky_number
            }

        if id is not None:
            member["id"]= id

        jackson_family.add_member(member)
        return jsonify(member), 200
    
     except Exception as error:
            return jsonify({"error": str(error)}), 500

@app.route('/member/<int:id>', methods=["GET"])
def get_one_member(id):
    try:
        member = jackson_family.get_member(id)
        if member:
            return jsonify(member),200
        return jsonify({"error": "Miembro no encontrado"}), 400

    except Exception as error:
        return jsonify({"error": str(error)}), 500    

@app.route('/member/<int:id>', methods=["DELETE"])
def delete_member(id):
        try:
            member = jackson_family.delete_member(id)

            if member["done"]:
                return jsonify({"done": True}),200
            else:
                return jsonify({"error": "Miembro no encontrado"}),400

        except Exception as error:
            return jsonify({"error": str(error)}), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
