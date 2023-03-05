from django import forms

class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    # def clean(self):
    #     # Fill the password field so model validation won't complain about it
    #     # being blank. We'll set it with the real value below.
    #     self.instance.password = UNUSABLE_PASSWORD
    #     super(UserCreationForm, self).clean()