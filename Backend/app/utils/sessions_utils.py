from datetime import datetime, timedelta
from flask import session, current_app
import os

def check_daily_limit():
    db = current_app.config['db']
    uploads_collection = db.uploads
    now = datetime.utcnow()

    # Get the session ID from the current session
    session_id = session.get('session_id')
    if not session_id:
        session_id = os.urandom(16).hex()  # Generate new session ID if not present
        session['session_id'] = session_id

    # Check if the user has uploaded 5 or more files in the last 24 hours
    one_day_ago = now - timedelta(days=1)
    recent_uploads = list(uploads_collection.find({
        "session_id": session_id,
        "timestamp": {"$gte": one_day_ago}
    }))

    # Return whether the daily limit has been reached
    if len(recent_uploads) >= 5:
        return False  # Limit reached

    return True  # Limit not reached
