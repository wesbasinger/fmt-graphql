import db

from session import Session
from hours import Hours
from cast import Cast

def session_list(s_list):

    session_objects = []
    
    for session_dict in s_list:
        
        session_objects.append(
            Session(slug=session_dict['slug'], show=session_dict['show'], hours=hour_list(session_dict['hours']))
        )
    
    return session_objects
    
def hour_list(h_list):
    
    hour_objects = []
    
    for hour_dict in h_list:
        
        hour_objects.append(
            Hours(
                _id=hour_dict['_id'], 
                worker=hour_dict['worker'], 
                comment=hour_dict['comment'], 
                datestamp=hour_dict['datestamp'],
                timeIn=hour_dict['timeIn'],
                timeOut=hour_dict['timeOut']
        ))
        
    return hour_objects
