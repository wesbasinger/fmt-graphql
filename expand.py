import db

from session import Session
from hours import Hours
from cast import Cast

def single_cast(cast_id):
    
    result = db.get_single_cast(cast_id)
    
    return Cast(_id=cast_id, firstName=result['firstName'], lastName=result['lastName'], sessions=result['sessions'], hours=result['hours'])

def single_session(slug):
    
    session_dict = db.get_session(slug)
    
    return Session(slug=session_dict['slug'], show=session_dict['show'])

def session_list(s_list):

    session_objects = []
    
    for session_slug in s_list:
        
        session_dict = db.get_session(session_slug)
        
        session_objects.append(
            Session(slug=session_dict['slug'], show=session_dict['show'])
        )
    
    return session_objects
    
def hour_list(h_list, cast_id):
    
    hour_objects = []
    
    for hour_id in h_list:
        
        hour_dict = db.get_hour(hour_id)
        
        hour_objects.append(
            Hours(
                _id=hour_id, 
                worker=hour_dict['worker'], 
                comment=hour_dict['comment'], 
                datestamp=hour_dict['datestamp'],
                timeIn=hour_dict['timeIn'],
                timeOut=hour_dict['timeOut'],
                session=single_session(hour_dict['session']),
                cast=single_cast(cast_id))
        )
        
    return hour_objects
    

        
        
        