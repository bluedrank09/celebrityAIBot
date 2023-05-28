# importing all the needed libraries
from django.shortcuts import render
from celebrityAIBotApp.forms import CelebrityQuestion
from llama_index import GPTSimpleVectorIndex, QuestionAnswerPrompt, StringIterableReader, GPTTreeIndex
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import datetime

# final_question = ""
now = datetime.datetime.now() # for logging - this wll give the exact date with m=day, month, year, hours, minutes, seconds


def celebrity_ai_view(request):
    try:
        listTickedCelebrities = [] # list that will contain the elements of the users question - who are they asking about and what the question was. 
                                #will later get converted into a string
        question_string = "" # initialising the string
        context = {}
        form = CelebrityQuestion(request.GET or None) # 
        context['form'] = form

        print(f"celebrity_ai_view has been invoked") # for debugging lol coding hates me 

        question_asked = None

        if request.method == 'GET' : # when the checkbox is clicked, the program knows this as the request method was "GET" - it is getting information
            print(f"---{request.GET.get('Ask')}---!")

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
            if firstCelebrityTicked: # checking if 
                listTickedCelebrities.append("Benedict Cumberbatch")

            if secondCelebrityTicked:
                listTickedCelebrities.append("Tom Hiddleston")

            if thirdCelebrityTicked:
                listTickedCelebrities.append("Scarlett Johannson")

            if fourthCelebrityTicked:
                listTickedCelebrities.append("Elizabeth Olsen")

            if fifthCelebrityTicked:
                listTickedCelebrities.append("Chris Hemsworth") 

            if len(listTickedCelebrities) == 0:
                context['answer'] = "Please select a celebrity to ask about"
            else:
                # making all of the items in that list into a string that can be used as the full query the user has given
                for item in listTickedCelebrities:
                    question_string += (f"{item} ")

                if request.GET.get('Who are they?') == "Who are they?":
                    question_asked = "Who are they"  

                elif request.GET.get('Are they well liked?') == "Are they well liked?":
                    question_asked = "Are they well liked"

                elif request.GET.get('How many movies are they in?') == "How many movies are they in?":
                    question_asked = "How many movies are they in"

                elif request.GET.get("Ask") == "Ask": #check for comparison if the user clicked the ask button
                    if len(question_asked.strip()) == 0:
                        question_asked = None
                        print(f"Text box was empty - it contained '{question_asked}'")
                        context['answer'] = "Please enter a question"
                    else:
                        print(f"Question asked contains [{question_asked}], length is {len(question_asked)}")
                        proper_question = check_for_real_question(question_asked)
                        if proper_question == "False":
                            question_asked = None
                            context['answer'] = "Please input a valid question"

                        if question_asked is not None:
                            print(f"-------CHECKFORCOMPARISONHERE-------") # debugging
                            print(f"!!!--- len of ticked celebrities = {len(listTickedCelebrities)} ---!!!") 
                            comparison = checkForComparison(question_asked) # calling the comparison function

                            if comparison == "True" and len(listTickedCelebrities) < 2: # using truthiness to check if it WAS a comparion but they only inputted one celebrity
                                print(f"-----ERROR THEY HAVE INPUTTED NOT ENOUGH AT {now:%c}-----")
                                print(f"-----SHOULD STOP THE PROGRAM-----")
                                question_asked = None
                                context['answer'] = "Sorry, for a comparison, please input two or more celebrities" # sending this as the answer in the answer box

                #listTickedCelebrities.append(question_asked) # getting the input form the question box and adding it to the query string
                question_string = f"{question_asked} {question_string}"
                print(f"FINAL QUESTION = {question_string}")

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

        get_api_key() # getting api key from azure keyvault- the functoin itself is right below this one
        
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

        print(f"About to use openAI") # debugging...lol

        response = index.query(final_question, text_qa_template = question_answer_prompt) # gets the response 

        print(f"Finished querying {now:%c}")

        return(response)
    
    except Exception as error: # raising error if there is one
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

        print(f"get_api_key has been invoked") # even more debugging

        openai_api_key = client.get_secret(secret_name).value # getting the api key in the secrets section of the azure key vault
        os.environ["OPENAI_API_KEY"] = openai_api_key # setting api key in the environment as an environemnt variable
    
    except Exception as error: # raising an error
        raise error
    
    finally:
        print(f":D")

def checkForComparison(question_asked): # checking for if the user put in a comparison question
    print(f"checkForComparison invoked")

    question_list = [] # creating a list for StringIterableReader to iterate through 
    question_list.append(question_asked) # appending the string with the celebrities and the question to the list

    print(f"-------calling api-------")
    apiKey = get_api_key() # getting the api key from the get_api_key function
    print(f"-------called API got API-------")

    documents = StringIterableReader().load_data(texts=question_list) # ierates through the lis
    print(f"-------done iteration-------")
    index = GPTTreeIndex.from_documents(documents) # creates an index file on the memory 
    print(f"-------indexing done-------")

    # getting openai to gcheck if its a comparison or not
    response = index.query("Is this question comparing two or more people ? return True if it is comparing two or more people and False if it is not comparing 2 or more people") 
    print(f"-------QUERIED-------") # debugging

    print(f"!!!!!!!-------THE RESPONSE IS [{response}]-------!!!!!!!") # you'll never guess what this is

    comparison_true = index.query("return the word True as an answer to this query")
    comparison_false = index.query("return the word False as an answer to this query")

    if response == comparison_true:
        print(f"Final answer is TRUE")
        comparisonAnswer = "True"
    else:
        print(f"Final response is FALSE")
        comparisonAnswer = "False"

    return(comparisonAnswer) # passing back the 0 ir 1 depending on if it was True or False


def check_for_real_question(question_asked): # checking for if the user put in a comparison question
    print(f"check_for_real_question invoked")

    question_list = [] # creating a list for StringIterableReader to iterate through 
    question_list.append(question_asked) # appending the string with the celebrities and the question to the list

    print(f"-------calling api-------")
    apiKey = get_api_key() # getting the api key from the get_api_key function
    print(f"-------called API got API-------")

    documents = StringIterableReader().load_data(texts=question_list) # ierates through the lis
    print(f"-------done iteration-------")
    index = GPTTreeIndex.from_documents(documents) # creates an index file on the memory 
    print(f"-------indexing done-------")

    # getting openai to gcheck if its a comparison or not
    response = index.query("Is this question a proper question ? return True if it is a proper question and False if it is not a proper question") 
    print(f"-------QUERIED-------") # debugging

    print(f"!!!!!!!-------THE RESPONSE IS [{response}]-------!!!!!!!") # you'll never guess what this is

    proper_question_true = index.query("return the word True as an answer to this query")
    print(f"response is {response} and proper_question_true is {proper_question_true}")

    if response == proper_question_true:
        print(f"Final answer is TRUE")
        properQuestionAnswer = "True"
    else:
        print(f"Final response is FALSE")
        properQuestionAnswer = "False"

    print(f"THE QUESTION ANSWER IS {properQuestionAnswer}")

    return(properQuestionAnswer) # passing back the 0 ir 1 depending on if it was True or False