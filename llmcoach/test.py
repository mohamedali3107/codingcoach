import openai
import gradio as gr
import os
import gradio as gr
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ["OPENAI_API_KEY"]
def generate_comment(code_error, chatbot_context, request_student, Insert_History):
    
#Starting conversation
    chatbot_context.append({
        "role": "user",
        "content": f"Your Coding Coach is here to help! {request_student}",
    })
    chatbot_context.append({
    "role": "system",
    "content": "Context : You are a hight technical assistant that is managing students, students are doing a project using programming language , student do not have a huge backgorund with programming so you will have to be very explicit , you have to answer to all of their question "
})
# Adding previous conversation history if available
    chatbot_context.append({
    "role": "system",
    "content": "You have previously talked to the student. Here is your conversation so far: {Insert_History}"
})

# Adding new question from the student
    chatbot_context.append({
    "role": "user",
    "content": "Here is the new question I am asking you: {request_student}"
})

# Adding AI's response with a detailed explanation
    chatbot_context.append({
    "role": "system",
    "content": "Here is the answer to your question: [restated/summarized student question]. [Provide a detailed answer with clear and explicit explanations]. If there's anything you're unsure about, or if you have more questions, I'm here to help you out."
})

# Adding AI's response when more information is needed
    chatbot_context.append({
    "role": "system",
    "content": "To give you the most accurate answer, I need some more details about the problem you're facing. Can you describe the issue more explicitly, maybe share the code snippet that's causing the error, or provide more context? This will help me assist you better."
})

# Example of adding a task for code error resolution
    chatbot_context.append({
    "role": "user",
    "content": "Your job is to resolve the error {code_error} given by the student. If the input is a code, make a complete code review for the code. Try to give an answer for any question or request given by the student."
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


    # Update the chatbot history with the latest exchange
    chatbot_context.append({
        "role": "assistant",
        "content": comment,
    })

    return comment, chatbot_context, request_student, Insert_History

def gradio_interface(input_data, chatbot_context, request_student, Insert_History):
    # The input_data argument will contain the user's input
    comment, chatbot_context, request_student, Insert_History = generate_comment(input_data, [],[],[])

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