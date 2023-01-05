from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from .forms import NewUserForm, NoteForm, GroupForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Note, NoteGroup


@login_required(login_url="/login")
def index(request):
    if request.method == "POST":
        note_id = request.POST.get("note-id")
        note = Note.objects.filter(id=note_id).first()
        if note and note.author == request.user:
            note.delete()
    notes = Note.objects.filter(author=request.user)
    return render(request, 'notesManager/main.html', {"notes": notes})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, 'registration/register.html', {'form': form})


@csrf_protect
@login_required(login_url="/login")
def create_note(request):
    if request.method == 'POST':
        m = request.POST.get("form_type")
        if request.POST.get("form_type") == 'formOne':
            form1 = NoteForm(request.user, request.POST)
            if form1.is_valid():
                note = form1.save(commit=False)
                note.author = request.user
                note.save()
                return redirect("/")
        else:
                form22 = GroupForm(request.POST)
                x = form22.is_valid()
                group_text = request.POST.get('gName')
                post = NoteGroup(name=group_text, author=request.user)
                post.save()

    form1 = NoteForm(author=request.user)
    form2 = GroupForm()
    return render(request, 'notesManager/create_note.html', {'form1': form1, 'form2': form2})

