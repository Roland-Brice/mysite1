from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Question
from django.template import loader

# Create your views here.

def index(request):
    #return HttpResponse("Heloooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    #output = ", ".join([q.question_text for q in latest_question_list])
    #return HttpResponse(output)
    template = loader.get_template("polls/index.html")
    context = {"latest_question_list": latest_question_list }
    #return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    #return HttpResponse("Vous cherchez la question %s." % question_id)
    """"
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist.")
    return render(request, "polls/detail.html", {"question":Question})
    """
    question = get_object_or_404(Question, pk = question_id)
    return render(request, "polls/detail.html", {"question":question})


def results(request, question_id):
    response = "Vous cherchez les résultats à la question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    response = "Vote pour la question %s."
    return HttpResponse(response % question_id)