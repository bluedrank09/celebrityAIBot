from django.urls import path
from celebrityAIBotApp import views

app_name = 'celeb_ai'

urlpatterns = [
    path('', views.celebrity_ai_view, name='celeb_ai_view'),   
    path('apology', views.apology_message_view, name='apology_message_view'),
]
