"""
Prompter module: génère les prompts LLM pour chaque section de doc.
"""

from typing import Dict, List

PROMPT_TEMPLATE = """
Vous êtes un expert en documentation technique. 
Pour le fichier "{file}", générez une section <strong>{section}</strong> en HTML avec :
- Une liste claire des prérequis et dépendances (à partir des commentaires)
- Les commandes et extraits de code (à partir des blocs)
- Des explications détaillées, compréhensibles par un admin stagiaire
- Des balises <h2>, <ul>, <code> adaptées

Commentaires détectés :
{comments}

Bloc de code :
<pre><code>
{code}
</code></pre>

Répondez uniquement par le corps HTML de la section (sans wrapper complet).
"""

def build_prompt(section: str, file_info: Dict) -> str:
    """
    section: "Installation", "Configuration" ou "Exploitation"
    file_info: dict issu de extractor.extract(), avec clés "file", "comments", "blocks"
    Retourne le prompt texte à passer à l'API LLM.
    """
    # On prend le premier bloc, et tous les commentaires
    comments: List[str] = file_info.get("comments", [])
    blocks: List[str] = file_info.get("blocks", [])
    code = blocks[0] if blocks else ""
    # Formatage des commentaires
    comments_text = "\n".join(f"- {c}" for c in comments)

    return PROMPT_TEMPLATE.format(
        file=file_info.get("file", ""),
        section=section,
        comments=comments_text,
        code=code
    )
