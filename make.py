import schema
import db

def hours(data):
    
    h = schema.Hours()
    h.id = data['_id']
    h.worker = data['worker']
    h.comment = data['comment']
    h.datestamp = data['datestamp']
    h.timeOut = data['timeOut']
    h.timeIn = data['timeIn']
    h.castId = data['castId']
    h.remote = data['remote']
    
    return h

def session(data):
    
    s = schema.Session()
    s.id = data['slug']
    s.slug = data['slug']
    s.show = data['show']
    s.active = data['active']
    
    _hours = []
    
    for hour_id in data['hours']:
        
        _hours.append(hours(db.get_single_hours(hour_id)))
        
    s.hours = _hours
    
    return s
    
def cast(data):
    
    c = schema.Cast()
    c.id = data['_id']
    c.firstName = data['firstName']
    c.lastName = data['lastName']
    
    sessions = []
    
    for _session in data['sessions']:
        
        sessions.append(session(_session))
        
    c.sessions = sessions
    
    return c
    
    