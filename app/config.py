import os

API_URL = "https://api.nexusmods.com"
API_KEY = os.getenv('API_KEY')
PATH_JOGO = {
    'eldenring': os.getenv('PATH_ELDENRING'),
    'monsterhunterworld': os.getenv('PATH_MHWORLD'),
    'monsterhunterwilds': os.getenv('PATH_MHWILDS')
}
