from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from notesManager.models import Note, NoteGroup


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
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


class GroupForm(forms.ModelForm):
    class Meta:
        model = NoteGroup
        fields = ("name",)

