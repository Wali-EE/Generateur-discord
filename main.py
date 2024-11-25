import os
import random
from datetime import datetime, timedelta
import discord
from discord.ext import commands
from discord import Embed
from discord.ext.commands import BucketType

# Configurations du bot Discord
TOKEN = "Votre token ici"  # Remplacez par le token de votre bot
PREFIX = "-"  # Préfixe des commandes du bot
ADMIN_ID = "ID de l'admin" # ID Discord de l'administrateur
LOCKED_USER_ID = ""  # ID des membres à verrouiller

# Chemin des dossiers et fichiers
STOCK_DIR = "stock"
USED_FILE = "utiliser.txt"
LOG_FILE = "logs.txt"
STATUS_FILE = "statut.txt"
DM_DIR = "dm"
LOCK_FILE = "lock.txt"  # Fichier pour stocker l'état de verrouillage

# Configurations
COOLDOWN_DURATION = 60  # Cooldown en secondes
ACCOUNT_EXPIRATION = timedelta(hours=96)  # Durée avant expiration des comptes utilisés
REQUIRED_STATUS = ".gg/acev3"  # Statut requis pour générer un compte

# Création des dossiers nécessaires
if not os.path.exists(STOCK_DIR):
    os.makedirs(STOCK_DIR)

if not os.path.exists(DM_DIR):
    os.makedirs(DM_DIR)

if not os.path.exists(USED_FILE):
    open(USED_FILE, "w").close()

if not os.path.exists(LOG_FILE):
    open(LOG_FILE, "w").close()

if not os.path.exists(STATUS_FILE):
    with open(STATUS_FILE, "w") as file:
        file.write(".gg/acev3")  # Statut par défaut

if not os.path.exists(LOCK_FILE):
    with open(LOCK_FILE, "w") as file:
        file.write("false")  # Par défaut, déverrouillé

# Bot Discord
intents = discord.Intents.default()
intents.presences = True  # Activer la récupération des statuts
intents.members = True  # Activer l'accès aux membres
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# Fonction pour lire l'état de verrouillage
def is_locked():
    with open(LOCK_FILE, "r") as file:
        status = file.read().strip().lower()
    return status == "true"

# Fonction pour vérifier le statut de l'utilisateur
def has_required_status(member: discord.Member) -> bool:
    if member.activity and member.activity.type == discord.ActivityType.custom:
        return REQUIRED_STATUS.lower() in member.activity.name.lower()
    return False

# Gestion des commandes
@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")

@bot.event
async def on_message(message):
    print(f"Message reçu : {message.content}")
    await bot.process_commands(message)

# Générer un compte avec cooldown
@bot.command(name="gen")
@commands.cooldown(1, COOLDOWN_DURATION, BucketType.user)
async def generate_account(ctx, service: str):
    """
    Génère un compte pour un service donné et l'envoie en DM sous forme d'embed.
    """
    # Vérifiez si l'utilisateur a le statut requis
    member = ctx.author
    if not has_required_status(member):
        await ctx.send(f"Vous devez avoir le statut `{REQUIRED_STATUS}` pour utiliser cette commande.")
        return

    # Vérification du verrouillage
    if is_locked() and ctx.author.id == LOCKED_USER_ID:
        await ctx.send("Vous n'êtes pas autorisé à utiliser cette commande pour le moment.")
        return

    # Génération du compte
    file_path = os.path.join(STOCK_DIR, f"{service}.txt")
    if not os.path.exists(file_path):
        await ctx.send(f"Aucun service nommé '{service}' trouvé.")
        return

    with open(file_path, "r") as file:
        accounts = [line.strip() for line in file if line.strip()]

    if not accounts:
        await ctx.send(f"Aucun compte disponible pour le service '{service}'.")
        return

    # Sélection aléatoire d'un compte
    account = random.choice(accounts)
    accounts.remove(account)

    # Mise à jour du fichier après retrait de l'account
    with open(file_path, "w") as file:
        file.writelines([acc + "\n" for acc in accounts])

    # Extraction de l'email et du mot de passe
    if ":" not in account:
        await ctx.send(f"Le format du compte dans le fichier '{service}.txt' est incorrect. Utilisez 'email:mdp'.")
        return

    email, password = account.split(":", 1)

    # Création de l'embed
    embed = Embed(title=f"Compte pour {service.capitalize()}", color=0x000000)
    embed.add_field(name="Email", value=email, inline=False)
    embed.add_field(name="Mot de passe", value=password, inline=False)
    embed.set_footer(text="N'oubliez pas de garder ``.gg/acev3`` en bio pour le soutient !")

    # Envoi du compte en DM
    try:
        await ctx.author.send(embed=embed)
        await ctx.send("Compte envoyé en DM.")
    except discord.Forbidden:
        await ctx.send("Je ne peux pas vous envoyer de DM. Veuillez activer les messages privés.")

# Afficher le stock avec cooldown
@bot.command(name="stock")
@commands.cooldown(1, COOLDOWN_DURATION, BucketType.user)
async def show_stock(ctx):
    """
    Affiche la liste des services disponibles et le nombre de comptes sous forme d'embed.
    """
    services = os.listdir(STOCK_DIR)
    if not services:
        await ctx.send("Aucun service disponible dans le stock.")
        return

    # Construction des informations sur le stock
    stock_info = []
    for service_file in services:
        if service_file.endswith(".txt"):
            service_name = os.path.splitext(service_file)[0]
            with open(os.path.join(STOCK_DIR, service_file), "r") as file:
                accounts = [line.strip() for line in file if line.strip()]
                stock_info.append(f"{service_name}: **{len(accounts)} comptes disponibles**")

    if not stock_info:
        await ctx.send("Aucun service disponible dans le stock.")
        return

    # Création de l'embed
    embed_color = random.randint(0x000000, 0xFFFFFF)  # Couleur aléatoire
    embed = Embed(title="📦 Stock des services", color=embed_color)
    embed.description = "\n".join(stock_info)
    embed.set_footer(text="Dernière mise à jour du stock.")

    # Envoi de l'embed
    await ctx.send(embed=embed)

# Gestion des erreurs de cooldown
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Commande en cooldown. Réessayez dans {round(error.retry_after, 1)} secondes.")
    else:
        raise error

# Lancer le bot
bot.run(TOKEN)