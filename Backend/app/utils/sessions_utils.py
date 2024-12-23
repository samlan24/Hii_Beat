from flask import session, current_app
from datetime import datetime, timedelta
import os

def check_daily_limit():
    db = current_app.config['db']
    uploads_collection = db.uploads
    now = datetime.utcnow()

    # Check if the session ID exists; if not, create one (handled by Flask-Session)
    if 'session_id' not in session:
        session['session_id'] = os.urandom(16).hex()  # Generate a new session ID

    session_id = session['session_id']
    one_day_ago = now - timedelta(days=1)

    # Query the user's uploads in the last 24 hours
    recent_uploads = list(uploads_collection.find({
        "session_id": session_id,
        "timestamp": {"$gte": one_day_ago}
    }))

    # Check if user has exceeded the daily limit
    return len(recent_uploads) < 2