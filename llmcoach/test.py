import openai
import os
import chatgpt
import gradio as gr
from dotenv import load_dotenv, find_dotenv
import environ
env = environ.Env()
environ.Env.read_env()

_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ["OPENAI_API_KEY"]


class CorrecteurDeCode:
    def __init__(self, openai_api_key="OPENAI_API_KEY"):
        self.openai_api_key = openai_api_key
        self.model = OpenAI(openai_api_key)

    def correcteur_code(self, code):
        # Analyse du code et identification des erreurs
        # Vous pouvez utiliser des bibliothèques comme `flake8` ou `pycodestyle` pour cela
        # Pour cet exemple, nous utilizerons une fonction simple
        errors = ["Erreur 1", "Erreur 2", "Erreur 3"]
        erreurs_code = [i for i in range(len(code)) for j in range(3) for k in range(i + j + 1) if k >= i and k <= len(code) and code[k - i - j - 1] == code[i - 1] and code[k - i - j - 2] == code[j - 1]]
        if len(erreurs_code) > 0:
            return errors[0], errors[1], errors[2]
        else:
            return "Aucune erreur trouvée", "Aucune erreur trouvée", "Aucune erreur trouvée"



def suggestions(code):
    # Générez des suggestions de code à partir des erreurs identifiées
    # Vous pouvez utiliser des bibliothèques comme `autopep8` ou `black` pour cela
    # Pour cet exemple, nous utiliserons une fonction simple
    suggestions = ["Suggestion 1", "Suggestion 2", "Suggestion 3"]
    suggestion_code = [i for i in range(len(code)) for j in range(3) for k in range(i + j + 1) if k >= i and k <= len(code) and code[k - i - j - 1] == code[i - 1] and code[k - i - j - 2] == code[j - 1]]

    if len(suggestion_code) > 0:
        return suggestions[0], suggestions[1], suggestions[2]
    else:
        return "Aucune suggestion trouvée", "Aucune suggestion trouvée", "Aucune suggestion trouvée"
def main():
    # Create the Gradio interface
    app = gr.Interface(
        fn=CorrecteurDeCode,
        inputs=gr.inputs.Textbox(label="Code Python", name="code"),
        outputs=["text", "text"]
    )

    # Add a text input for suggestions
    app.add_input("text", label="Suggestions", name="suggestions")

    # Launch the user interface
    app.launch()

if __name__ == "__main__":
    main()