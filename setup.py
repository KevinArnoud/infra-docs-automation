from setuptools import setup, find_packages

setup(
    name="infra-docs-automation",
    version="0.1.0",
    description="Outil IA pour générer automatiquement des documentations HTML à partir de code infra/dev/secops",
    author="Kevin Arnoud",
    author_email="kev.arnoud@outlook.fr",
    packages=find_packages(include=["auto_doc", "auto_doc.*"]),
    install_requires=[
        "openai",
        "jinja2",
    ],
    entry_points={
        "console_scripts": [
            "auto_doc=auto_doc.ci_pipeline:main",
        ],
    },
)
