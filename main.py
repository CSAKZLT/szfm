# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vacation.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@servername/dbname'
# majd a sajat mqsql adataival helyettesitjuk
db = SQLAlchemy(app)

# Model
# Ideiglenes db adatok
class User(db.Model):
    email = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    total_vacation = db.Column(db.Integer, nullable=False)
    used_vacation = db.Column(db.Integer, default=0)

# Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 400
    user = User(email=data['email'], name=data['name'],
                password=data['password'], total_vacation=data['total_vacation'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email'], password=data['password']).first()
    if user:
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

if __name__ == '__main__':
    #ez is csak ideiglenesen került bele
    with app.app_context():
        db.create_all()
    app.run(debug=True)
