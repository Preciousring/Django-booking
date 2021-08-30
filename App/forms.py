from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Booking, Resource

REUNION = 'RE'
VISIO = 'VI'
ROOM_CHOICES = [
    (REUNION, 'Salle de réunion'),
    (VISIO, 'Salle de visioconférence'),

]
FORM_CLASS = 'form-control rounded-left'


class BookingForm(forms.ModelForm):
    title = forms.CharField(label='Titre', widget=forms.TextInput(attrs={'class': FORM_CLASS,
                                                                         'placeholder': 'Titre'}))
    start_date = forms.DateTimeField(label='Date de début', widget=forms.DateTimeInput(attrs=
                                                                                       {'class': FORM_CLASS,
                                                                                        'placeholder': 'Date de début'}
                                                                                       ))
    end_date = forms.DateTimeField(label='Date de fin', widget=forms.DateTimeInput(attrs=
                                                                                   {'class': FORM_CLASS,
                                                                                    'placeholder': 'Date de fin'}))
    resource = forms.ModelChoiceField(queryset=Resource.objects.all(), widget=forms.Select(attrs=
                                                                                           {'class': FORM_CLASS,
                                                                                            'placeholder': 'Ressource'}
                                                                                           ))

    class Meta:
        model = Booking
        fields = ['title', 'start_date', 'end_date', 'resource']


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True, 'class': FORM_CLASS,
                                                             'placeholder': 'Pseudonyme'}))
    password = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={'class': FORM_CLASS,
                                                                              'placeholder': 'Mot de passe'})
                               )
