from flask import Blueprint

posts = Blueprint('posts',__name__)

from .routes import *