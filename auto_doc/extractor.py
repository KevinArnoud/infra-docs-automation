"""
Extractor module: parcourt un projet et extrait blocs de code et commentaires.
"""

import glob
import os
from typing import List, Dict

def extract(project_path: str) -> List[Dict]:
    """
    Parcourt les fichiers de project_path/docs-source et retourne une liste de dicts:
    [
        {
            "file": "chemin/vers/fichier.ext",
            "language": "js|py|tf|yml|etc",
            "blocks": ["code ou config"],
            "comments": ["commentaires trouvés"]
        },
        ...
    ]
    """
    results: List[Dict] = []
    base = os.path.join(project_path, 'docs-source')
    # Extensions à traiter
    exts = ['*.js', '*.py', '*.tf', '*.yml', '*.yaml']
    # Recherche récursive
    files = []
    for ext in exts:
        files.extend(glob.glob(os.path.join(base, '**', ext), recursive=True))

    for filepath in files:
        comments: List[str] = []
        blocks: List[str] = []
        code_buffer: List[str] = []
        # Détecter le langage d'après l'extension
        _, ext = os.path.splitext(filepath)
        lang = ext.lstrip('.')

        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                stripped = line.strip()
                # Lignes de commentaires
                if stripped.startswith('//') or stripped.startswith('#'):
                    # Si on avait du code en mémoire, on le consigne
                    if code_buffer:
                        blocks.append('\n'.join(code_buffer))
                        code_buffer = []
                    # Nettoyage du préfixe de commentaire
                    comment = stripped.lstrip('/# ').strip()
                    comments.append(comment)
                elif stripped:
                    # Ligne de code
                    code_buffer.append(stripped)
                else:
                    # Ligne vide -> clôture d’un bloc de code
                    if code_buffer:
                        blocks.append('\n'.join(code_buffer))
                        code_buffer = []
        # Flush du dernier bloc de code
        if code_buffer:
            blocks.append('\n'.join(code_buffer))

        results.append({
            'file': filepath,
            'language': lang,
            'blocks': blocks,
            'comments': comments
        })

    return results
