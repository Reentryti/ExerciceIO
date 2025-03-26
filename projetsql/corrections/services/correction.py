from .ia_services import DeepSeekService, OllamaService

class CorrectionEngine:
    @classmethod
    def create_correction(cls, solution, provider="DEEPSEEK"):
        prompt = cls._build_prompt(solution)
        
        if provider == "OLLAMA":
            response = OllamaService.generate_feedback(prompt)
        else:
            response = DeepSeekService.generate_feedback(prompt)

        return {
            "raw_response": response,
            "feedback": cls._format_response(response),
            "score": cls._extract_score(response)
        }

    @staticmethod
    def _build_prompt(solution) -> str:
        return f"""
        [INSTRUCTIONS]
        Vous êtes un professeur assistant. Corrigez cette solution d'exercice.
        Fournissez : 1) Un feedback structuré 2) Une note sur 20.

        [EXERCICE]
        {solution.exercice.enonce}

        [SOLUTION ÉLÈVE]
        {solution.contenu}
        """

    @staticmethod
    def _format_response(response: dict) -> str:
        # Implémentez la logique de parsing selon la réponse de l'IA
        ...