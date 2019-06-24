from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone


# def index(request):
#     late_qust_list = Question.objects.order_by("pub_date")[:5]
#     context = {"l_q_l": late_qust_list}
#     return render(request, "polls/index.html.j2", context)
#
#
# def detail(request, question_id):
#     q = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html.j2", {"q": q})
#
#
# def results(request, question_id):
#     q = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html.j2", {"q": q})


class IndexView(generic.ListView):
    template_name = "polls/index.html.j2"
    context_object_name = "l_q_l"

    def get_queryset(self):
        """return the last 5 questions """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )[:5]


class DetailView(generic.DetailView):
    model = Question
    context_object_name = "q"
    template_name = "polls/detail.html.j2"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html.j2"
    context_object_name = "q"


def vote(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    try:
        sel_ch = q.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html.j2",
            {"q": q, "er_m": "You didn't select a choice."},
        )
    else:
        sel_ch.votes = F("votes") + 1
        sel_ch.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))
