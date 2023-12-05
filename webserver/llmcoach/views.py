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
def CHAT(request):
    chat = request.session.get('chat', [])

    if request.method == 'POST':
        user_input = request.POST.get('user_input')

        # Define your chatbot's predefined prompts
        instructions =f"""You are an AI assistant proficient in programming languages. Your task is to help student to reslove their problems and to provide an educational response to all requests given by a student. Always answer in written language by the student.  If a question is unclear, respond by stating, "Your question is not clear; can you provide more details to assist you?" Otherwise, strive to provide the most helpful answer. Always include all steps, along with explicit commands separately that students can use to resolve identified errors in the simplest manner. Try to provide all details in your answers.
        Chat History:{chat}

        Follow Up Input: {user_input}
        Helpful Answer:"""
    
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
        request.session.clear()
        #return render(request, 'chat.html', {'conversation': conversation}) 
        return render(request, 'llmcoach/chatgpt.html', {'chat': chat})
    
def EVALUATION(request):
    conversation = request.session.get('conversation', [])

    if request.method == 'POST':
        user_input = request.POST.get('user_input')

        # Define your chatbot's predefined prompts
        instructions ="""Review the following code strictly and provide feedback. First check if the message of the user has the correct form of a code. If the message is not a code say "sorry i can't evalaute your input" .If it has the format of a code, please give a rating out of 10. Use the format 'Rating_out_of 10: ....Feedback:' in your response.\n\n{user_input}\n\nRating out of 10:" If the message is not in code format, please let me know.\n\n{user_input}\n\nFeedback:
        Chat History:{conversation}
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
        request.session.clear()
        #return render(request, 'chat.html', {'conversation': conversation}) 
        return render(request, 'llmcoach/code_evaluation.html', {'conversation': conversation})