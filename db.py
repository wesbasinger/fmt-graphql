from pymongo import MongoClient

client = MongoClient('mongodb://admin:1@ds135547.mlab.com:35547/fmt-graphql')

db = client['fmt-graphql']

cast = db.cast

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
        "lastName" : last_name
    })
    
    return str(result.inserted_id)