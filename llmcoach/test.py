import openai
import gradio as gr
import os
import gradio as gr
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ["OPENAI_API_KEY"]
<<<<<<< HEAD
def generate_comment(code_error, chatbot_context):
    chatbot_context.append({
        "role": "user",
        "content": f"Your are a helpful chatbot that can assist students in their learning. Your job is to reslove the  error {code_error} given by the student. If the input is a code, make a complete code review for the code. Try to give an answer for any question or request given by the student.",
    })
    
    retries = 3
    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=chatbot_context
            )
            break
        except Exception as e:
            if attempt == retries - 1:
                print(f"Attempt: {attempt}, Retries: {retries}")
                raise e
            else:
                print("OpenAI error occurred. Retrying...")
                continue

    comment = response.choices[0].message['content']

    chatbot_context = [
        {"role": "user", "content": f"Your are a helpful chatbot that can assist students in their learning. Your job is to reslove the  error {code_error} given by the student. If the input is a code, make a complete code review for the code. Try to give an answer for any question or request given by the student. "},
        {"role": "assistant", "content": comment},
    ]

    return comment, chatbot_context

def gradio_interface(input_data, chatbot_context):
    # The input_data argument will contain the user's input
    comment, chatbot_context = generate_comment(input_data, [])

    return comment

gr.ChatInterface(
    fn=gradio_interface,
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="Ask me a question", container=False, scale=7),
    theme="soft",
    examples=["Hello", "Am I cool?"],
    cache_examples=True,
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear",
    title="Coding_Coach",
    description="Hello, I am your Coding_Coach.",
).launch()

#gr.ChatInterface(gradio_interface).launch()
=======
 
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

>>>>>>> f2eaf3f1bf47d1c16db9d79fbfe8dad749b54144
