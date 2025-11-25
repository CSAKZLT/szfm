from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

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

# Szabadság törlése
@app.route('/vacations/<int:vacation_id>', methods=['DELETE'])
def delete_vacation(vacation_id):
    vacation = VacationEntry.query.get(vacation_id)
    if not vacation:
        return jsonify({"error": "Vacation not found"}), 404
    db.session.delete(vacation)
    db.session.commit()
    return jsonify({"message": "Vacation deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)