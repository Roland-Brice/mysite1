from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Heloooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")

def detail(request, question_id):
    return HttpResponse("Vous cherchez la question %s." % question_id)

def results(request, question_id):
    response = "Vous cherchez les résultats à la question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    response = "Vote pour la question %s."
    return HttpResponse(response % question_id)