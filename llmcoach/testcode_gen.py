import openai
import gradio as gr
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read the local .env file

openai.api_key = os.environ["OPENAI_API_KEY"]


def generate_comment(request_student, context):
    context.append({
        "role": "user",
        "content": f"Your Coding Coach is here to help! {request_student}",
    })

    retries = 3
    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=context
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




