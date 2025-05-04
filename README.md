Reminder service

Flask

DB: SQLite

Create reminder (Post)

http://127.0.0.1:5000/reminder

{
  "userId": "user123",
  "name": "Stretch Break",
  "description": "Get up and stretch your legs",
  "startTime": "2025-05-01T11:00:00",
  "endTime": "2025-05-01T11:05:00",
  "recurrenceRule": "FREQ=DAILY;INTERVAL=1",
  "timezone": "UTC",
  "notificationType": "email"
}
