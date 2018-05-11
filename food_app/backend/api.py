from flask import Flask,jsonify,request, send_from_directory
import code
import py2neo
import os
import glob
import json
from os import listdir
from py2neo import Graph, Node, NodeSelector,authenticate

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

def json_sigma():
    print('stuffs happening!')
    graph_cnxn = connect_to_db()
    node_result = graph_cnxn.data("MATCH (a) WITH collect({node_id: id(a),node_type:labels(a)[0],node_name:a.name}) AS nodes RETURN nodes")
    rel_result = graph_cnxn.data("MATCH (a)-[r]->(b) where b.name = 'garlic' WITH collect({source_id: id(a), target_id: id(b),rel_id: id(r),rel_properties:properties(r),rel_type:type(r)}) AS edges  RETURN edges")
    sigma_input = {'nodes':node_result[0]['nodes'],'edges':rel_result[0]['edges']}
    return sigma_input

@app.route('/api/graphs')
def graphs():
    return jsonify({"data": {"attributes": json_sigma()}})

# @app.route('/api/graphs/')
# def sigma_input():
#     return jsonify({"data": {"attributes": json_sigma()}})

##INGREDIENTS

def ingredient_id_list():
    graph_name = read_config()
    graph_cnxn = connect_to_db()
    input_ingredient = "garlic"
    search_ingredient_query = """match p = (n)-[:includes]-(m) where m.name = '{}' return n.name as ingredient_name,id(n) as ingredient_id""".format(input_ingredient)
    ingredient_return_cur = graph_cnxn.data(search_ingredient_query)
    ing_name_list = [a['ingredient_id'] for a in ingredient_return_cur]
    return ing_name_list

def ing_info(ing_id):
    graph_name = read_config()
    graph_cnxn = connect_to_db()
    ing_query = "MATCH (a) where id(a) = {} return id(a) as nodeid,a.name as ingname".format(ing_id)
    ing_return_cur = graph_cnxn.data(ing_query)
    return ing_return_cur

def ing(ing_id):
    ingr_info = ing_info(ing_id)
    info_dict = ingr_info[0]
    return {
        "type": "ingredients",                    # It has to have type
        "id": info_dict['nodeid'],
        "attributes": {                     # Here goes actual payload.
            # "info": str(user_id),  # the only data we have for each user is "info" field
            "ingname":info_dict['ingname']
        },
    }

@app.route('/api/ingredients/<ing_id>')
def ings_by_id(ing_id):
    return jsonify({"data": ing(ing_id)})

@app.route('/api/ingredients')
def ingredients():
    ing_id_list = ingredient_id_list()
    return jsonify({
        "data":  [ing(i) for i in ing_id_list]
        })



##NODES

def nodes_ids():
    graph_name = read_config()
    graph_cnxn = connect_to_db()
    #     node_query = "MATCH (a) WITH collect({attributes:{node_id: id(a),node_type:labels(a)[0],node_name:a.name}}) AS data RETURN data"
    node_query = "MATCH (a) return id(a) as nodeid"
    node_return_cur = graph_cnxn.data(node_query)
    node_ids = [a['nodeid'] for a in node_return_cur]
    return node_ids

def nodes_info(node_id):
    graph_name = read_config()
    graph_cnxn = connect_to_db()
    node_query = "MATCH (a) where id(a) = {} return id(a) as nodeid,labels(a)[0] as nodetype,a.name as nodename".format(node_id)
    node_return_cur = graph_cnxn.data(node_query)
    return node_return_cur

def n(node_id):
    node_info = nodes_info(node_id)
    info_dict = node_info[0]
    return {
        "type": "nodes",                    # It has to have type
        "id": info_dict['nodeid'],
        "attributes": {                     # Here goes actual payload.
            # "info": str(user_id),  # the only data we have for each user is "info" field
            "nodename":info_dict['nodename'],
            "nodetype":info_dict['nodetype']
        },
    }


@app.route('/api/nodes/<nodeid>')
def nodes_by_id(node_id):
    return jsonify({"data": n(node_id)})

@app.route('/api/nodes')
def nodes():
    node_id_list = nodes_ids()
    return jsonify({
        "data": [n(i) for i in node_id_list]
        })

@app.route('/')
def root():
    return send_from_directory('static', "index.html")

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
