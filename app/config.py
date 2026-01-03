import os

API_URL = "https://api.nexusmods.com"
API_GITHUB_URL = "https://api.github.com"
API_KEY = os.getenv('API_KEY')
PATH_JOGO = {
    'eldenring': os.getenv('PATH_ELDENRING'),
    'monsterhunterworld': os.getenv('PATH_MHWORLD'),
    'monsterhunterwilds': os.getenv('PATH_MHWILDS'),
    'clairobscurexpedition33': os.getenv('PATH_EXPED33'),
}
