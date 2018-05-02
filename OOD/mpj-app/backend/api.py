from flask import Flask
from flask import jsonify
from flask import request, send_from_directory

app = Flask(__name__, static_url_path='')

# this function returns an object for one user
def u(user_id):
    return {
        "type": "users",                    # It has to have type
        "id": user_id,                      # And some unique identifier
        "attributes": {                     # Here goes actual payload.
            "info": "data" + str(user_id),  # the only data we have for each user is "info" field
        },
    }

# routes for individual entities
@app.route('/api/users/<user_id>')
def users_by_id(user_id):
    return jsonify({"data": u(user_id)})

# default route.
# flask has to serve a file that will be generated later with ember
# relative path is backend/static/index.html
@app.route('/')
def root():
    return send_from_directory('static', "index.html")


# route for all entities
@app.route('/api/users')
def users():
    return jsonify({
        "data": [u(i) for i in range(0,10)]
        })

# route for other static files
@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('', path)


if __name__ == '__main__':
    print("use\n"
          "FLASK_APP=dummy.py python -m flask run\n"
          "instead")
    exit(1)

# if __name__ == '__main__':
#     app.run(
#         host="0.0.0.0",
#         port=5000,
#         debug=True
#     )
# from flask import Flask, request, render_template, send_from_directory
# import code
# from py2neo import authenticate, Graph
# import py2neo
# import os
# import glob
# import json
# import jsonify
# from os import listdir
# from neo4j.v1 import GraphDatabase
#
# # app = Flask(__name__)
#
# app = Flask(__name__,static_url_path = '')
#
# def ingredient(ingredient_name):
#     return {
#     'node_type':ingredient
#     "name":ingredient_name
#     }
#
# # routes for individual entities
# @app.route('/api/ingredient/<ingredient_name>')
# def ingredients_by_name(ingredient_name):
#     return jsonify({"data": ingredient(ingredient_name)})
#
# # default route.
# # flask has to serve a file that will be generated later with ember
# # relative path is backend/static/index.html
# @app.route('/')
# def root():
#     return send_from_directory('static', "index.html")
#
#
# # route for all entities
# @app.route('/api/ingredients')
# def users():
#     return jsonify({
#         "data": [ingredients(i) for i in ['onion','garlic']]
#         })
#
# # route for other static files
# @app.route('/<path:path>')
# def send_js(path):
#     return send_from_directory('', path)
#
#
# if __name__ == '__main__':
#     print("use\n"
#           "FLASK_APP=dummy.py python -m flask run\n"
#           "instead")
#     exit(1)
