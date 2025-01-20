from flask import session, current_app
from datetime import datetime, timedelta
import os

def check_daily_limit():
    db = current_app.config['db']
    uploads_collection = db.uploads
    now = datetime.utcnow()


    if 'session_id' not in session:
        session['session_id'] = os.urandom(16).hex()

    session_id = session['session_id']
    one_day_ago = now - timedelta(days=1)


    recent_uploads = list(uploads_collection.find({
        "session_id": session_id,
        "timestamp": {"$gte": one_day_ago}
    }))


    return len(recent_uploads) < 10