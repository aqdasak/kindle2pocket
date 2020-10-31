from flask import Blueprint, render_template, session, redirect, url_for

from k2p.models import User

# from config.config import params

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')
