from datetime import datetime, timedelta, timezone
class ShowActivity:
  def run(activity_uuid):
    now = datetime.now(timezone.utc).astimezone()
    
    # This is just an example - you might want to query a database instead
    activities = [
      {
        'uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
        'handle':  'Andrew Brown',
        'message': 'Cloud is fun!',
        'created_at': (now - timedelta(days=2)).isoformat(),
        'expires_at': (now + timedelta(days=5)).isoformat(),
        'replies': {
          'uuid': '26e12864-1c26-5c3a-9658-97a10f8fea67',
          'handle':  'Worf',
          'message': 'This post has no honor!',
          'created_at': (now - timedelta(days=2)).isoformat()
        }
      }
    ]
    
    # Filter to find the requested activity
    for activity in activities:
      if activity['uuid'] == activity_uuid:
        return activity
    
    # Return None or an error if not found
    return None