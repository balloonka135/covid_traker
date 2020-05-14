from django import forms


# uniform form for user creation
class UserCreateForm(forms.Form):
    email = forms.EmailField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=40)
    name = forms.CharField(max_length=100)
    occupation = forms.CharField(max_length=40)
    status = forms.CharField(max_length=20)
