from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
from django.views import generic
from django.utils import timezone

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    #response = "Vote pour la question %s."
    #return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You did not select a choice",
            }
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


""""
def index(request):
    #return HttpResponse("Heloooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    #output = ", ".join([q.question_text for q in latest_question_list])
    #return HttpResponse(output)
    #template = loader.get_template("polls/index.html")
    context = {"latest_question_list" : latest_question_list }
    #return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    #return HttpResponse("Vous cherchez la question %s." % question_id)
    ""
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist.")
    return render(request, "polls/detail.html", {"question":question})
    ""
    question = get_object_or_404(Question, pk = question_id)
    return render(request, "polls/detail.html", {"question" : question})


def results(request, question_id):
    #response = "Vous cherchez les résultats à la question %s."
    #return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question":question})


"""