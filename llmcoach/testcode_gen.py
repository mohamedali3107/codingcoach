import openai
import gradio as gr
import os
<<<<<<< HEAD
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read the local .env file

openai.api_key = os.environ["OPENAI_API_KEY"]

def generate_comment(request_student, context):
    context.append({
        "role": "user",
        "content": f"Your Coding Coach is here to help! {request_student}",
    })

=======
import gradio as gr
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ["OPENAI_API_KEY"]
def generate_comment(code_error, chatbot_context):
    chatbot_context.append({
        "role": "user",
        "content": f"Your are a helpful chatbot that can assist students in their learning. Your job is to reslove the  error {code_error} given by the student. If the input is a code, make a complete code review for the code. Try to give an answer for any question or request given by the student.",
    })
    
>>>>>>> f2eaf3f1bf47d1c16db9d79fbfe8dad749b54144
    retries = 3
    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
<<<<<<< HEAD
                messages=context
=======
                messages=chatbot_context
>>>>>>> f2eaf3f1bf47d1c16db9d79fbfe8dad749b54144
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
<<<<<<< HEAD
        {"role": "user", "content": f"Your Coding Coach is here to help! {request_student}"},
        {"role": "assistant", "content": comment},
    ]

    return comment, context

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

=======
        {"role": "user", "content": f"Your are a helpful chatbot that can assist students in their learning. Your job is to reslove the  error {code_error} given by the student. If the input is a code, make a complete code review for the code. Try to give an answer for any question or request given by the student. "},
        {"role": "assistant", "content": comment},
    ]

    return comment, chatbot_context

def gradio_interface(Request_student):
    comment, chatbot_context = generate_comment(Request_student, [])

    return comment

iface = gr.Interface(
    fn=gradio_interface,
    inputs="text",
    outputs="text",
    live=True,
    title="Coding_Coach",
    description="Hello, I am your Coding_Coach.",
)

iface.launch()
>>>>>>> f2eaf3f1bf47d1c16db9d79fbfe8dad749b54144
