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


# def connect_to_db(graph_name):
#     # graph_name = 'bolt://127.0.0.1:7687'
#     my_graph = Graph(graph_name)
#     return my_graph

# def push_new_component(component_name):
#     my_graph = Graph('bolt://127.0.0.1:7687')
#     # my_graph = connect_to_db('bolt://127.0.0.1:7687')
#     add_component_query = """CREATE (s:component {{name: {}}})""".format(component_name)
#     my_graph.run(add_component_query)

@app.route("/")
def main():
    return render_template('intface.html')

@app.route("/addComponent",methods=['GET', 'POST'])
def addComponent():
    print('in add component function')
    # read the posted values from the UI
    component_name = request.form.get('component')
    #connect to graph database
    # push_new_component(component_name)
    return component_name


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
