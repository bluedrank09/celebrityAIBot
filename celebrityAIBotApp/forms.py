from django import forms 

class CelebrityQuestion(forms.Form):
    first_celebrity = forms.BooleanField(label="Benedict Cumberbatch", required=False)
    second_celebrity = forms.BooleanField(label="Tom Hiddleston", required=False)
    third_celebrity = forms.BooleanField(label="Scarlett Johannson", required=False)
    fourth_celebrity = forms.BooleanField(label="Elizabeth Olsen", required=False)
    fifth_celebrity = forms.BooleanField(label="Chris Hemsworth", required=False)  
    celeb_question = forms.CharField(label="Ask your question here", max_length=1000, initial=' ', widget=forms.Textarea(attrs={'rows':3}))