"""
Renderer module: convertit les sections HTML en un document complet via Jinja2.
"""

import os
from jinja2 import Environment, FileSystemLoader
from typing import List, Dict

def render(sections: List[str], output_path: str):
    """
    sections: liste de blocs HTML (chaque bloc est un <h2>…)
    output_path: chemin complet du fichier à générer (ex. project-dev/docs-output/documentation.html)
    """
    # Préparation des données pour le template
    data: List[Dict] = []
    for html in sections:
        # Récupérer le titre de la section (<h2>Titre</h2>)
        # et construire un anchor (ex "Installation" -> "installation")
        # On suppose que chaque section commence par <h2>…</h2>
        start = html.find("<h2>")
        end   = html.find("</h2>")
        title = html[start+4:end].strip() if start != -1 and end != -1 else "Section"
        anchor = title.lower().replace(" ", "-")
        data.append({
            "title": title,
            "anchor": anchor,
            "html": html
        })

    # Chargement du template
    here = os.path.dirname(__file__)
    tmpl_dir = os.path.join(here, "templates")
    env = Environment(loader=FileSystemLoader(tmpl_dir), autoescape=True)
    template = env.get_template("base.html")

    # Contexte
    project_name = os.path.basename(os.getcwd())
    rendered = template.render(project_name=project_name, sections=data)

    # Création du dossier si besoin
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Écriture du HTML complet
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)
