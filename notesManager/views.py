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
        # messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm()
    # args['form'] = form
    return render(request, 'registration/register.html', {'form': form})


@csrf_protect
@login_required(login_url="/login")
def create_note(request):
    if request.method == 'POST':
        # m = request.POST.get("form_type")
        if request.POST.get("form_type") == 'create_note_form_id':
            create_note_form = NoteForm(request.user, request.POST)
            if create_note_form.is_valid():
                note = create_note_form.save(commit=False)
                note.author = request.user
                note.save()
                return redirect("/")
        else:
            form22 = GroupForm(request.POST)
            if form22.is_valid():
                group = form22.save(commit=False)
                group.author = request.user
                group.save()
                return redirect("/create_note")

    create_note_form = NoteForm(author=request.user)
    form22 = GroupForm()
    return render(request, 'notesManager/create_note.html', {'create_note_form': create_note_form, 'form22': form22})

