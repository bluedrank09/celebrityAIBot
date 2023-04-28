from django.shortcuts import render
from celebrityAIBotApp.forms import CelebrityQuestion

def celebrity_ai_view(request):
    listTickedCelebrities = []
    context = {}
    form = CelebrityQuestion(request.GET or None)
    context['form'] = form

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

        context['answer'] = listTickedCelebrities
        
    return render(request, 'celebrity-ai.html', context)

def apology_message_view(request):
    context = None
    return render(request, 'apology-message.html', context)


