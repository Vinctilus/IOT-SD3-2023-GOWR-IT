#wiht the help of chat gpt
from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from . import database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://GrowIT:PFa24ktaOtaDelta4@localhost/growit'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = database.db
db.init_app(app)



# Manuell den Anwendungskontext erstellen
with app.app_context():
    #db.drop_all()
    # Erstelle die Datenbank-Tabellen
    db.create_all()

    # Füge einen Benutzer hinzu
    try:
        new_user = User(useremail='günter@günter.günigü',name="günter",googelid=123456789012345678,logedin=False)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Änderungen verwerfen
        print(f"Fehler: {e}")

# Routen für Webseiten-Aufrufe
@app.route('/')
def home():
    return 'Willkommen auf der Startseite!'
@app.route('/users')
def get_all_users():
    all_users = User.query.all()
    users_list = [{'useremail': user.useremail, 'googelid': user.googelid} for user in all_users]
    return jsonify(users_list)

@app.route('/users/<int:user_id>')
def get_user_by_id(googelid):
    specific_user = User.query.get(googelid)
    if specific_user:
        return jsonify({'useremail': specific_user.useremail, 'googelid': specific_user.googelid})
    else:
        return jsonify({'message': 'Benutzer nicht gefunden'}), 404

@app.route('/check_username', methods=['POST'])
def check_username():
    # Hole den Benutzernamen aus der Anfrage
    requested_username = request.json.get('useremail')

    # Überprüfe, ob der Benutzername bereits existiert
    existing_user = User.query.filter_by(username=requested_username).first()

    if existing_user:
        return jsonify({'message': 'Benutzername bereits vergeben'}), 400
    else:
        return jsonify({'message': 'Benutzername ist verfügbar'}), 200  


# Führe die Flask-Anwendung aus
if __name__ == '__main__':
    app.run(debug=True)

