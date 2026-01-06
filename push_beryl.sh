#!/bin/bash

# Se placer dans le dossier du projet
cd ~/beryl_ecosysteme/berylEcosystem/berylcommunity-ai-engine || exit

# Initialiser git si nécessaire
if [ ! -d ".git" ]; then
    git init
    echo "Git initialisé"
fi

# Ajouter tous les fichiers
git add .

# Commit avec message automatique
git commit -m "Optimisation et ajout de tous les fichiers"

# S'assurer que la branche principale est 'main'
git branch -M main

# Ajouter le remote si pas déjà configuré
if ! git remote | grep -q origin; then
    git remote add origin https://github.com/Generalhaypi/berylcommunity-ai-engine.git
    echo "Remote ajouté"
fi

# Pousser les modifications sur GitHub
git push -u origin main
