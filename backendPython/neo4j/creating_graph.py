import langchain.graphs.neo4j_graph as neo4j_graph
import os
import sys
import ast
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

prefix = ''' 

You are supposed to convert the following natural query into a cypher query for neo4j database
You can refer to  below examples for getting idea of how to write cypher query for neo4j database.

'''

suffix = '''
create a cypher query for following  natural query for neo4j database

The query has the following list of nodes :
    {List_of_nodes}
    
You can create relations between the nodes in following manner :
    Node1 : Company
    Node2 : CGPA
    Relation1 : Company_to_CGPA
    Relation2 : CGPA_to_Company

    
natural_query :
{natural_query}

Do not put back-ticks(`) in the output.
Use only nodes provided , don't create your new nodes and relations.
 '''


few_shot_prompt = FewShotPromptTemplate( 
    examples=examples,

    # prompt template used to format each individual example
    example_prompt=example_prompt,

    # prompt template string to put before the examples, assigning roles and rules.
    prefix=prefix ,
    
    # prompt template string to put after the examples.
    suffix=suffix ,
    
    # input variable to use in the suffix template
    input_variables=["List_of_nodes" , "natural_query"],
    example_separator="\n", 
)


cypher_chain = LLMChain(llm=llm, prompt=few_shot_prompt,verbose=False,)
#__________________________________________________________________________________________________
# cypher = cypher_chain.run({"List_of_nodes" :['Company' , 'CGPA'] , 'natural_query':'name 10 companies which came for cgpa below 7'})

# result = graph.query(cypher)
# print(result)

#__________________________________________________________________________________________________
result_template = '''

You will be provided with the response generated for the given user query.

Response :
{response}

You need to format the respone in html in a conversational way,
arrange the response in bulleted points and under major headings if possible.

Take care that you do not pollute the data provided in response, by adding your own data.

Check that there are no back-ticks(`) in the output.
Check that html syntax is correct.
'''

result_prompt = PromptTemplate(input_variables=['response'], template=result_template)

result_chain = LLMChain(llm=llm, prompt=result_prompt)
# print(result_chain.run({'response': result}))

# #__________________________________________________________________________________________________

def get_response(query):
    print('\n\n\n\n', query)
    li = get_nodes_chain.run(query)
    print(li)
    if type(li)==str:
        li = ast.literal_eval(li) 

    cypher = cypher_chain.run({"List_of_nodes" : li, 'natural_query':query})
    print('\n\n\n', cypher,'\n\n\n')
    result = graph.query(cypher)
    print('\n\n\n', result)
    response = result_chain.run({'response': result})
    # print('\n\n\n', response)
    return response


# x = get_response('what ctc is offered for cgpa below 7, sort the ctc in descending order')
# x = get_response("list companies with ctc above 30")
# x= get_response("list companies with ctc above 30 and cgpa below 8")
# x = get_response('name 10 companies which offered ctc above 20')
# x = get_response('jobProfiles available for cgpa below 7')
# print(x)







