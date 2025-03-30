# Arquivo: app/routes/main_routes.py
from flask import Blueprint, render_template, session
from .web_routes import web

# web = Blueprint('main', __name__)

@web.route('/')
def index():
    return render_template('index.html')

