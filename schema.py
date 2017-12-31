# schema.py
import graphene

import db
import expand

from cast import Cast
from hours import Hours
from session import Session

class PunchIn(graphene.Mutation):
    
    newHours = graphene.Field(Hours)
    
    class Arguments:
        
        worker = graphene.String()
        session_slug = graphene.String()
        comment = graphene.String()
        cast_id = graphene.String()
        
    def mutate(self, info, worker, session_slug, comment, cast_id):
        
        result = db.punch_in(worker, session_slug, comment, cast_id)
        
        hours=Hours(_id=result)
        
        return PunchIn(newHours=hours)

class AddSessionToCast(graphene.Mutation):
    
    updatedCast = graphene.Field(Cast)
    
    class Arguments:
        
        cast_id = graphene.String()
        session_slug = graphene.String()
        
    def mutate(self, info, cast_id, session_slug):
        
        db.add_cast_to_session(cast_id, session_slug)
        db.add_session_to_cast(cast_id, session_slug)
        
        cast=Cast(_id=cast_id)
        
        return AddSessionToCast(updatedCast=cast)
        
class CreateCast(graphene.Mutation):
    
    # instantiate an object to return
    addedCast = graphene.Field(Cast)
    
    # pass in arguments
    class Arguments:
        
        first_name = graphene.String()
        last_name = graphene.String()
    
    # this function does the database insert, instantiates another
    # Cast object and sets the first addedCast equal to the second cast
    # that has new values in it
    def mutate(self, info, first_name, last_name):
        
        result = db.add_new_cast(first_name, last_name)
        
        cast = Cast(_id=result, firstName=first_name, lastName=last_name, sessions=[], hours=[])
        
        return CreateCast(addedCast=cast)


class Mutations(graphene.ObjectType):
    
    # put the mutation into the root mutation class
    createCast = CreateCast.Field()
    
    addSessionToCast = AddSessionToCast.Field()
    
    punchIn = PunchIn.Field()
        

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
            cast_instance.sessions = expand.session_list(result['sessions'])
            cast_instance.hours = expand.hour_list(result['hours'], result['_id'])
                
            object_types.append(cast_instance)
            
        return object_types

schema = graphene.Schema(query=Query, mutation=Mutations)
