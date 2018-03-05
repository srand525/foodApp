import py2neo
from py2neo import Graph
import os
import glob
from os import listdir
from neo4j.v1 import GraphDatabase


def main():
	#connect to graph database
	my_graph = Graph('bolt://127.0.0.1:7687')
	#writing out the query explictly
	query = """MATCH (c:component)-[:includes]-(i:ingredient)
	where i.name = 'green_beans'
	RETURN c"""
	a = my_graph.run(query)
	b = list(a)
    return b


 if __name__ == "__main__":
 	main()
