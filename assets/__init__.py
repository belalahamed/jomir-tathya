import os

BASE_DIR = os.path.dirname(__file__)

IMAGES = {
    "logo": os.path.join(BASE_DIR, "images", "jomir-tathya-logo.png")
}

def get_image(name):
    return IMAGES.get(name)