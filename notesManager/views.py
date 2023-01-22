from django.contrib.sites.shortcuts import get_current_site
from django.db.models.functions import Lower
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_protect

from .forms import NewUserForm, NoteForm, GroupForm, RemainderForm
from django.contrib.auth import login, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Note, NoteGroup, Remainder
from django.core.mail import send_mail, EmailMessage
from .tokens import account_activation_token
from django.db.models import Q

@login_required(login_url="/login")
def index(request):
    if request.method == "POST":
        note_id = request.POST.get("note-id")
        note = Note.objects.filter(id=note_id).first()
        if note and note.author == request.user:
            note.delete()
    sorting = request.GET.get('sorting', '')
    group = request.GET.get('group', '')
    if sorting == 'name':
        notes = Note.objects.filter(author=request.user).order_by(Lower('title'))
    elif sorting == 'nameDESC':
        notes = Note.objects.filter(author=request.user).order_by(Lower('title').desc())
    elif sorting == 'date':
        notes = Note.objects.filter(author=request.user).order_by('pub_date')
    else:
        notes = Note.objects.filter(author=request.user).order_by('-pub_date')
    if group != '':
        notes = notes.filter(group=group)
    groups = NoteGroup.objects.filter(author=request.user).order_by(Lower('name'))
    context = {
        'sorting': sorting,
        'group': group,
    }
    return render(request, 'notesManager/main.html', {'notes': notes, 'groups': groups, 'context': context})


@login_required(login_url="/login")
def note_details(request, primary_key):
    note = get_object_or_404(Note, pk=primary_key)
    return render(request, 'notesManager/note.html', context={'note': note})


@login_required(login_url="/login")
def modify_note(request, primary_key):
    note = get_object_or_404(Note, pk=primary_key)
    form = NoteForm(None, request.POST or None, instance=note)
    if form.is_valid():
        form.save()
        return redirect('note-detail', note.pk)
    return render(request, 'notesManager/update_note.html', context={'note': note, 'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login")
        return redirect("/")
    else:
        messages.error(request, "Activation link is invalid")
    return redirect("/registration")


def activate_email(request, user, email):
    mail_subject = "Activate user account"
    message = render_to_string("registration/confirmation.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[email])
    if email.send():
        messages.success(request, f'Hi <b>{user}</b>, please confirm your email by clicking the activation link '
                                  f'to confirm and complete the registration')
    else:
        message.error(request, f'Sorry, problem sending your mail confirmation')


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # login(request, user)
            # messages.success(request, "Registration successful.")
            activate_email(request, user, form.cleaned_data.get('email'))
            return redirect("/")
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
                form22 = GroupForm(author=request.user)
        else:
            form22 = GroupForm(request.user, request.POST)
            if form22.is_valid():
                group = form22.save(commit=False)
                group.author = request.user
                group.save()
                return redirect("/create_note")
            else:
                create_note_form = NoteForm(author=request.user)
    else:
        create_note_form = NoteForm(author=request.user)
        form22 = GroupForm(author=request.user)
    return render(request, 'notesManager/create_note.html', {'create_note_form': create_note_form, 'form22': form22})


@login_required(login_url="/login")
def create_reminder(request):
    if request.method == 'POST':
        form = RemainderForm(request.user, request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            return redirect("/")
    else:
        form = RemainderForm(author=request.user)
    return render(request, 'notesManager/create_reminder.html', {'form': form})


@login_required(login_url="/login")
def view_reminders(request):
    if request.method == "POST":
        reminder_id = request.POST.get("reminder-id")
        r = Remainder.objects.filter(id=reminder_id).first()
        if r and r.author == request.user:
            r.delete()
    now = timezone.now()

    reminders = Remainder.objects.filter(author=request.user, date__lte=now).order_by('-priority')
    upcoming = Remainder.objects.filter(author=request.user, date__gte=now).order_by('-priority')
    return render(request, 'notesManager/reminders.html', {'reminders': reminders, 'upcoming': upcoming})
