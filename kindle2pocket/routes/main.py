from flask import Blueprint, render_template, session, redirect, url_for

from kindle2pocket.models import User
from kindle2pocket.extensions import pocket

from kindle2pocket.extensions import db
# from config.config import params

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
@main.route('/<path:item_url>', methods=['GET', 'POST'])
def index(item_url=None):
    if item_url:
        session['item_url'] =item_url
        
    if 'user' in session:
        user = User.query.filter_by(email=session['user']).first()

        # getting access token
        # step 2
        if 'token_step' in session and session['token_step'] == 2:
            session.pop('token_step')
            pocket.get_access_token()
            user.access_token = pocket.access_token
            db.session.commit()
        # step 1
        elif not user.access_token:
            session['token_step'] = 2
            return redirect(pocket.request_access_token(redirect_to='http://127.0.0.1:5000/'))

        else:
            pocket.access_token = user.access_token
            pocket.add_item(session['item_url'])
            return 'OK 4'

    return render_template('index.html')
