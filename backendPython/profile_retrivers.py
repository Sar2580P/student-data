import os, sys, json
from langchain_community.vectorstores import chroma
sys.path.append(os.getcwd())
from langchain.retrievers import ContextualCompressionRetriever
from utils import *
from langchain.retrievers.document_compressors import LLMChainFilter
from langchain.schema import Document
db_path = 'backendPython/profile_database\info_db'
db = chroma.Chroma(embedding_function = embedder, persist_directory= db_path)


_filter = LLMChainFilter.from_llm(llm)
retriever = db.as_retriever(search_kwargs={"k": 5}, return_source_documents=True)
print(retriever.get_relevant_documents('job_profile :  Software Engineer '))
compression_retriever = ContextualCompressionRetriever(base_compressor=_filter, base_retriever=retriever)

#__________________________________________________________________________________________________

def get_profiles(query: str, skill_query =  ['Python', 'SQL', 'R']):
    results:List[Document] = compression_retriever.get_relevant_documents(query)
    general_suggestions_idxs = set()
    order = 0
    print(results)
    companies_info = {}
    for i ,doc in enumerate(results):
        skills = doc.metadata['Skills'].split(',')
        j , k = 0, 0
        x = True
        while j <len(skill_query):
            if k >= len(skills):
                general_suggestions_idxs.add(i)
                x = False
                break
            elif skill_query[j] == skills[k]:
                j+=1
            k+=1
        if x:
            companies_info.append(doc.metadata)
    for i in general_suggestions_idxs:
        companies_info[order] = results[i].metadata
        order+=1
            
    return json.dumps(companies_info)

# print(get_profiles('Job Profile available is : Research Engineer \n\nTech Stack needed for the job : Python, R, SQL, Machine Learning, Deep Learning, Cloud Computing, Data Visualization, Statistics'))
# print(get_profiles('Digital Consultants'))
# print(get_profiles('Tech stack : Python, Deep Learning , SQL'))

# import pickle
# f = pickle.load(open('backendPython\profile_database\skill_set.pkl', 'rb'))
# print(f)