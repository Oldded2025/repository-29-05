from django.shortcuts import render

from notes.models import Note


def note_list(request):
    notes = Note.objects.all()
    return render(request, 'notes/note_list.html', {'notes': notes})
# Create your views here.
