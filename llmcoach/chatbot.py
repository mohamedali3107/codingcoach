import os
import openai
import gradio as gr
from dotenv import load_dotenv
from colorama import Fore, Back, Style

# load values from the .env file if it exists
load_dotenv()

# configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

INSTRUCTIONS = """
You are an AI assistant proficient in programming languages and Git. Your task is to help student to reslove their problems and to provide an educational response to all {new_question} given by a student. Always answer in written language by the student.  If a question is unclear, respond by stating, "Your question is not clear; can you provide more details to assist you?" Otherwise, strive to provide the most helpful answer. Always include all steps, along with explicit commands separately that students can use to resolve identified errors in the simplest manner. Try to provide all details in your answers.
Chat History:
{previous_questions_and_answers}
Follow Up Input: {new_question}
Helpful Answer:
"""
TEMPERATURE = 0
MAX_TOKENS = 600
FREQUENCY_PENALTY = 0.1
PRESENCE_PENALTY = 0.6
#limits how many questions we include in the prompt
MAX_CONTEXT_QUESTIONS = 30

def get_response(instructions, previous_questions_and_answers, new_question):
    """Get a response from ChatCompletion

    Args:
        instructions: The instructions for the chat bot - this determines how it will behave
        previous_questions_and_answers: Chat history
        new_question: The new question to ask the bot

    Returns:
        The response text
    """
    # build the messages
    messages = [
        { "role": "system", "content": instructions },
    ]
    # add the previous questions and answers
    for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })
    # add the new question
    messages.append({ "role": "user", "content": new_question })

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=1,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
    )
    response = completion.choices[0].message["content"]

    return response

# def main():
#     os.system("cls" if os.name == "nt" else "clear")
# #    # keep track of previous questions and answers
#     previous_questions_and_answers = []
#     while True:
#     #    ask the user for their question
#         new_question = input(
#             Fore.GREEN + Style.BRIGHT + "What can I get you?: " + Style.RESET_ALL

#         )      
#         response = get_response(INSTRUCTIONS, previous_questions_and_answers, new_question)
#         # add the new question and answer to the list of previous questions and answers
#         previous_questions_and_answers.append((new_question, response))

#         # print the response
#         print(Fore.CYAN + Style.BRIGHT + "Here you go: " + Style.NORMAL + str(response))


# if __name__ == "__main__":
#   main()

previous_questions_and_answers = []
def main(new_question, previous_questions_and_answers):
    # Récupérez la réponse à la nouvelle question
    response = get_response(INSTRUCTIONS, previous_questions_and_answers, new_question)
    # Gardez une trace de la nouvelle question et de la réponse
    updated_previous_questions_and_answers = previous_questions_and_answers + [(new_question, response)]
    # Construisez la discussion complète mise à jour
    #full_chat = "\n".join([f"Q: {q}\nA: {a}" for q, a in updated_previous_questions_and_answers])
    return response

# Créez une interface Gradio pour le chatbot
chatbot_interface = gr.ChatInterface(
    fn=main,
    chatbot=gr.Chatbot(
        height=300,
    ),
    textbox=gr.Textbox(placeholder="Posez-moi une question", container=False, scale=7),
    theme="soft",
    examples=["Hello", "Am I cool?"],
    cache_examples=True,
    retry_btn=None,
    undo_btn="Delete Previous",
    title="Coding_Coach",
    description="Bonjour, je suis votre Coding_Coach."
)

chatbot_interface.launch()