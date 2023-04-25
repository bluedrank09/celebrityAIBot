from django.shortcuts import render
from celebrityAIBotApp.forms import CelebrityQuestion

def celebrity_ai_view(request):
    context = {}
    form = CelebrityQuestion(request.GET or None)
    context['form'] = form
    context['answer'] = "cool cool cool"

    return render(request, 'celebrity-ai.html', context)

def apology_message_view(request):
    context = None
    return render(request, 'apology-message.html', context)
