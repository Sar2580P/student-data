from chromadb.api.types import Documents, Embeddings
from typing import List, Tuple
from langchain.docstore.document import Document
from newspaper import Article 
import requests
from langchain.vectorstores.chroma import Chroma
import sys
sys.path.append('backendPython/')
# from utils import Embedding
import pandas as pd
from chains import *
import ast
import pickle 
from llms import embedder

path = 'backendPython/neo4j\Placement data.xlsx'
df = pd.read_excel(path, sheet_name='2020-21')
values = {'Selected': df.iloc[:,2].mode() , 'CTC':df.iloc[:, 4].median() , 'CGPA':0}
df.fillna(value=values, inplace=True)
df = df.iloc[5:25, :]
cols = list(df.columns)

def get_about_company(url):
  title, article =  web_scraping(url)
  if article is None:
    return 'No article found'
  # try:
  #   return summarize_chain.invoke(article)
  # except:
  return article
  

skill_template = """
- Given the Job role, return the names of atmax 8 possible tech stacks needed for the job role. 
- Just return the of tech-stacks separated by commas.
- Don't put backticks(`) around the output.

Job Profile : {job_profile}

Skills :
"""
skill_prompt = PromptTemplate(
    input_variables=["job_profile"],
    template=skill_template,
)
skill_chain = LLMChain(llm=llm, prompt=skill_prompt,)

syntax_template = '''Given input is an output of previous llm chain, it was expected it return a 
list of strings , check that there are no parsing errors in the output.

It may be possible that the output may contain some syntax errors. Which can crash the execution of file when doing literal_eval on the output.
You need to check that there are no syntax errors in the output. Don't put backticks(`) in the output.

Code Snippet : 
{code}
'''

syntax_prompt = PromptTemplate(
    input_variables=["code"],
    template=syntax_template,
)
syntax_chain = LLMChain(llm=llm, prompt=syntax_prompt,)


def get_context(job_profile, syntax_err_ct): 
  skills = skill_chain.invoke(job_profile)   # return a string format dict
  try:
    tries = 0
    while tries<3:
      try :
        skills_ = syntax_chain.invoke({'code' : skills})  
        skills = ast.literal_eval(skills_)    # 1.) removing backticks , 2.) convert string to dict
        break
      except : 
        syntax_err_ct += 1
        tries+=1
  except:
    skills = {'job_profile': 'Software Engineer', 'text': 'Java, Python, C++, JavaScript, React, Node.js, SQL, Docker'}
  return skills, syntax_err_ct


def web_scraping(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
            }
    session = requests.Session()

    try:
      response = session.get(url, headers=headers, timeout=10)
    
      if response.status_code == 200:     # the request was successful
        article = Article(url)
        article.download()
        article.parse()
        
        print('All fetching successful!', end= '\n\n\n')
        return article.title, article.text
      else:
        print(f"Failed to fetch article at {url}")
    except Exception as e:
      print(f"Error occurred while fetching article at {url}: {e}") 
    
    return  None, None

vector_db = Chroma(embedding_function = embedder, persist_directory= 'backendPython/profile_database/info_db')
docs = []
skill_set = set()
import time
syntax_err_ct = 0
for index, row in df.iterrows():
  print(index , end = ' ')
  metadata = {}
  for col in cols:
    if col == 'About company':
      x = get_about_company(row[col])
      if type(x) == str:
        metadata[col] = x
      else : 
        metadata.update(x)
      
    else :   
      metadata[col] = row.loc[col]

  skill_dict, syntax_err_ct = get_context(metadata['JobProfile'], syntax_err_ct)
  
  
  # page_content = str(page_content_chain.invoke({'job_profile': metadata['JobProfile'], 'tech_stack': skill_dict['text']}))
  # page_content = ast.literal_eval(page_content)['text']
  page_content = f"Job Profile available is : {metadata['JobProfile']} \n\nTech Stack needed for the job : {skill_dict['text']}"
  print(page_content , '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
  skill_set.update(set(skill_dict['text']))
  metadata['Skills'] = skill_dict['text']
  # vector_db.add_texts(texts= list(page_content),metadatas=[metadata], persist_directory= 'backendPython/profile_database/info_db')
  doc= Document(page_content=page_content, metadata=metadata)
  print(doc , '\n\n\n')
  docs.append(doc)
  time.sleep(5)
  if index == 25:
    break

  
vector_db.add_documents(docs, persist_directory= 'backendPython/profile_database/info_db')
print('syntax_err_ct : ', syntax_err_ct)

pickle.dump(list(skill_set), open('backendPython/profile_database/skill_set.pkl', 'wb'))
# print(vector_db.similarity_search('python , nodejs'))