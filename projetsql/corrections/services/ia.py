# corrections/services/ia.py
#import requests
#from django.conf import settings

#class AICorrectionService:
 #   @staticmethod
  #  def generate_feedback(prompt: str) -> dict:
   #     """Version simplifiée utilisant uniquement DeepSeek"""
    #    try:
     #       response = requests.post(
      #          "https://api.deepseek.com/v1/chat/completions",
       #         headers={"Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}"},
         #       json={
        #          "model": "deepseek-chat",
        #            "messages": [{"role": "user", "content": prompt}],
         #           "temperature": 0.3
          #      },
           #     timeout=30
            #)
            #response.raise_for_status()
            #return response.json()
       # except Exception as e:
        #    # Fallback minimaliste
         #   return {
          #      "error": str(e),
           #     "fallback_data": {
            #        "score": 10,
             #       "feedback": "Correction indisponible - Mode simulation"
              #  }
            #}