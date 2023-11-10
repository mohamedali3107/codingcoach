import os
import openai
import gradio as gr
from dotenv import load_dotenv
from colorama import Fore, Back, Style

# load values from the .env file if it exists
load_dotenv()

# configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

INSTRUCTIONS = """You are an AI assistant that is an expert in programming languages. Your task is to help student to reslove their problems and to give a precise answer to all {new_question} given by a student.
"""
TEMPERATURE = 0
MAX_TOKENS = 500
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
#limits how many questions we include in the prompt
MAX_CONTEXT_QUESTIONS = 10

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
        model="gpt-4",
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=1,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
    )
    response = completion.choices[0].message.content
    return response

def main():
    os.system("cls" if os.name == "nt" else "clear")
#    # keep track of previous questions and answers
    previous_questions_and_answers = []
    while True:
    #    ask the user for their question
        new_question = input(
            Fore.GREEN + Style.BRIGHT + "What can I get you?: " + Style.RESET_ALL

        )
#        
        response = get_response(INSTRUCTIONS, previous_questions_and_answers, new_question)
        # add the new question and answer to the list of previous questions and answers
        previous_questions_and_answers.append((new_question, response))

        # print the response
        print(Fore.CYAN + Style.BRIGHT + "Here you go: " + Style.NORMAL + str(response))


if __name__ == "__main__":
  main()


