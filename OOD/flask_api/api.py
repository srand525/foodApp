from flask import Flask, request, render_template, send_from_directory
import code
from py2neo import authenticate, Graph
import py2neo
import os
import glob
import json
import jsonify
from os import listdir
from neo4j.v1 import GraphDatabase

# app = Flask(__name__)

app = Flask(__name__,static_url_path = '')

def ingredient(ingredient_name):
    return {
    'node_type':ingredient
    "name":ingredient_name
    }

# routes for individual entities
@app.route('/api/ingredient/<ingredient_name>')
def ingredients_by_name(ingredient_name):
    return jsonify({"data": ingredient(ingredient_name)})

# default route.
# flask has to serve a file that will be generated later with ember
# relative path is backend/static/index.html
@app.route('/')
def root():
    return send_from_directory('static', "index.html")


# route for all entities
@app.route('/api/ingredients')
def users():
    return jsonify({
        "data": [ingredients(i) for i in ['onion','garlic']]
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
#
# @app.route("/")
# def main():
#     return render_template('index.html')
#
# def read_config():
#     data = json.load(open('config.json'))
#     # port_name = data["port_name"]
#     return data
#
# def connect_to_db():
# 	params = read_config()
# 	password = params['password']
# 	host = params['host']
# 	http_port = params['http_port']
# 	user = params['user']
# 	graph_cnxn = Graph(password=password,host=host,http_port=http_port,user=user)
# 	return graph_cnxn
#
# def push_mc_relationship(parent_meal,meal_component):
#     params = read_config()
#     graph_cnxn = _db()
#     meal_component_query ="""match (m:meal {{name:'{}'}}) match (c:component {{name:'{}'}})
#     create p = (m) -[h:has]->(c)""".format(parent_meal,meal_component)
#     graph_cnxn.run(meal_component_query)
#     print(meal_component_query)
#
# def push_ci_relationship(parent_component,child_ingredient,prep_type):
#     graph_name = read_config()
#     graph_cnxn = connect_to_db()
#     if prep_type is None:
#         component_ingredient_query ="""match (c:component {{name:'{}'}})
#         match (i:ingredient {{name:'{}'}})
#         create p = (c) -[r:includes]->(i)""".format(parent_component,child_ingredient)
#     if prep_type is not None:
#         component_ingredient_query ="""match (c:component {{name:'{}'}})
#         match (i:ingredient {{name:'{}'}})
#         create p = (c) -[r:includes {{prep_type: '{}'}}]->(i)""".format(parent_component,child_ingredient,prep_type)
#     graph_cnxn.run(component_ingredient_query)
#     print(component_ingredient_query)
#
# def push_cc_relationship(parent_component,child_component):
#     graph_name = read_config()
#     graph_cnxn = connect_to_db()
#     component_component_query ="""match (c1:component {{name:'{}'}})
#     match (c2:component {{name:'{}'}})
#     create p = (c1) -[r:includes]->(c2)""".format(parent_component,child_component)
#     graph_cnxn.run(component_component_query)
#     print(component_component_query)
#
# def push_new_relationship(parent_component,child_ingredient):
#     graph_name = read_config()
#     graph_cnxn = connect_to_db()
#     create_relationship_query ="""match (c:component {{name:'{}'}})
#     match (i:ingredient {{name:'{}'}})
#     create p = (c) -[r:includes]->(i)""".format(parent_component,child_ingredient)
#     graph_cnxn.run(create_relationship_query)
#     print(create_relationship_query)
#
# def push_new_meal(meal_name):
#     graph_name = read_config()
#     graph_cnxn = connect_to_db()
#     merge_meal_query = """MERGE (m:meal {{name:'{}'}})""".format(meal_name)
#     graph_cnxn.run(merge_meal_query)
#     print(merge_meal_query)
#
# def push_new_component(component_name):
#     graph_name = read_config()
#     graph_cnxn = connect_to_db()
#     merge_component_query = """MERGE (c:component {{name:'{}'}})""".format(component_name)
#     graph_cnxn.run(merge_component_query)
#     print(merge_component_query)
#
# def push_new_ingredient(ingredient_name):
#     graph_name = read_config()
#     graph_cnxn = connect_to_db()
#     merge_ingredient_query = """MERGE (i:ingredient {{name:'{}'}})""".format(ingredient_name)
#     graph_cnxn.run(merge_ingredient_query)
#     print(merge_ingredient_query)
#
# def search_component(search_component):
#     graph_name = read_config()
#     graph_cnxn = connect_to_db()
#     search_component_query = """MATCH (c:component {{name:'{}'}}) return c.name""".format(search_component)
#     component_return_cur = graph_cnxn.run(search_component_query)
#     component_return = str(component_return_cur.evaluate())
#     searched_component = component_return
#     if component_return == 'None':
#         searched_component = 'there is no component ' + search_component
#     return searched_component
#
# def search_ingredient(search_ingredient):
#     graph_name = read_config()
#     graph_cnxn = connect_to_db()
#     search_ingredient_query = """MATCH (i:ingredient {{name:'{}'}}) return i.name""".format(search_ingredient)
#     ingredient_return_cur = graph_cnxn.run(search_ingredient_query)
#     ingredient_return = str(ingredient_return_cur.evaluate())
#     searched_ingredient = ingredient_return
#     if ingredient_return == 'None':
#         searched_ingredient = 'there is no component ' + search_ingredient
#     return searched_ingredient
#
# @app.route('/create_data', methods=['GET', 'POST'])
# def create_data():
#     if request.method == 'POST':
#         return redirect(url_for('index'))
#     # show the form, it wasn't submitted
#     return render_template('create_data.html')
#
# @app.route('/query_data', methods=['GET', 'POST'])
# def query_data():
#     if request.method == 'POST':
#         return redirect(url_for('index'))
#     # show the form, it wasn't submitted
#     return render_template('query_data.html')
#
# @app.route("/searchIngredient",methods=['GET', 'POST'])
# def searchIngredient():
#     ingredient_to_search = request.form.get('search_ingredient')
#     searched_ingredient = search_ingredient(ingredient_to_search)
#     return searched_ingredient
#
# @app.route("/searchComponent",methods=['GET', 'POST'])
# def searchComponent():
#     component_to_search = request.form.get('search_component')
#     searched_component = search_component(component_to_search)
#     return searched_component
#
# @app.route("/addMCRelationship",methods=['GET', 'POST'])
# def addMCRelationship():
#     print('in add relationship meal component')
#     # read the posted values from the UI
#     parent_meal = request.form.get('parent_meal')
#     meal_component = request.form.get('meal_component')
#     #push the meals and components
#     push_new_meal(parent_meal)
#     push_new_component(meal_component)
#     #now push the relationship
#     push_mc_relationship(parent_meal,meal_component)
#     a_string = parent_meal + ' includes: ' + meal_component
#     return a_string
#
# @app.route("/addCCRelationship",methods=['GET', 'POST'])
# def addCCRelationship():
#     print('in add relationship component component')
#     # read the posted values from the UI
#     parent_component = request.form.get('parent_component_component')
#     child_component = request.form.get('child_component')
#     #push the ingredient and components
#     push_new_component(parent_component)
#     push_new_component(child_component)
#     #now push the relationship
#     push_cc_relationship(parent_component,child_component)
#     a_string = parent_component + ' includes: ' + child_component
#     return a_string
#
# @app.route("/addCIRelationship",methods=['GET', 'POST'])
# def addCIRelationship():
#     # read the posted values from the UI
#     parent_component = request.form.get('parent_component')
#     child_ingredient = request.form.get('child_ingredient')
#     prep_type = request.form.get('prep_type')
#     #push the ingredient and components
#     push_new_component(parent_component)
#     push_new_ingredient(child_ingredient)
#     #now push the relationship
#     push_ci_relationship(parent_component,child_ingredient,prep_type)
#     a_string = parent_component + ' includes: ' + child_ingredient + ' and its MEP is ' + prep_type
#     return a_string
#
# @app.route("/addRelationship",methods=['GET', 'POST'])
# def addRelationship():
#     print('in add relationship function')
#     # read the posted values from the UI
#     parent_component = request.form.get('parent_component')
#     child_ingredient = request.form.get('child_ingredient')
#     #push the ingredient and components
#     push_new_component(parent_component)
#     push_new_ingredient(child_ingredient)
#     #now push the relationship
#     push_new_relationship(parent_component,child_ingredient)
#     print('i pushed your relationship')
#     a_string = parent_component + ' includes: ' + child_ingredient
#     return a_string
#
# @app.route("/addIngredient",methods=['GET', 'POST'])
# def addIngredient():
#     print('in add ingredient function')
#     # read the posted values from the UI
#     ingredient_name = request.form.get('ingredient')
#     #connect to graph database
#     push_new_ingredient(ingredient_name)
#     print('i pushed your ingredient')
#     return ingredient_name
#
# @app.route("/addComponent",methods=['GET', 'POST'])
# def addComponent():
#     print('in add component function')
#     # read the posted values from the UI
#     component_name = request.form.get('component')
#     #connect to graph database
#     push_new_component(component_name)
#     print('i pushed your component')
#     return component_name

# if __name__ == '__main__':
#     app.run(
#         host="0.0.0.0",
#         port=5000,
#         debug=True
#     )
