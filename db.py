from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://admin:1@ds135547.mlab.com:35547/fmt-graphql')

db = client['fmt-graphql']

cast = db.cast

sessions = db.sessions

def get_all_cast():
    
    cursor = cast.find()
    
    results = []
    
    for doc in cursor:
        
        doc['_id'] = str(doc['_id'])
        
        results.append(doc)
        
    return results
    
def add_new_cast(first_name, last_name):
    
    result = cast.insert_one({
        "firstName" : first_name,
        "lastName" : last_name,
        "sessions" : []
    })
    
    return str(result.inserted_id)
    
def add_cast_to_session(cast_id, session_slug):
    
    sessions.update_one(
        {"slug": session_slug},
        { "$push" : { "cast" : cast_id } }
    )
    
def add_session_to_cast(cast_id, session_slug):
    
    cast.update_one(
        {"_id" : ObjectId(cast_id)},
        { "$push" : {"sessions" : session_slug}}
    )
    
def get_session(session_slug):
    
    result = sessions.find_one({"slug" : session_slug})
    
    result['_id'] = str(result['_id'])
    
    return result
    