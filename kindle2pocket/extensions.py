from flask_sqlalchemy import SQLAlchemy
# from flask_mail import Mail
from kindle2pocket.k2p import Pocket

db = SQLAlchemy()
# mail = Mail()

pocket = Pocket()
