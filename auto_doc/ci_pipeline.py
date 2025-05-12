import sys
import os
from auto_doc.extractor import extract
from auto_doc.prompter import build_prompt
from auto_doc.generator import generate
from auto_doc.renderer import render

def main():
    if len(sys.argv) != 2:
        print("Usage: auto_doc <project-path>")
        sys.exit(1)

    project = sys.argv[1]
    items = extract(project)
    html_sections = []

    for item in items:
        for section in ["Installation", "Configuration", "Exploitation"]:
            prompt = build_prompt(section, item)
            html = generate(prompt)
            html_sections.append(html)

    output_dir  = os.path.join(project, "docs-output")
    output_file = os.path.join(output_dir, "documentation.html")
    os.makedirs(output_dir, exist_ok=True)

    render(html_sections, output_file)
    print(f"Documentation générée dans {output_file}")

if __name__ == "__main__":
    main()
