#from celery import shared_task
#from django.core.cache import cache
#from .models import Correction
#from .services.ia import AICorrectionService
#import logging

#logger = logging.getLogger(__name__)

#@shared_task(bind=True, max_retries=3)
#def process_correction(self, solution_id):
 #   """Version adaptée pour DeepSeek uniquement"""
  #  lock_id = f'solution_lock_{solution_id}'
   # 
    # Empêche les doublons avec un verrou
    #with cache.lock(lock_id, timeout=60):
     #   try:
      #      solution = Solution.objects.get(id=solution_id)
       #     prompt = f"""
        #    [Exercice] {solution.exercise.instructions}
         #   [Solution] {solution.content}
          #  """
            
           # feedback = AICorrectionService.generate_feedback(prompt)
            #
            #Correction.objects.update_or_create(
             #   solution=solution,
              #  defaults={
               #     'provider': 'DEEPSEEK',
                #    'score': feedback.get('score'),
                 #   'feedback': feedback.get('feedback'),
                  #  'raw_response': feedback
                #}
           # )
            
       # except Exception as e:
        #    logger.error(f"Erreur correction {solution_id}: {str(e)}")
         #s   self.retry(exc=e, countdown=60)