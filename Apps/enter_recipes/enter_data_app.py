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
    component_format = "'" + component_name + "'"
    add_component_query = """CREATE (s:component {{name: {}}})""".format(component_format)
    graph_cnxn.run(add_component_query)
    print(add_component_query)

# def push_new_ingredient(ingredient_name):
#     # my_graph = Graph('bolt://127.0.0.1:7687')
#     graph_cnxn = connect_to_db('bolt://127.0.0.1:7687')
#     ingredient_format = "'" + ingredient_name + "'"
#     add_ingredient_query = """CREATE (i:ingredient {{name: {}}})""".format(ingredient_format)
#     graph_cnxn.run(add_ingredient_query)
#     print(add_ingredient_query)

def push_new_ingredient(ingredient_name):
    # my_graph = Graph('bolt://127.0.0.1:7687')
    graph_cnxn = connect_to_db('bolt://127.0.0.1:7687')
    ingredient_format = "'" + ingredient_name + "'"
    # add_ingredient_query = """CREATE (i:ingredient {{name: {}}})""".format(ingredient_format)
    merge_ingredient_query = """MERGE (i:ingredient {{name:{}}})""".format(ingredient_format)
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
