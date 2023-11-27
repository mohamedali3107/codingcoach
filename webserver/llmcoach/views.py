from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from openai import ChatCompletion
import openai

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
        request.session.clear()
        #return render(request, 'chat.html', {'conversation': conversation}) 
        return render(request, 'llmcoach/index.html', {'conversation': conversation})
