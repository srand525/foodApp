from flask import Flask
from flask import jsonify
from flask import request, send_from_directory
from py2neo import authenticate, Graph
import json
import py2neo

app = Flask(__name__, static_url_path='')


def read_config():
    data = json.load(open('local_config.json'))
    # port_name = data["port_name"]
    return data

def connect_to_db():
	params = read_config()
	password = params['password']
	host = params['host']
	http_port = params['http_port']
	user = params['user']
	graph_cnxn = Graph(password=password,host=host,http_port=http_port,user=user)
	return graph_cnxn

def search_ingredient():
    graph_name = read_config()
    graph_cnxn = connect_to_db()
    search_ingredient_query = """match p = (n)-[:includes]-(m) where m.name = 'garlic' return n.name"""
    # search_ingredient_query = """MATCH (i:ingredient {{name:'{}'}}) return i.name""".format(search_ingredient)
    ingredient_return_cur = graph_cnxn.data(search_ingredient_query)
    return ingredient_return_cur

# def search_ingredient():
#     graph_name = read_config()
#     graph_cnxn = connect_to_db()
#     search_ingredient_query = """match p = (n)-[:includes]-(m) where m.name = 'garlic' return p"""
#     # search_ingredient_query = """MATCH (i:ingredient {{name:'{}'}}) return i.name""".format(search_ingredient)
#     ingredient_return_cur = graph_cnxn.data(search_ingredient_query)
#     return ingredient_return_cur

# this function returns an object for one user
def u(user_id):
    return {
        "type": "foods",                    # It has to have type
        "id": user_id,                      # And some unique identifier
        "attributes": {                     # Here goes actual payload.
            "info": str(user_id),  # the only data we have for each user is "info" field
        },
    }

# routes for individual entities
@app.route('/api/foods/<user_id>')
def users_by_id(user_id):
    # return jsonify({"data": search_ingredient()})
    return jsonify({"data": u(user_id)})

# default route.
# flask has to serve a file that will be generated later with ember
# relative path is backend/static/index.html
@app.route('/')
def root():
    return send_from_directory('static', "index.html")


# route for all entities
@app.route('/api/foods')
def users():
    print('something is happening')
    ingredient_list_all = search_ingredient()
    ingredient_list = [i['n.name'] for i in ingredient_list_all]
    print('something is happening')
    return jsonify({
        "data": [u(i) for i in ingredient_list]
    # return jsonify({
    #     "data": [i for i in search_ingredient()]
        # "data": [u(i) for i in range(0,10)]
        })

# route for other static files
@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('', path)


# if __name__ == '__main__':
#     print("use\n"
#           "FLASK_APP=dummy.py python -m flask run\n"
#           "instead")
#     exit(1)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
