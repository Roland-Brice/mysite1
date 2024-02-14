from django.test import TestCase
import datetime
from django.utils import timezone
from polls.models import Question

# Create your tests here.

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