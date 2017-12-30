# schema.py
import graphene

import db

from cast import Cast
# from hours import Hours
# from session import Session


class Query(graphene.ObjectType):
    
    all_cast = graphene.List(Cast)
    
    def resolve_all_cast(self, info):
        
        db_results = db.get_all_cast()
        
        object_types = []
        
        for result in db.get_all_cast():
            
            cast_instance = Cast()
            cast_instance._id = result['_id']
            cast_instance.firstName = result['firstName']
            cast_instance.lastName = result['lastName']
            
            object_types.append(cast_instance)
            
        return object_types

schema = graphene.Schema(query=Query)
