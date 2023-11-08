from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from langchain.prompts.chat import SystemMessage, HumanMessagePromptTemplate
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.document_loaders import UnstructuredFileLoader
from unstructured.cleaners.core import clean_extra_whitespace
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import csv 
import openai
import gradio as gr
import sys
import os
import langchain
import mysql.connector
from langchain.chains import create_sql_query_chain
#from langchain import OpenAI, SQLDatabase
from langchain.utilities.sql_database import SQLDatabase
from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI
from langchain_experimental.sql import SQLDatabaseChain
from transformers import pipeline
from dotenv import load_dotenv, find_dotenv
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Qdrant
import getpass
from dotenv import load_dotenv, find_dotenv
import environ
env = environ.Env()
environ.Env.read_env()

_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ["OPENAI_API_KEY"]

#username = "postgres" 
#password = env('DBPASS')
#password = getpass.getpass("Enter your MySQL password: ")
password=env("PASSWORD")
host = "localhost" 
#port = "5432"
port= "3306"
mydatabase =env('DATABASE')
#username="localhost"
user= "root" 
#pg_uri = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{mydatabase}"
mysql_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{mydatabase}"


#db = SQLDatabase.from_uri(pg_uri,sample_rows_in_table_info=9)# we include only one table to save tokens in the prompt :)
db = SQLDatabase.from_uri(mysql_uri,sample_rows_in_table_info=9)

#mydb = mysql.connector.connect(
 #       host="localhost",
  ##     password=password,
    #)
#cursor = mydb.cursor()
# Créez une instance de moteur SQLAlchemy pour établir la connexion
engine = create_engine(mysql_uri)
#print(db.table_info)
# Créez une session SQLAlchemy pour exécuter des requêtes
Session = sessionmaker(bind=engine)
session = Session()
#query_sql = text("SELECT * FROM public.\"Cv_data\"")
#result= session.execute()
#session.execute(sql.create_candidates)
# Parcourez les résultats
#for row in result:
    #print(row)

# N'oubliez pas de fermer la session lorsque vous avez fini
#session.close()






# Load Cvs
documents = [] 
for file in os.listdir("Cv"):
   if file.endswith('.pdf'):
     pdf_path = './Cv/' + file
     loader = UnstructuredFileLoader(pdf_path,post_processors=[clean_extra_whitespace])
     documents.extend(loader.load())
     
#Préparez votre séparateur
     
#text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100, length_function=len)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
# Divisez vos documents en textes
texts = text_splitter.split_documents(documents)

#Embedding
embedding = OpenAIEmbeddings()
#VectorDB store
vectordb = Chroma.from_documents(texts, embedding)
 
vectordb.persist()
# Similarity Search query
def query_docs(query):
	#embedding_vector = OpenAIEmbeddings().embed_query(query)
	#print(f"embedding_vector.len: {len(embedding_vector)}")
 docs = vectordb.similarity_search_with_score(query, search_kwargs={"k": 1})
        
 return docs[0]
# LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
# initialize the models: Retreiver

retriever = vectordb.as_retriever(search_type="similarity_score_threshold", 
                          search_kwargs={"score_threshold": .5})
# Build prompt
template = """You are a smart assistant. Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
Give only short and concise answer in maximum three phrases.

{context}
Question: {question}
"""
PROMPT =PromptTemplate(
  input_variables=["context", "question"],
   template=template
)
chain_type_kwargs = {"prompt": PROMPT}

qa= RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents = False,
    chain_type_kwargs=chain_type_kwargs,
)

#db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
#chain = create_sql_query_chain(ChatOpenAI(temperature=0), db)
# Create db chain
QUERY = """
Given an input question, first create a syntactically correct postgresql query to run, then look at the results of the query and return the answer.
Use the following format:
Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here:

{question}
"""

TEMPLATE = """
You are a {dialect} expert. Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results using the LIMIT clause as per {dialect}. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use date('now') function to get the current date, if the question involves "today".
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the following tables:

{table_info}

If someone asks for the art table, they really mean the artworks table.

Only single quotes in the SQLQuery.

Question: {input}"""

PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "dialect"], template=TEMPLATE)

# Revert to db without custom_table_info
# Could overflow context window (max prompt+completion length) of 4097
#db = SQLDatabase.from_uri(RDS_URI)

db_chain = SQLDatabaseChain.from_llm(
    llm,
    db,
    prompt=PROMPT,
    verbose=True,
    use_query_checker=True,
    return_intermediate_steps=False,
    top_k=3)


def get_prompt():
    print("Type 'exit' to quit")

    while True:
        prompt = input("Enter a prompt: ")

        if prompt.lower() == 'exit':
            print('Exiting...')
            break
        else:
            try:
                question = QUERY.format(question=prompt)
                #question= prompt
                result=db_chain(question)
                print(result)
                
            except Exception as e:
                print(e)
#get_prompt()                
def QA(query): 
    return(qa({"query": query}),query_docs(query))
###############Qui
#print(get_prompt())
#print(db)
#print(db_chain.run("What is the phone number of Mohamed Ali"))
#chain = create_sql_query_chain(ChatOpenAI(temperature=0), db)
#response = chain.invoke({"question":"what is the name of LEO"})
#print(response)

