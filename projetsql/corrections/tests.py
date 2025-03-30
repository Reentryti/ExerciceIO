from django.test import TestCase
from exercices.models import Exercice
from utilisateurs.models import Utilisateur
from corrections.services.ia import DeepSeekService, OllamaService
from model_bakery import baker
from django_celery_results.models import TaskResult

# Create your tests here.

class CorrectionTest(TestCase):
    def setUp(self):
        self.user = baker.make('utilisateurs.Utilisateur')
        self.exercice = baker.make('exercices.Exerccice')
        self.solution = baker.make('solutions.Solution', exercice=self.exercice, etudiant=self.user)

        @patch('corrections.services.ia.requests.post')
        def test_deepseek_correction(self, mock_post):
            mock_response ={
                "choices": [{
                    "message":{
                        "content": '{"score": 15, "feedback": "Bien"}'
                    }
                }]
            }
            mock_post.return_value.json.return_value = mock_response

            result = DeepSeekService.generate_feedback("Test prompt")
            self.assertIn('choices', result)


