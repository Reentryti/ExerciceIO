from celery import shared_task
from .models import Correction
from .services.correction import CorrectionEngine

@shared_task(bind=True)
def process_correction_task(self, solution_id, provider="DEEPSEEK"):
    from exercices.models import Solution
    solution = Solution.objects.get(id=solution_id)
    
    result = CorrectionEngine.create_correction(solution, provider)
    
    Correction.objects.create(
        solution=solution,
        provider=provider,
        **result
    )