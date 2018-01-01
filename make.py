import schema
import db

def hours(data):
    
    h = schema.Hours()
    h._id = data['_id']
    h.worker = data['worker']
    h.comment = data['comment']
    h.datestamp = data['datestamp']
    h.timeOut = data['timeOut']
    h.timeIn = data['timeIn']
    
    return h

def session(data):
    
    s = schema.Session()
    s.slug = data['slug']
    s.show = data['show']
    
    _hours = []
    
    for hour_id in data['hours']:
        
        _hours.append(hours(db.get_single_hours(hour_id)))
        
    s.hours = _hours
    
    return s
    
def cast(data):
    
    c = schema.Cast()
    c._id = data['_id']
    c.firstName = data['firstName']
    c.lastName = data['lastName']
    
    sessions = []
    
    for _session in data['sessions']:
        
        sessions.append(session(_session))
        
    c.sessions = sessions
    
    return c
    
    