from langchain.prompts import PromptTemplate
import os, sys
sys.path.append(os.getcwd())
from parsers import *


summary_template= ''''
Write a summary of the following text in bulleted points: 
Format Instructions:
{format_instructions}

Query : 
{query}

''' 
summary_prompt = PromptTemplate(
    input_variables=["query"],
    template=summary_template,
    partial_variables={"format_instructions": summary_parser.get_format_instructions()}
)



short_summary_template= ''''

Summarise the following text :

{text}
'''

short_summary_prompt = PromptTemplate(
    input_variables=["text"],
    template=short_summary_template,
)

title_template= ''''
Write a descriptive title of the following text in not more than 30 words:

Text: {text}
'''

title_prompt = PromptTemplate(
    input_variables=["text"],
    template=title_template,
)
#_________________________________________________________________________________________
formatting_template = '''

You are a smart and polite bot who is concerned regarding improving readibility.
You should not change the facts and meaning of the text and try arranging text under major headings and bulleted points if possible.


User Input: 

{text}

'''
formatting_prompt = PromptTemplate(
    input_variables=["text"],
    template=formatting_template,
)
#_________________________________________________________________________________________
formatting_graph_response_template = '''
You are a smart and polite bot who is concerned regarding improving readibility. You will be provided with user query 
and also the response from the graph database. The response from the graph database is not always in a readable format, may be in the form of a list of dictionaries.

- INSTRUCTIONS:
    - If the response is a list of dictionaries, try to convert it into a readable format, extracting the necessary information.
    - If the response is a string, try to arrange it in a readable format.

User Query:
{query}

Response from the graph database:
{response}

'''
formatting_graph_response_prompt = PromptTemplate(
    input_variables=["query" , "response"],
    template=formatting_graph_response_template,
)

#_________________________________________________________________________________________

page_content_creator_template = '''
You are provided with the job profile and tech stack needed for the job. You are required to create a page content for the job profile.
Just a continuous paragraph of text. 

Job Profile: {job_profile}

Tech Stack: {tech_stack}

Do not return a list of bullet points or lists or a dictionary.
Create a simple and informative page content for the job profile, in continuous text format.
Do not exceed 70 words.

Profile : 
'''

page_content_creator_prompt = PromptTemplate(
    input_variables=["job_profile" , "tech_stack"],
    template=page_content_creator_template,
)