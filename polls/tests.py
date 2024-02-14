from django.test import TestCase
import datetime
from django.utils import timezone
from polls.models import Question
from django.urls import reverse

# Create your tests here.
def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):

    # Test pour  vérifier que la méthode renvoie False lorsque la date de publication  est  dans le futur

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    # Test pour  vérifier que la méthode renvoie False pour les questions anciennes de plus  d'un jour

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1,  seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    # Test pour vérifier que la méthode  renvoie True pour les  questions datant du jour  précédent
        
    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    # Vérifie que s'il  n'y a aucune  question le message s'affiche
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerySetEqual(response.context['latest_question_list'], [])


    # Vérifie que les questions avec une date de publication dans le passée,  sont bien affichée sur la page index
    def test_past_question(self):
        question = create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context["latest_question_list"],[question],)

    # Vérifie que les questions avec  une pud  date dans le future ne sont pas  affichées
    def test_future_question(self):
        question = create_question(question_text="Future Question",  days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls available")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])
    
    # Vérifie que s'il existe des questions dans le passé et  d'autres dans le futur ,
    # seuls celles dont la date de publication est dépassée sont affichées
    def test_past_and_future_question(self):
        question = create_question(question_text="Past Question", days=-30)
        create_question(question_text="Future Question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question],)

    # Vérifie que la  page  index doit afficher plusieurs questions
    def test_two_past_questions(self):
        question1 = create_question(question_text="Past Question 1", days=-30)
        question2 = create_question(question_text="Past Question 2", days=-3)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question2,  question1],)

class QuestionDetailViewTests(TestCase):

    # Vérifier  que les détails d'une question dont la pub date est dans le futur ne s'affiche pas
    def test_future_question(self):
        future_question = create_question(question_text="Future Question", days=30)
        url = reverse ("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # Vérifier que les détails d'une question dont la pub_date est dans le passé s'affiche
    def test_past_question(self):
        past_question = create_question(question_text="Past Question", days=-5)
        url = reverse ("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
