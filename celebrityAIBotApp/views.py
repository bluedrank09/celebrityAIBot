from django.shortcuts import render
from celebrityAIBotApp.forms import CelebrityQuestion
from llama_index import GPTSimpleVectorIndex, QuestionAnswerPrompt
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def celebrity_ai_view(request):
    listTickedCelebrities = []
    question_string = ""
    context = {}
    form = CelebrityQuestion(request.GET or None)
    context['form'] = form

    print(f"celebrity_ai_view has been invoked")

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

        for item in listTickedCelebrities:
            question_string += (f"{item} ")

        print(f"{question_asked}")

        print(f"question_string contains {question_asked}")

        if question_asked is not None:
            context['answer'] = get_response(question_string)
        
    return render(request, 'celebrity-ai.html', context)

def apology_message_view(request):
    context = None
    return render(request, 'apology-message.html', context)

def get_response(question_string):
    prompt_template = ""

    get_api_key()
    
    print(f"get_response has been invoked")

    index = GPTSimpleVectorIndex.load_from_disk('data/actor_index.json')

    prompt_template = (
    "Hello, I have some context information for you:\n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Based on this context, could you please help me understand the answer to this question: {query_str}?\n"
    )


    question_answer_prompt = QuestionAnswerPrompt(prompt_template)
    final_question = f"{question_string}"

    response = index.query(final_question, text_qa_template = question_answer_prompt)

    return(response)

def get_api_key():
    kv_uri = "https://kv-celeb-ai-chatbot.vault.azure.net/"
    kv_name = "kv-celeb-ai-chatbot" # name of the keyvault
    secret_name = "OPENAI-API-KEY"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=kv_uri, credential=credential)

    print(f"get_api_key has been invoked")

    openai_api_key = client.get_secret(secret_name).value
    os.environ["OPENAI_API_KEY"] = openai_api_key # setting api key in the environment as an environemnt variable


