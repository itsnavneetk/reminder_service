from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reminders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Reminder(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    recurrence_rule = db.Column(db.String)
    timezone = db.Column(db.String, default="UTC")
    notification_type = db.Column(db.String, default="email")
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@app.route('/reminder', methods=['POST'])
def create_reminder():
    data = request.json
    try:
        reminder = Reminder(
            user_id=data['userId'],
            name=data['name'],
            description=data.get('description', ''),
            start_time=datetime.fromisoformat(data['startTime']),
            end_time=datetime.fromisoformat(data['endTime']) if data.get('endTime') else None,
            recurrence_rule=data.get('recurrenceRule'),
            timezone=data.get('timezone', 'UTC'),
            notification_type=data.get('notificationType', 'email')
        )
        db.session.add(reminder)
        db.session.commit()
        return jsonify(reminder.as_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/reminders', methods=['GET'])
def get_reminders():
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({'error': 'Missing userId'}), 400
    reminders = Reminder.query.filter_by(user_id=user_id).all()
    return jsonify([r.as_dict() for r in reminders]), 200


@app.route('/reminder', methods=['GET'])
def get_reminder():
    reminder_id = request.args.get('reminderId')
    reminder = Reminder.query.get(reminder_id)
    if not reminder:
        return jsonify({'error': 'Reminder not found'}), 404
    return jsonify(reminder.as_dict()), 200


@app.route('/reminder', methods=['PUT'])
def update_reminder():
    data = request.json
    reminder = Reminder.query.get(data['reminderId'])
    if not reminder:
        return jsonify({'error': 'Reminder not found'}), 404
    try:
        for field in ['name', 'description', 'start_time', 'end_time', 'recurrence_rule', 'active', 'timezone', 'notification_type']:
            if field in data:
                setattr(reminder, field, data[field] if not 'time' in field else datetime.fromisoformat(data[field]))
        db.session.commit()
        return jsonify(reminder.as_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/reminder/status', methods=['PATCH'])
def toggle_reminder_status():
    data = request.json
    reminder = Reminder.query.get(data['reminderId'])
    if not reminder:
        return jsonify({'error': 'Reminder not found'}), 404
    reminder.active = data['active']
    db.session.commit()
    return jsonify({'status': 'updated', 'reminder': reminder.as_dict()}), 200


@app.route('/reminder', methods=['DELETE'])
def delete_reminder():
    reminder_id = request.args.get('reminderId')
    reminder = Reminder.query.get(reminder_id)
    print(reminder_id)
    if not reminder:
        return jsonify({'error': 'Reminder not found'}), 404
    db.session.delete(reminder)
    db.session.commit()
    return jsonify({'status': 'deleted'}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
