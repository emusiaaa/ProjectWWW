from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from notesManager.models import Note, NoteGroup


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def username_clean(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError('User Already Exist')
        return username

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError(" Email Already Exist")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ("title", "group", "content")

    def __init__(self, author=None, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        if author:
            self.fields['group'].queryset = NoteGroup.objects.filter(author=author)
            self.fields['group'].required = False


class GroupForm(forms.ModelForm):
    class Meta:
        model = NoteGroup
        fields = ("name",)

