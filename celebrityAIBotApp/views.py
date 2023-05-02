# importing all the needed libraries
from django.shortcuts import render
from celebrityAIBotApp.forms import CelebrityQuestion
from llama_index import GPTSimpleVectorIndex, QuestionAnswerPrompt
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import datetime

def celebrity_ai_view(request):
    try:
        listTickedCelebrities = [] # list that will contain the elements of the users question - who are they asking about and what the question was. will later get converted into a string
        question_string = "" # initialising the string
        context = {}
        form = CelebrityQuestion(request.GET or None)
        context['form'] = form

        print(f"celebrity_ai_view has been invoked") # for debugging lol coding hates me 

        if request.method == 'GET' : 
            firstCelebrityTicked = request.GET.get('first_celebrity')
            print(f"{firstCelebrityTicked}")

            secondCelebrityTicked = request.GET.get('second_celebrity')
            print(f"{secondCelebrityTicked}")

            thirdCelebrityTicked = request.GET.get('third_celebrity')
            print(f"{thirdCelebrityTicked}")

            fourthCelebrityTicked = request.GET.get('fourth_celebrity')
            print(f"{fourthCelebrityTicked}")

            fifthCelebrityTicked = request.GET.get('fifth_celebrity')
            print(f"{fifthCelebrityTicked}")

            question_asked = request.GET.get('celeb_question')
            print(f"{question_asked}")

            # all of these if conditions will add the actors name to the list of components for the query string if they have ben checked
            # if they have been, only their names will be given as part of the query string
            if firstCelebrityTicked:
                listTickedCelebrities.append("Benedict Cumberbatch")

            if secondCelebrityTicked:
                listTickedCelebrities.append("Tom Hiddleston")

            if thirdCelebrityTicked:
                listTickedCelebrities.append("Scarlett Johannson")

            if fourthCelebrityTicked:
                listTickedCelebrities.append("Elizabeth Olsen")

            if fifthCelebrityTicked:
                listTickedCelebrities.append("Chris Hemsworth")   

            listTickedCelebrities.append(question_asked)

            # making all of the items in that list into a string that can be used as the full query the user has given
            for item in listTickedCelebrities:
                question_string += (f"{item} ")

            print(f"{question_asked}") # also for debugging lol

            print(f"question_string contains {question_asked}")

            if question_asked is not None: # making sure the user has actually asked a question
                context['answer'] = get_response(question_string)
            
            return render(request, 'celebrity-ai.html', context)
        
    except Exception as error: # rasing an error and sending it to the console if there is one
        raise error

    finally:
        print(f":D") # printing a smile lol its my code calling card

def get_response(question_string): # function that goes and gets the answer to the users question
    try:
        prompt_template = "" # initialising prompt

        get_api_key() # getting api key from azure - the functoin itself is right below this one
        
        print(f"get_response has been invoked") # more debigging lol

        index = GPTSimpleVectorIndex.load_from_disk('data/actor_index.json') # using the json file thta was created by get_index_file.py that has all th celebrity information

        prompt_template = ( # generalised prompt 
        "Hello, I have some context information for you:\n"
        "---------------------\n"
        "{context_str}"
        "\n---------------------\n"
        "Based on this context, could you please help me understand the answer to this question: {query_str}?\n"
        )


        question_answer_prompt = QuestionAnswerPrompt(prompt_template) # making the 
        final_question = f"{question_string}"

        print(f"About to use openAI")
        
        response = index.query(final_question, text_qa_template = question_answer_prompt)

        #print(f"Finished querying {now:%c}")

        return(response)
    
    except Exception as error:
        raise error
    
    finally:
        print(f":D")

def get_api_key(): # getting th api key from my azure key vault
    try:
        kv_uri = "https://kv-celeb-ai-chatbot.vault.azure.net/" # my keyvault on azure
        kv_name = "kv-celeb-ai-chatbot" # name of the keyvault
        secret_name = "OPENAI-API-KEY"
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=kv_uri, credential=credential)

        print(f"get_api_key has been invoked")

        openai_api_key = client.get_secret(secret_name).value
        os.environ["OPENAI_API_KEY"] = openai_api_key # setting api key in the environment as an environemnt variable
    
    except Exception as error:
        raise error
    
    finally:
        print(f":D")

