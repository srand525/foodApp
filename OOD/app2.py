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


@app.route("/ingredientSearch",methods=['GET', 'POST'])
def ingredientSearch():
    # read the posted values from the UI
    ingredient = request.form.get('ingredient')
    return ingredient
    
if __name__ == "__main__":
    app.run()
