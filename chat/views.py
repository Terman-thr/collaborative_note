import json
from django.shortcuts import render
from .models import Text, Note
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def lobby(request):
    article = Text.objects.get(id=1)
    notes = Note.objects.filter(articleId=1)
    return render(request, 'chat/lobby.html', {'article': article, 'notes': notes})


