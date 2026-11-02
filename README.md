Stage Tracker

Le problème que ça résout : quand les candidatures s'accumulent, on perd vitele fil. Qui était le contact chez Thales ? Ai-je déjà relancé ? C'était quelle version du CV pour cette offre ? Stage Tracker garde tout au même endroit :les entreprises, les offres, la pipeline des candidatures, les recruteurs etl'historique des échanges. Plus tard, il m'aidera à générer avec un LLM un CVet une lettre adaptés à chaque offre.

Ce qui existe déjà
La pipeline complète : une offre démarre en wishlist, puis applied,screening, interview, offer — et les deux issues tristes, rejectedet ghosted.
Créer une offre crée automatiquement sa candidature, dans une seuletransaction : pas d'offre orpheline dans la base.
Un répertoire de contacts, rattachés à une entreprise ou pas encore — unrecruteur repéré sur LinkedIn se sauvegarde même sans entreprise.
Un journal d'interactions par candidature, avec de vraies dates : on peutsaisir un échange de la semaine dernière sans fausser l'ordre du journal.
La doc des endpoints est générée automatiquement par FastAPI (/docs).
La stack
Python 3.14, FastAPI, SQLAlchemy 2, PostgreSQL 17 dans Docker, migrationsAlembic. Le front React viendra quand la couche données sera stable — d'abordle fond, ensuite la forme.

Lancer le projet
Il faut Python (3.13+), Docker, et un fichier .env avec l'accès à la base :

git clone https://github.com/caplain20/stage-tracker.gitcd stage-trackerpython -m venv .venv && source .venv/bin/activatepip install -r requirements.txtdocker compose up -d
Créer un fichier .env à la racine (il n'est pas versionné, volontairement) :

DATABASE_URL=postgresql+psycopg://stagetracker:VOTRE_MOT_DE_PASSE@localhost:5432/stagetracker
Puis :

alembic upgrade headuvicorn main:app --port 8100 --reload
La documentation interactive des endpoints : http://localhost:8100/docs

Notes de chantier
Quelques choses apprises en construisant, en vrac :

Le server_default d'une colonne ne joue que si la colonne est absente del'INSERT. Passer None explicitement, c'est écrire NULL — et un 500 au lieud'une date automatique.
Les règles de suppression (CASCADE, SET NULL) valent mieux déclarées dans labase que recodées dans l'API : le moteur les applique toujours, même quand onoublie côté Python.
Alembic + autogenerate évitent que le modèle Python et la vraie basedérivent l'un de l'autre.
La suite
Référentiel de faits (parcours, compétences, projets) en JSONB
Génération LLM de CV / lettres adaptés par offre
Front React
Déploiement k3s
Ce qui a changé : première personne, une histoire au lieu d'un pitch, plus aucun emoji ni tableau, une section « Notes de chantier » qui assume les galères rencontrées (c'est exactement ce qu'un ingénieur senior respecte dans un repo d'alternant), et des blocs de code à l'ancienne (indentation) plutôt que du markdown décoré.

