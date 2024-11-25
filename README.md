**Bot Discord - Générateur de Comptes**
Un bot Discord qui permet :

De générer des comptes pour des services spécifiques et les envoyer en DM.
De consulter les stocks de comptes disponibles via une commande dédiée.
De gérer des restrictions basées sur le statut des utilisateurs et des permissions personnalisées.
Fonctionnalités


**Commandes de Génération :**

`-gen [service]` : Génère un compte pour le service demandé et l'envoie en message privé sous forme d'embed.
Les comptes doivent être dans le répertoire stock/ sous forme de fichiers texte (service.txt).
Commandes de Stock :

`-stock` : Affiche la liste des services et le nombre de comptes disponibles sous forme d'embed.
Conditions d’Utilisation :

Les utilisateurs doivent avoir un statut spécifique (par exemple, *.gg/acev3*) pour utiliser les commandes.
Certaines commandes peuvent être verrouillées pour des utilisateurs spécifiques.


**Système de Cooldown :**

Un cooldown configurable limite l'utilisation des commandes pour éviter les abus.

**Gestion des Erreurs :**

Gestion des erreurs de permissions, format incorrect, ou statut manquant.


*Prérequis*
Python 3.8 ou plus récent (recommandé : Python 3.10 ou 3.11).
Bibliothèque discord.py version 2.4.0.

**Installation des Dépendances**
***Pour installer les dépendances nécessaires, utilisez :***

bash
Copier le code
Dézip "stock.zip"
pip install -r requirements.txt
Installation et Configuration
Clonez ce dépôt :

bash
Copier le code
git clone https://github.com/Wali-EE/Generateur-discord
cd Generateur-discord
Créez un fichier config.py contenant votre configuration :

python
Copier le code
TOKEN = "VOTRE_TOKEN_DISCORD"  # Token du bot
PREFIX = "-"  # Préfixe des commandes
ADMIN_ID = 123456789012345678  # ID de l'administrateur
REQUIRED_STATUS = ".gg/acev3"  # Statut requis pour utiliser les commandes
COOLDOWN_DURATION = 60  # Cooldown en secondes
Structurez vos fichiers pour le stock :

Placez vos fichiers de comptes dans le répertoire stock/.
Chaque fichier doit être nommé après le service, comme netflix.txt, avec des comptes au format :
makefile
Copier le code
email1:password1
email2:password2
Lancez le bot :

bash
Copier le code
python main.py
Commandes Disponibles


Génération et Gestion
`-gen [service]` : Génère un compte pour le service demandé et l'envoie en message privé.
`-stock` : Affiche la liste des services et les comptes disponibles.

Génération des Comptes :

Les comptes sont lus depuis un fichier texte (ex. : netflix.txt) dans le répertoire stock/.
Les comptes sont marqués comme utilisés dans utiliser.txt.
Stock : Affiche les comptes disponibles dans chaque fichier de service sous forme d'embed.

Restrictions : Les utilisateurs doivent avoir un statut spécifique pour accéder aux commandes.


Contribution
Forkez le projet.

Créez une branche pour vos modifications :
bash
Copier le code
git checkout -b feature/amélioration
Proposez vos modifications via une Pull Request.
Licence
Ce projet est sous licence Apache V2.0. Consultez le fichier LICENSE pour plus d'informations.

Améliorations Futures
Ajout d'un système d’avertissements pour les utilisateurs abusifs.
Restructuration des fichiers pour que ce soit plus homogène.
amélioration générale.


_En résumé, ce README.md contient :_

👉🏼 Une description claire des fonctionnalités.
👉🏼 Les étapes d'installation et de configuration.
👉🏼 Une liste des commandes disponibles.
👉🏼 Des suggestions d'amélioration future pour les contributeurs.





