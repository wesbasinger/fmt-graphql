from pymongo import MongoClient
from bson.objectid import ObjectId
from time import time
from datetime import datetime

client = MongoClient('mongodb://admin:1@ds135547.mlab.com:35547/fmt-graphql')

db = client['fmt-graphql']

cast = db.cast

def get_single_cast(cast_id):
    
    result = cast.find_one({"_id": ObjectId(cast_id)})
    
    result['_id'] = str(result['_id'])
    
    return result
    
    
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
        "sessions" : [],
    })
    
    new_id = str(result.inserted_id)
    
    return get_single_cast(new_id)
    
    
def add_session_to_cast(cast_id, session_slug, show):
    
    cast.update_one(
        {"_id" : ObjectId(cast_id)},
        { "$push" : {"sessions" : {"slug" : session_slug, "show": show, "hours": []}}}
    ) 
    
def get_session(session_slug):
    
    result = sessions.find_one({"slug" : session_slug})
    
    result['_id'] = str(result['_id'])
    
    return result
    
    
def punch_in(worker, slug, comment, cast_id):
    
    ''' arguments:  worker, slug, comment, cast_id '''
    
    # cast.update_one(
    #     {"_id" : ObjectId(cast_id)},
    #     {
    #         "$push" : {
    #             "hours" : {
    #                 "worker" : worker,
    #                 "session" : slug,
    #                 "comment" : comment,
    #                 "datestamp" : str(datetime.now()),
    #                 "timeIn" : time(),
    #                 "timeOut" : 0
    #             }
    #         }
    #     }
    # )
    
    cast.update_one(
        {"_id" : ObjectId(cast_id), "sessions.slug" : slug},
        {
            "$push" : {
                "sessions.$.hours" : {
                    "worker" : worker,
                    "comment" : comment,
                    "datestamp" : str(datetime.now()),
                    "timeIn" : time(),
                    "timeOut" : 0
                }
            }
        }
    )
    
    return get_single_cast(cast_id)