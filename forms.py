from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    RATING_CHOICES = [
        (5, '★'),
        (4, '★★'),
        (3, '★★★'),
        (2, '★★★★'),
        (1, '★★★★★')
    ]
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    
    class Meta:
        model = Feedback
        fields = ['rating']