from flask import Blueprint, render_template, session, redirect, url_for

from kindle2pocket.models import User
from kindle2pocket.extensions import pocket

from kindle2pocket.extensions import db

from kindle2pocket.config import params

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
@main.route('/<path:item_url>', methods=['GET', 'POST'])
def index(item_url=None):
    if item_url:
        session['item_url'] = item_url

    if 'user' in session:
        user = User.query.filter_by(email=session['user']).first()

        if not user.access_token:
            return redirect(pocket.request_access_token(redirect_to=params['domain']+'/access'))
            # return redirect(pocket.request_access_token(redirect_to='http://127.0.0.1:5000//access'))

        else:
            pocket.access_token = user.access_token
            pocket.add_item(session['item_url'])
            return 'OK 4'

    return render_template('index.html')


@main.route('/access', methods=['GET', 'POST'])
def access():
    return str(pocket.request_token)
    if 'user' in session:
        user = User.query.filter_by(email=session['user']).first()

        # getting access token
        # step 2
        pocket.get_access_token()
        user.access_token = pocket.access_token
        db.session.commit()
    return render_template('index.html')

# if __name__ == '__main__':
    # redirect(pocket.request_access_token(redirect_to=params['domain'] + '/access'))
    # pocket.request_token='ffa0ec46-7bb0-2245-61cf-1a4608'
    # pocket.get_access_token()
    # pocket.access_token = '59b190fa-0ae2-dda1-5005-48dd04'
    # pocket.add_item('https://www.youtube.com')