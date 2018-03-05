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

def get_query_results(ingredient):
    my_graph = Graph('bolt://127.0.0.1:7687')
    #writing out the query explictly
    query = """MATCH (c:component)-[:includes]-(i)
    where c.name = '{}'
    RETURN i""".format(ingredient)
    
    a = my_graph.run(query)
    b = list(a)
    ing_list = []
    for e in b:
        ing_list.append(e.values()[0]['name'])
    return ing_list
        
@app.route("/")
def main():
    return render_template('index.html')


@app.route("/ingredientSearch",methods=['GET', 'POST'])
def ingredientSearch():
    print("fn executed")
    # read the posted values from the UI
    ingredient = request.form.get('ingredient')
    #code used to do live debugging
    print(ingredient)
    #connect to graph database
    ing_list = get_query_results(ingredient)
    return json.dumps(ing_list)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )


    
