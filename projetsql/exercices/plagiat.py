import spacy
from collections import defaultdict

#Chargement du modele francais de spacy
nlp = spacy.load("fr_core_news_md")

#Fonction d'analyse des fichiers
def analyse_nlp(solutions):
    seuil = 0.8
    resultat = defaultdict

    #Traitement
    docs = [nlp(solution.contenu_textuel) for solution in solutions]
    #Comparaison par deux solutions
    for i, doc1 in enumerate(docs):
        for j, doc2 in enumerate(docs[i+1], start=i+1):
            similarite = doc1.similarity(doc2)
            if similarite > seuil:
                resultat["solutions_suspectes"].append({
                    "id_solution1": solution[i].id,
                    "id_solution2": solution[j].id,
                    "similarite": round(similarite, 3),
                    "method": "spaCy_NLP"
                })

    return resultat