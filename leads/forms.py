from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Lead, User, Agent, Category

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
            'description',
            'phone_number',
            'email',
        )

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', )
        field_classes = {'username': UsernameField}

class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    # override di __init__ per conoscere l'utente nella request e filtrare gli agenti associati
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        agents = Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields['agent'].queryset = agents # update del field agenti nel form

class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'category', 
            )

