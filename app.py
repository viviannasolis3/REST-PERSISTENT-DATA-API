from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime, timezone
from pathlib import Path
import json

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'clinical_data.db'
JSONL_PATH = BASE_DIR / 'data' / 'clinical_data.jsonl'
JSONL_PATH.parent.mkdir(exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ClinicalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    diagnosis = db.Column(db.String(200), nullable=False)
    blood_pressure = db.Column(db.String(20), nullable=False)
    heart_rate = db.Column(db.Integer, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'patient_name': self.patient_name, 'age': self.age,
                'diagnosis': self.diagnosis, 'blood_pressure': self.blood_pressure,
                'heart_rate': self.heart_rate, 'temperature': self.temperature,
                'created_at': self.created_at.isoformat()}

class ClinicalSchema(BaseModel):
    patient_name: str = Field(min_length=1)
    age: int = Field(ge=0, le=120)
    diagnosis: str = Field(min_length=1)
    blood_pressure: str = Field(pattern=r'^\d{2,3}/\d{2,3}$')
    heart_rate: int = Field(ge=20, le=250)
    temperature: float = Field(ge=90, le=110)

@app.route('/clinical/', methods=['POST'])
def create_clinical_record():
    try:
        data = ClinicalSchema.model_validate(request.get_json())
    except ValidationError as error:
        return jsonify({'error': 'Invalid clinical data', 'details': error.errors(include_context=False)}), 400
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid JSON body'}), 400
    record = ClinicalData(**data.model_dump(), created_at=datetime.now(timezone.utc).replace(tzinfo=None))
    try:
        db.session.add(record)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Database write failed'}), 500
    result = record.to_dict()
    try:
        with JSONL_PATH.open('a', encoding='utf-8') as file:
            file.write(json.dumps(result) + '\n')
    except OSError:
        return jsonify({'error': 'Database saved, but JSONL append failed', 'record': result}), 500
    return jsonify(result), 201

@app.route('/clinical/', methods=['GET'])
def get_clinical_records():
    records = db.session.execute(db.select(ClinicalData).order_by(ClinicalData.id)).scalars().all()
    return jsonify([record.to_dict() for record in records]), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
