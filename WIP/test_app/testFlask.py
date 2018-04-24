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
    return render_template('creating_new_fieldsindex.html')

def connect_to_db(graph_name):
    graph_cnxn = Graph(graph_name)
    return graph_cnxn

def read_config():
    data = json.load(open('config.json'))
    port_name = data["port_name"]
    return port_name

def push_new_component(component_name):
    graph_name = read_config()
    graph_cnxn = connect_to_db(graph_name)
    merge_component_query = """MERGE (c:component {{name:'{}'}})""".format(component_name)
    graph_cnxn.run(merge_component_query)
    print(merge_component_query)


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
