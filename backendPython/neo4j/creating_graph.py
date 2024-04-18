import langchain.graphs.neo4j_graph as neo4j_graph
import os
import sys
sys.path.append('backendPython')
from llms import *
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # read local .env file
from langchain.chains.graph_qa.cypher import GraphCypherQAChain

graph = neo4j_graph.Neo4jGraph(
  url = os.environ['NEO4J_URI'],
  username=os.environ['NEO4J_USERNAME'],
  password=os.environ['NEO4J_PASSWORD']
)
graph_chain = GraphCypherQAChain.from_llm(
   llm = llm, graph=graph, verbose=True, return_direct=True,validate_cypher=True,
)
# input = {'query': }
# x = graph_chain.run('name companies which offered work location as Kolkata')
# print(x , type(x))
