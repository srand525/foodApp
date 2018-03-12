from flask import Flask, request, render_template
import code
import py2neo
from py2neo import Graph
import os
import glob
import json
from os import listdir
from neo4j.v1 import GraphDatabase

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('intface.html')

def connect_to_db(graph_name):
    graph_cnxn = Graph(graph_name)
    return graph_cnxn

def push_new_component(component_name):
    # my_graph = Graph('bolt://127.0.0.1:7687')
    graph_cnxn = connect_to_db('bolt://127.0.0.1:7687')
    merge_component_query = """MERGE (c:component {{name:'{}'}})""".format(component_name)
    graph_cnxn.run(merge_component_query)
    print(merge_component_query)

# new_component = "'sauteed kale'"
# component_includes_1 = "'sauteed onion and garlic'"
# component_includes_2 = "'kale'"

#
# def push_new_ingredient(ingredient_name):
#     # my_graph = Graph('bolt://127.0.0.1:7687')
#     graph_cnxn = connect_to_db('bolt://127.0.0.1:7687')
#     # ingredient_format = "'" + ingredient_name + "'"
#     # new_component = = "'" + ingredient_name + "'"
#     new_component = "'sauteed kale'"
#     component_includes_1 = "'sauteed onion and garlic'"
#     component_includes_2 = "'" + ingredient_name + "'"
#     # add_ingredient_query = """CREATE (i:ingredient {{name: {}}})""".format(ingredient_format)
#     # merge_ingredient_query = """MERGE (i:ingredient {{name:{}}})""".format(ingredient_format)
#     merge_ingredient_query = """MATCH (c1:component {{name: {}}}), (c2:component {{name: {}}})
#     ,(i:ingredient {{name:{}}}) CREATE (c1)-[:includes]->(c2) CREATE (c1)-[:includes]->(i)"""
#     .format(new_component,component_includes_1,component_includes_2).replace("\n","")
#     # graph_cnxn.run(relationship_query)
#     print(merge_ingredient_query)
#     # print(merge_ingredient_query)

def push_new_ingredient(ingredient_name):
    # my_graph = Graph('bolt://127.0.0.1:7687')
    graph_cnxn = connect_to_db('bolt://127.0.0.1:7687')
    merge_ingredient_query = """MERGE (i:ingredient {{name:'{}'}})""".format(ingredient_name)
    graph_cnxn.run(merge_ingredient_query)
    print(merge_ingredient_query)

@app.route("/addIngredient",methods=['GET', 'POST'])
def addIngredient():
    print('in add ingredient function')
    # read the posted values from the UI
    ingredient_name = request.form.get('ingredient')
    #connect to graph database
    push_new_ingredient(ingredient_name)
    print('i pushed your ingredient')
    return ingredient_name

@app.route("/addComponent",methods=['GET', 'POST'])
def addComponent():
    print('in add component function')
    # read the posted values from the UI
    component_name = request.form.get('component')
    #connect to graph database
    push_new_component(component_name)
    print('i pushed your component')
    return component_name

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
