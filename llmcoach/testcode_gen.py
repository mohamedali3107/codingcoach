import openai
import gradio as gr
import os
import gradio as gr
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ["OPENAI_API_KEY"]
def generate_comment(code_error, chatbot_context):
    chatbot_context.append({
        "role": "user",
        "content": f"Try to reslove the following error {code_error}. If the input is not an error, say the input is not an error",
    })
    
    retries = 3
    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=chatbot_context
            )
        except Exception as e:
            if attempt == retries - 1:
                print(f"Attempt: {attempt}, Retries: {retries}")
                raise e
            else:
                print("OpenAI error occurred. Retrying...")
                continue

    comment = response.choices[0].message['content']

    chatbot_context = [
        {"role": "user", "content": f"Try to reslove the following error {code_error}. If the input is not an error, say the input is not an error"},
        {"role": "assistant", "content": comment},
    ]

    return comment, chatbot_context

def gradio_interface(code_error):
    comment, chatbot_context = generate_comment(code_error, [])

    return comment

iface = gr.Interface(
    fn=gradio_interface,
    inputs="text",
    outputs="text",
    live=True,
    title="Code Review Chatbot",
    description="Enter an error of your code , and the chatbot will generate a suggestion solution.",
)

iface.launch()