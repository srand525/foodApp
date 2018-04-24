import code
import py2neo
from py2neo import Graph
from neo4j.v1 import GraphDatabase

def connect_to_db(graph_name):
    graph_cnxn = Graph(graph_name)
    return graph_cnxn

graph_cnxn = connect_to_db('bolt://127.0.0.1:7687')

if __name__ == '__main__':
    graph_cnxn = connect_to_db('bolt://127.0.0.1:7687')