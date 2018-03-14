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


def push_mc_relationship(parent_meal,meal_component):
    # my_graph = Graph('bolt://127.0.0.1:7687')
    graph_cnxn = connect_to_db('bolt://127.0.0.1:7687')
    meal_component_query ="""match (m:meal {{name:'{}'}})
    match (c:component {{name:'{}'}})
    create p = (m) -[h:has]->(c)""".format(parent_meal,meal_component)
    graph_cnxn.run(meal_component_query)
    print(meal_component_query)

def push_ci_relationship(parent_component,child_ingredient,prep_type):
    # my_graph = Graph('bolt://127.0.0.1:7687')
    graph_cnxn = connect_to_db('bolt://127.0.0.1:7687')
    if prep_type is None:
        component_ingredient_query ="""match (c:component {{name:'{}'}})
        match (i:ingredient {{name:'{}'}})
        create p = (c) -[r:includes]->(i)""".format(parent_component,child_ingredient)
    if prep_type is not None:
        component_ingredient_query ="""match (c:component {{name:'{}'}})
        match (i:ingredient {{name:'{}'}})
        create p = (c) -[r:includes {{prep_type: '{}'}}]->(i)""".format(parent_component,child_ingredient,prep_type)
    graph_cnxn.run(component_ingredient_query)
    print(component_ingredient_query)


def push_cc_relationship(parent_component,child_component):
    # my_graph = Graph('bolt://127.0.0.1:7687')
    graph_cnxn = connect_to_db('bolt://127.0.0.1:7687')
    component_component_query ="""match (c1:component {{name:'{}'}})
    match (c2:component {{name:'{}'}})
    create p = (c1) -[r:includes]->(c2)""".format(parent_component,child_component)
    graph_cnxn.run(component_component_query)
    print(component_component_query)

def push_new_relationship(parent_component,child_ingredient):
    # my_graph = Graph('bolt://127.0.0.1:7687')
    graph_cnxn = connect_to_db('bolt://127.0.0.1:7687')
    create_relationship_query ="""match (c:component {{name:'{}'}})
    match (i:ingredient {{name:'{}'}})
    create p = (c) -[r:includes]->(i)""".format(parent_component,child_ingredient)
    graph_cnxn.run(create_relationship_query)
    print(create_relationship_query)

def push_new_meal(meal_name):
    # my_graph = Graph('bolt://127.0.0.1:7687')
    graph_cnxn = connect_to_db('bolt://127.0.0.1:7687')
    merge_meal_query = """MERGE (m:meal {{name:'{}'}})""".format(meal_name)
    graph_cnxn.run(merge_meal_query)
    print(merge_meal_query)

def push_new_component(component_name):
    # my_graph = Graph('bolt://127.0.0.1:7687')
    graph_cnxn = connect_to_db('bolt://127.0.0.1:7687')
    merge_component_query = """MERGE (c:component {{name:'{}'}})""".format(component_name)
    graph_cnxn.run(merge_component_query)
    print(merge_component_query)

def push_new_ingredient(ingredient_name):
    # my_graph = Graph('bolt://127.0.0.1:7687')
    graph_cnxn = connect_to_db('bolt://127.0.0.1:7687')
    merge_ingredient_query = """MERGE (i:ingredient {{name:'{}'}})""".format(ingredient_name)
    graph_cnxn.run(merge_ingredient_query)
    print(merge_ingredient_query)


@app.route("/addMCRelationship",methods=['GET', 'POST'])
def addMCRelationship():
    print('in add relationship meal component')
    # read the posted values from the UI
    parent_meal = request.form.get('parent_meal')
    meal_component = request.form.get('meal_component')
    #push the meals and components
    push_new_meal(parent_meal)
    push_new_component(meal_component)
    #now push the relationship
    push_mc_relationship(parent_meal,meal_component)
    a_string = parent_meal + ' includes: ' + meal_component
    return a_string

@app.route("/addCCRelationship",methods=['GET', 'POST'])
def addCCRelationship():
    print('in add relationship component component')
    # read the posted values from the UI
    parent_component = request.form.get('parent_component_component')
    child_component = request.form.get('child_component')
    #push the ingredient and components
    push_new_component(parent_component)
    push_new_component(child_component)
    #now push the relationship
    push_cc_relationship(parent_component,child_component)
    a_string = parent_component + ' includes: ' + child_component
    return a_string

@app.route("/addCIRelationship",methods=['GET', 'POST'])
def addCIRelationship():
    # read the posted values from the UI
    parent_component = request.form.get('parent_component')
    child_ingredient = request.form.get('child_ingredient')
    prep_type = request.form.get('prep_type')
    #push the ingredient and components
    push_new_component(parent_component)
    push_new_ingredient(child_ingredient)
    #now push the relationship
    push_ci_relationship(parent_component,child_ingredient,prep_type)
    a_string = parent_component + ' includes: ' + child_ingredient + ' and its MEP is ' + prep_type
    return a_string

@app.route("/addRelationship",methods=['GET', 'POST'])
def addRelationship():
    print('in add relationship function')
    # read the posted values from the UI
    parent_component = request.form.get('parent_component')
    child_ingredient = request.form.get('child_ingredient')
    #push the ingredient and components
    push_new_component(parent_component)
    push_new_ingredient(child_ingredient)
    #now push the relationship
    push_new_relationship(parent_component,child_ingredient)
    print('i pushed your relationship')
    a_string = parent_component + ' includes: ' + child_ingredient
    return a_string

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
