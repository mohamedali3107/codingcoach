from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from openai import ChatCompletion
import openai
from django.contrib.auth.decorators import login_required , user_passes_test


@login_required(login_url="/login")
def home(request):
    conversation = request.session.get('conversation', [])

    if request.method == 'POST':
        user_input = request.POST.get('user_input')

        # Define your chatbot's predefined prompts
        instructions ="""You are a helpful GIT ASSISTANT. Your role involves assisting students in overcoming challenges encountered while working with GIT, offering educational responses. Ensure that each response includes the relevant GIT commands and corresponding code to enhance the students understanding. Always answer in written language by the student.  If a question is unclear, respond by stating, "Your question is not clear; can you provide more details to assist you?" Otherwise, strive to provide the most helpful answer. Always include all steps, along with explicit commands separately that students can use to resolve identified errors in the simplest manner. Try to provide all details in your answers.
        Chat History:
        Follow Up Input: {conversation}
        Helpful Answer:"""
    
    # build the messages
        prompts = [
        {"role": "system", "content": instructions},
       ]


        # Append user input to the conversation
        if user_input:
            conversation.append({"role": "user", "content": user_input})

        # Append conversation messages to prompts
        prompts.extend(conversation)

        # Set up and invoke the ChatGPT model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompts,
            api_key="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"
        )
        
        # Extract chatbot replies from the response

        chatbot_replies = [message['message']['content'] for message in response['choices'] if message['message']['role'] == 'assistant']

        # Append chatbot replies to the conversation
        for reply in chatbot_replies:
            conversation.append({"role": "assistant", "content": reply})

        # Update the conversation in the session
        request.session['conversation'] = conversation

        return render(request, 'llmcoach/index.html', {'user_input': user_input, 'chatbot_replies': chatbot_replies, 'conversation': conversation})
    else:
        #request.session.clear()
        #return render(request, 'chat.html', {'conversation': conversation}) 
        return render(request, 'llmcoach/index.html', {'conversation': conversation})

@login_required(login_url="/login")
def CHAT(request):
    chat = request.session.get('chat', [])

    if request.method == 'POST':
        user_input = request.POST.get('user_input')

        # Define your chatbot's predefined prompts
        instructions =f"""You are a helpful CODE REVIEW ASSISTANT. Your role involves reviewing and providing constructive feedback on code snippets submitted by students. Generate insightful questions that encourage students to think critically about their code and address potential issues. Ensure your questions prompt the student to consider best practices, efficiency, and potential improvements.
        Chat History:
        Follow Up Input: {chat}
        Code Review Questions:"""
    
    # build the messages
        prompts = [
        {"role": "system", "content": instructions},
       ]


        # Append user input to the conversation
        if user_input:
            chat.append({"role": "user", "content": user_input})

        # Append conversation messages to prompts
        prompts.extend(chat)

        # Set up and invoke the ChatGPT model
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=prompts,
            api_key="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"
        )
        
        # Extract chatbot replies from the response

        chatbot_replies = [message['message']['content'] for message in response['choices'] if message['message']['role'] == 'assistant']

        # Append chatbot replies to the conversation
        for reply in chatbot_replies:
            chat.append({"role": "assistant", "content": reply})

        # Update the conversation in the session
        request.session['chat'] = chat

        return render(request, 'llmcoach/chatgpt.html', {'user_input': user_input, 'chatbot_replies': chatbot_replies, 'chat': chat})
    else:
        # request.session.clear()
        #return render(request, 'chat.html', {'conversation': conversation}) 
        return render(request, 'llmcoach/chatgpt.html', {'chat': chat})

@login_required(login_url="/login")
def EVALUATION(request):
    conversation = request.session.get('conversation', [])

    if request.method == 'POST':
        user_input = request.POST.get('user_input')

        # Define your chatbot's predefined prompts
        instructions = """Review the following code rigorously and provide detailed feedback. First, check if the user's message has the correct format of a code. If the message is not code, say "sorry, I can't evaluate your input". If it is in the code format, please give a rating out of 10 and provide constructive feedback using the format 'Rating_out_of 10: ....Feedback:' in your response. Additionally, consider adding an annotation to the code if necessary.

Code Annotation: 
{code_annotation}

{user_input}

Rating out of 10:" If the message is not in code format, please let me know.

{user_input}

Feedback:
    - Code Structure: Evaluate the overall structure and organization of the code. [Teacher's Note: {code_structure_rating}]
    - Readability: Assess how easily the code can be read and understood. [Teacher's Note: {readability_rating}]
    - Efficiency: Consider the efficiency of the code in terms of time and space. [Teacher's Note: {efficiency_rating}]
    - Best Practices: Check if the code follows best practices and coding standards. [Teacher's Note: {best_practices_rating}]
    - Error Handling: Examine how well the code handles potential errors. [Teacher's Note: {error_handling_rating}]
    - Optimization: Suggest optimizations or improvements where applicable. [Teacher's Note: {optimization_rating}]

Chat History: {conversation}
Follow Up Input: {user_input}
Helpful Answer:"""

  
      # build the messages
        prompts = [
        {"role": "system", "content": instructions},
       ]


        # Append user input to the conversation
        if user_input:
            conversation.append({"role": "user", "content": user_input})

        # Append conversation messages to prompts
        prompts.extend(conversation)

        # Set up and invoke the ChatGPT model
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=prompts,
            api_key="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"
        )
        
        # Extract chatbot replies from the response

        chatbot_replies = [message['message']['content'] for message in response['choices'] if message['message']['role'] == 'assistant']
         # Check if the response indicates that the message is not in code format
        if any("not in code format" in reply.lower() for reply in chatbot_replies):
            conversation.append({"role": "user", "content": user_input})
            conversation.append({"role": "assistant", "content": "Your message is not in code format. I can't help you, sorry."})
            request.session['conversation'] = conversation
            return render(request, 'llmcoach/index.html', {
                'user_input': user_input,
                'chatbot_replies': ["Your message is not in code format. I can't help you, sorry."],
                'conversation': conversation
            })
        # Append chatbot replies to the conversation
        for reply in chatbot_replies:
            conversation.append({"role": "assistant", "content": reply})

        # Update the conversation in the session
        request.session['conversation'] = conversation

        return render(request, 'llmcoach/index.html', {'user_input': user_input, 'chatbot_replies': chatbot_replies, 'conversation': conversation})
    else:
        #request.session.clear()
        #return render(request, 'chat.html', {'conversation': conversation}) 
        return render(request, 'llmcoach/code_evaluation.html', {'conversation': conversation})