from django.shortcuts import render

# Create your views here.

def celebrity_ai_view(request):
    context = None
    return render(request, 'celebrity-ai.html', context)
