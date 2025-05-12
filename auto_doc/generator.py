"""
Generator module: appelle l'API OpenAI pour générer du HTML à partir d'un prompt.
"""

import os
import openai

# Récupération de la clé
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate(prompt: str, model: str = "gpt-4o-mini") -> str:
    """
    Envoie le prompt à l'API OpenAI et retourne la réponse textuelle.
    """
    if not openai.api_key:
        raise RuntimeError("Clé OpenAI non définie. Exportez OPENAI_API_KEY avant de lancer.")

    resp = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Tu es un assistant expert en documentation technique."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=800,
    )
    # Dans la nouvelle API, on accède à resp.choices[0].message.content de la même façon
    return resp.choices[0].message.content.strip()
