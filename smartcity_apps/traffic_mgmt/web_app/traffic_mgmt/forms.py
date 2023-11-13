from django import forms

from . import models

class LoginForm(forms.Form):
    email = forms.CharField(label="Email", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    about = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    
    class Meta:
        model = models.User
        fields = ['email', 'password', 'name']
        labels = {
            'name': 'Name',
            'email': 'Email',
            'password': 'Password',
        }


class RoutePlanningForm(forms.ModelForm):
    class Meta:
        model = models.EmergencyCall
        fields = ['caller_name', 'caller_contact', 'location', 'emergency_service']
    
    def __init__(self, *args, **kwargs):
        super(RoutePlanningForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ServerlessAppForm(forms.ModelForm):
    class Meta:
        model = models.ServerlessApp
        fields = ['name', 'description', 'access_url', 'docker_image', 'status']
    
    def __init__(self, *args, **kwargs):
        super(ServerlessAppForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'