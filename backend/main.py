from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__, template_folder='../templates')

#   Módosított DB csatlakozás tesztek futtatásához

if os.environ.get('FLASK_ENV') == 'testing':
    print('TESTING MODE')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    print('PRODUCTION MODE')
    # PostgreSQL kapcsolat Neon DB-vel
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'postgresql+psycopg2://neondb_owner:npg_jJo5RHZvQhd3@'
        'ep-winter-flower-ag0v0vhc-pooler.c-2.eu-central-1.aws.neon.tech/neondb'
    )
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@servername/dbname'
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
     'connect_args': {'sslmode': 'require'}
    }

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELL DEFINÍCIÓK ---
class AppUser(db.Model):
    __tablename__ = 'app_user'
    id = db.Column(db.Integer, primary_key=True)
    unique_key = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    base_vacation_days = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

class VacationEntry(db.Model):
    __tablename__ = 'vacation_entry'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    vacation_date = db.Column(db.Date, nullable=False)
    days = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

# --- ENDPOINTOK ---

# Index.html
@app.route('/')
def index():
    return render_template('index.html')

# Regisztráció
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if AppUser.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 400

    # Meghatározzuk a következő Unique_Key-t
    last_user = AppUser.query.order_by(AppUser.id.desc()).first()
    next_id = (last_user.id + 1) if last_user else 1
    unique_key = f"UKEY-{next_id:03d}"  # pl. UKEY-001, UKEY-002

    user = AppUser(
        unique_key=unique_key,
        email=data['email'],
        password_hash=data['password_hash'],
        full_name=data['full_name'],
        base_vacation_days=data['base_vacation_days']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = AppUser.query.filter_by(email=data['email'], password_hash=data['password_hash']).first()
    if user:
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# Szabadságok lekérése
@app.route('/vacations', methods=['GET'])
def user_vacations():
    email = request.args.get('email')
    user = AppUser.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    vacations = VacationEntry.query.filter_by(user_id=user.id).all()
    used_days = sum(v.days for v in vacations)
    vacation_list = [{"id": v.id, "vacation_date": v.vacation_date.isoformat(), "days": v.days} for v in vacations]
    return jsonify({
        "base_vacation_days": user.base_vacation_days,
        "used_vacation_days": used_days,
        "available_vacation_days": user.base_vacation_days - used_days,
        "vacations": vacation_list
    })

# Új szabadság hozzáadása
@app.route('/vacations', methods=['POST'])
def add_vacation():
    data = request.json
    user = AppUser.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    vacations = VacationEntry.query.filter_by(user_id=user.id).all()
    used_days = sum(v.days for v in vacations)
    if used_days + data['days'] > user.base_vacation_days:
        return jsonify({"error": "Not enough vacation days available"}), 400
    vacation = VacationEntry(
        user_id=user.id,
        vacation_date=datetime.strptime(data['vacation_date'], '%Y-%m-%d').date(),
        days=data['days']
    )
    db.session.add(vacation)
    db.session.commit()
    return jsonify({"message": "Vacation added successfully"}), 201

# Szabadság törlése
@app.route('/vacations/<int:vacation_id>', methods=['DELETE'])
def delete_vacation(vacation_id):
    vacation = VacationEntry.query.get(vacation_id)
    if not vacation:
        return jsonify({"error": "Vacation not found"}), 404
    db.session.delete(vacation)
    db.session.commit()
    return jsonify({"message": "Vacation deleted successfully"}), 200

# Szabadság módosítása
@app.route('/vacations/<int:vacation_id>', methods=['PUT'])
def modify_vacation(vacation_id):
    data = request.json
    vacation = VacationEntry.query.get(vacation_id)
    if not vacation:
        return jsonify({"error": "Vacation not found"}), 404

    user = AppUser.query.get(vacation.user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Lekérjük az összes szabadságot, kivéve a módosítandót
    other_vacations = VacationEntry.query.filter(
        VacationEntry.user_id == user.id,
        VacationEntry.id != vacation_id
    ).all()
    used_days = sum(v.days for v in other_vacations)

    # Új napok ellenőrzése
    new_days = data.get('days', vacation.days)
    if used_days + new_days > user.base_vacation_days:
        return jsonify({"error": "Not enough vacation days available"}), 400

    # Frissítés
    if 'vacation_date' in data:
        vacation.vacation_date = datetime.strptime(data['vacation_date'], '%Y-%m-%d').date()
    vacation.days = new_days

    db.session.commit()
    return jsonify({"message": "Vacation modified successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)