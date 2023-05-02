from django.urls import path
from celebrityAIBotApp import views

app_name = 'celeb_ai'

urlpatterns = [ #list of url paths the app may need to go through
    path('', views.celebrity_ai_view, name='celeb_ai_view'), # creating a path to the page that needs to be displayed
]