#iface=  gr.Interface(fn=QA, inputs="text", outputs=['text', 'text'], title= 'QACHAIN') 
#iface.launch()
yellow = "\033[0;33m"
green = "\033[0;32m"
BLACK = "\033[0;30m"
RED = "\033[0;31m"
RESET = "\033[0m"

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")
    
    def respond(query, chat_history):
        print(query)
        print(chat_history)
        if chat_history:
          chat_history = [tuple(sublist) for sublist in chat_history]
          print(chat_history)
        result = qa({"query": query,"chat_history": chat_history})
        print(f"{RED}Answer: {result['result']}{RESET}")
        chat_history.append((query, result["result"]))
        print(chat_history)
        output_file = "QAV0.csv"
        with open(output_file, mode='w', newline='') as file:
           writer = csv.writer(file)
           writer.writerow(["Question", "Réponse","Source & score"])
           writer.writerow([query, result,query_docs(query)])
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot], queue=False)
    clear.click(lambda: None, None, chatbot, queue=False)
    

#demo.launch(debug=True, share=False)
###################################################################################

#LlamaIndex vs Langchain
from llama_index.evaluation import DatasetGenerator
from llama_index import SimpleDirectoryReader
from llama_index import (SimpleDirectoryReader, 
                         ServiceContext, 
                         LLMPredictor, 
                         VectorStoreIndex,
                         TreeIndex,
                         GPTVectorStoreIndex, 
                         load_index_from_storage, 
                         StorageContext)

from pathlib import Path
from llama_index import download_loader
from llama_index import SimpleDirectoryReader
from llama_hub.file.unstructured import UnstructuredReader

#UnstructuredReader = download_loader("UnstructuredReader")
#loader = UnstructuredReader()
#base_directory = 'data_template'
#filename = '.DS_Store'
#file_path = os.path.join(base_directory, filename)

#if os.path.exists(file_path):
 #   os.remove(file_path)
  #  print(f"Le fichier {file_path} a été supprimé avec succès.")
#else:
 #   print(f"Le fichier {file_path} n'existe pas dans le répertoire {base_directory}.")
#documents = []
#for filename in os.listdir(base_directory):
 #   full_path = os.path.join(base_directory, filename)
  #  if os.path.isfile(full_path):
   ###   documents.extend(loader.load_data(file=full_path))
#print(documents)
#UnstructuredReader = download_loader('UnstructuredReader')

#dir_reader = SimpleDirectoryReader('Cv', file_extractor={
 # ".pdf": UnstructuredReader(),
#})
#documents = dir_reader.load_data()

#documents = [] 
#for file in os.listdir("Cv"):
 #  if file.endswith('.pdf'):
  ####documents.extend(loader.load())
     
#documents = loader.load_data()
#load data
#######Question Generation 
documents = SimpleDirectoryReader('data_template').load_data()
#documents= loader.load_data(file=)
# build service context
llm_predictor = LLMPredictor(llm=llm)
service_context = ServiceContext.from_defaults(
    llm_predictor=llm_predictor)

# Generate Question
data_generator = DatasetGenerator.from_documents(documents)
question = data_generator.generate_questions_from_nodes()
#print(question)
######Generate Answers/Source Nodes (Context)
# Create Index
index = GPTVectorStoreIndex.from_documents(documents)
# New indesx
#new_index=TreeIndex.from_documents(documents)
# save index to disk
index.set_index_id("vector_index")
index.storage_context.persist('storage')

# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir='storage')
# load index
index = load_index_from_storage(storage_context, index_id="vector_index")

# Query the index
query_engine = index.as_query_engine(similarity_top_k=3,service_context=service_context)
#####
#query_engine = index.as_query_engine()
responses = []  # Initialisation d'une liste pour stocker les réponses

for index, une_question in enumerate(question):
    # Utilisez 'index' pour suivre l'indice de la question
    # et 'une_question' pour accéder à la question
    response = query_engine.query(une_question)
    responses.append(response)
    print(f"Question {index + 1}: {une_question}")
    print(f"Réponse {index + 1}: {response}")


#for une_question in question:
 #   response = query_engine.query(une_question)
  #  responses.append(response)
   

# La liste 'responses' contient maintenant les réponses pour chaque question
while True:
        question = input("Enter a query: ")

        if question.lower() == 'exit':
            print('Exiting...')
            break
        else:
            try:
                #question = QUERY.format(question=prompt)
            
                result=query_engine.query(question)
                print(result)
                
            except Exception as e:
                print(e)
#query= input("question:")
#response = query_engine.query([for une_question in question])
#print(response)

###############Evaluation
#from llama_index.evaluation import ResponseEvaluator, QueryResponseEvaluator
#from llama_index import VectorStoreIndex
# define evaluator
#evaluator = ResponseEvaluator(service_context=service_context)
# define evaluator
#evaluator = QueryResponseEvaluator(service_context=service_context)
# evaluate using the response object
#response = query_engine.query(question[0])



# Exécutez la requête pour obtenir la réponse
#response = query_engine.query("What is the phone number of Leo")

# Définissez la requête et les contextes comme une liste de documents
#query = "What is the phone number of Leo"

# Remplacez 'context_text' par le texte de chaque contexte
#context=[]
# Évaluez la réponse en fournissant la requête et les contextes
#eval_result = evaluator.evaluate(query=question[0],response=response)

#print(eval_result)

#############################################################
# Using LlamaIndex as a memory module
