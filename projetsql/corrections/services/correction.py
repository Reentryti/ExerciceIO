import requests
#from django.conf import settings
from decouple import config
from django.core.exceptions import ValidationError

class CorrectionEngine:
    @classmethod
    def create_correction(cls, solution, provider="DEEPSEEK"):
        """Version optimisée avec gestion d'erreurs améliorée"""
        if provider == "DEEPSEEK":
            return cls._create_deepseek_correction(solution)
        raise ValueError("Provider de correction non supporté")

    @classmethod
    def _create_deepseek_correction(cls, solution):
        from ..models import Correction

        #Verifier si la correction existe
        try:
            existing_correction = Correction.objects.get(solution=solution)
            return existing_correction
        except Correction.DoesNotExist:

            content = cls._extract_content(solution)
            response = cls._call_deepseek_api(
                consigne=solution.exercice.description,
                solution=content
            )

            correction = Correction(solution=solution, commentaires=response['commentaires'], note=response['note'], provider='DEEPSEEK', metadata={'api_response': response.get('raw_response'), 'content_extracted': content})
            correction.full_clean()
            correction.save()

            solution.note = correction.note
            solution.save()

            return correction

    @staticmethod
    def _extract_content(solution):
        """Extrait le contenu de la solution de manière robuste"""
        if solution.fichier:
            try:
                with solution.fichier.open('r') as f:
                    return f.read()
            except (UnicodeDecodeError, IOError) as e:
                return f"[Erreur de lecture: {str(e)}]"
        return getattr(solution, 'solution_texte', '[Aucun contenu]')

    @classmethod
    def _call_deepseek_api(cls, consigne, solution):
        """Appel API avec gestion d'erreur complète"""
        try:
            from decouple import config
            
            api_url = "https://api.deepseek.com/v1/chat/completions"
            api_key = config('DEEPSEEK_API_KEY', default='')
            
            response = requests.post(
                api_url,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [{
                        "role": "user",
                        "content": cls._build_prompt(consigne, solution)
                    }],
                    "temperature": 0.5,
                    "max_tokens": 2000
                },
                timeout=30
            )
            response.raise_for_status()
            return cls._parse_response(response.json())
        except Exception as e:
            return {
                'commentaires': f"Erreur de correction: {str(e)}",
                'note': None,
                'raw_response': None
            }

    @staticmethod
    def _build_prompt(consigne, solution):
        """Construit le prompt de manière structurée"""
        return f"""
        [Rôle] Correcteur automatique d'exercices
        [Consigne] {consigne}
        [Solution à corriger] {solution}

        Merci de:
        1. Analyser rigoureusement la solution
        2. Donner une note sur 20 avec justification
        3. Proposer des améliorations
        4. Formuler des commentaires pédagogiques
        """

    @staticmethod
    def _parse_response(api_response):
        """Extrait les données pertinentes de la réponse API"""
        try:
            content = api_response['choices'][0]['message']['content']
            return {
                'commentaires': content,
                'note': cls._extract_note(content),
                'raw_response': api_response
            }
        except (KeyError, IndexError) as e:
            raise ValueError(f"Réponse API malformée: {str(e)}")

    @staticmethod
    def _extract_note(text):
        """Extrait la note du texte avec regex améliorée"""
        import re
        match = re.search(r'Note\s*:\s*(\d{1,2}(?:[.,]\d+)?)/20', text, re.IGNORECASE)
        return float(match.group(1).replace(',', '.')) if match else None


#Testeur de correction
        
def direct_deepseek_call(consigne, solution_content):
    """Standalone function to call DeepSeek API directly"""
    import requests
    from decouple import config
    
    # Get API credentials directly with config
    api_url = config('DEEPSEEK_API_URL', default='https://api.deepseek.com/v1/chat/completions')
    api_key = config('DEEPSEEK_API_KEY', default='')
    
    try:
        response = requests.post(
            api_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [{
                    "role": "user",
                    "content": f"""
                    [Rôle] Correcteur automatique d'exercices
                    [Consigne] {consigne}
                    [Solution à corriger] {solution_content}

                    Merci de:
                    1. Analyser rigoureusement la solution
                    2. Donner une note sur 20 avec justification
                    3. Proposer des améliorations
                    4. Formuler des commentaires pédagogiques
                    """
                }],
                "temperature": 0.5,
                "max_tokens": 2000
            },
            timeout=30
        )
        
        response.raise_for_status()
        content = response.json()['choices'][0]['message']['content']
        
        # Simple regex for note extraction
        import re
        note_match = re.search(r'Note\s*:\s*(\d{1,2}(?:[.,]\d+)?)/20', content, re.IGNORECASE)
        note = float(note_match.group(1).replace(',', '.')) if note_match else None
        
        return {
            'commentaires': content,
            'note': note,
            'raw_response': response.json()
        }
    except Exception as e:
        return {
            'commentaires': f"Erreur de correction: {str(e)}",
            'note': None,
            'raw_response': None
        }