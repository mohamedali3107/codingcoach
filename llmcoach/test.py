import openai
import os
import gradio as gr
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ["OPENAI_API_KEY"]
 
def generate_comment(code_error, chatbot_context):
    # Use the OpenAI ChatGPT to generate a comment on the file changes

    chatbot_context.append(
      {
            "role": "user",
            "content": f"Make a code review of the changes made in this code: {code_error}",
       }
    )
    # Retry up to three times
    retries = 3
    for attempt in range(retries):
       try:
            #response = openai.Completion.create(
            #model="text-davinci-003",  # Utilise le moteur approprié pour les modèles de chat
            #prompt=f"Make a code review of the changes made in this code: {code}",
            #prompt= f"Try to reslove the following error {code_error}. If the input is not an error, say the input is not an error",
            #max_tokens=150,)  # Ajoutez d'autres paramètres si nécessaire
        

           response = openai.ChatCompletion.create(
                       model="gpt-3.5-turbo",
                       messages=chatbot_context)
    
              

       except Exception as e:
             if attempt == retries - 1:
                   print(f"attempt: {attempt}, retries: {retries}")
                   raise e  # Raise the error if reached maximum retries
             else:
                   print("OpenAI error occurred. Retrying...")
                   continue

    comment = response.choices[0]

    # Update the chatbot context with the latest response
    chatbot_context = [
       {
             "role": "user",
                   "content": f"Make a code review of the changes made in this code: {code_error}",
       },
       {
             "role": "assistant",
             "content": comment,
       }
    ]

    return comment

# Initialise le contexte du chatbot
chatbot_context = []

# Code pour lequel tu veux générer un commentaire
#code_error = """openai.error.InvalidRequestError: Unrecognized request argument supplied: messages
#"""
code_error=  """
def add_numbers(a, b):
    return a + b
"""
# Appelle la fonction generate_comment
comment= generate_comment(code_error,chatbot_context)

# Affiche le commentaire généré
print("Commentaire généré par le chatbot:")
print(comment)
# Affiche le contexte mis à jour du chatbot
print("\nContexte du chatbot mis à jour:")
print(chatbot_context)

