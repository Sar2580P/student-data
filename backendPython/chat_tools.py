from langchain.agents import Tool
from langchain_google_community.search import GoogleSearchAPIWrapper
from prompts import *
from llms import *
from parsers import *
from chains import *
from profile_retrivers import *
from backendPython.neo4j.creating_graph import graph_chain

# wolfram = WolframAlphaAPIWrapper()
search = GoogleSearchAPIWrapper()

def get_answer(query:str):
    x = graph_chain.run(query)
    
    ans = formatting_graph_response_chain.run({'query' : query , 'response' : x})
    print('*********************************************************\n', ans, '\n\n\n')
    return ans


task_tools = [
    # Tool(
    # name="Google Search",  
    # description="Use when the user wants to search something on web instead of relying on database. Use it when user insists on searching something on web.", 
    # func=search.run,  
    # return_direct=False, 
    # handle_tool_error=True,  
    # ),
    Tool(
    name = "All purpose tool" , 
    description='''The tool accepts a natural language query regarding companies, job roles, skills, etc. 
    
    ''',
    func = get_answer,
    # func = graph_chain.run,
    return_direct = True, 
    handle_tool_error=True,
    ),
]