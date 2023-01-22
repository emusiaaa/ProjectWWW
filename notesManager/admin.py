from django.contrib import admin
from .models import NoteGroup, Note, Remainder
# # Register your models here.
admin.site.register(Note)
admin.site.register(NoteGroup)
admin.site.register(Remainder)
