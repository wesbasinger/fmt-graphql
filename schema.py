# schema.py
import graphene

import db
import expand

from cast import Cast
from hours import Hours
from session import Session

# class PunchIn(graphene.Mutation):
    
#     newHours = graphene.Field(Hours)
    
#     class Arguments:
        
#         worker = graphene.String()
#         session_slug = graphene.String()
#         comment = graphene.String()
#         cast_id = graphene.String()
        
#     def mutate(self, info, worker, session_slug, comment, cast_id):
        
#         result = db.punchIn(worker, session_slug, comment, cast_id)
        
#         hours=Hours(_id=result)
        
#         return PunchIn(newHours=hours)
        

class AddSessionToCast(graphene.Mutation):
    
    updatedCast = graphene.Field(Cast)
    
    class Arguments:
        
        cast_id = graphene.String()
        session_slug = graphene.String()
        show = graphene.String()
        
    def mutate(self, info, cast_id, session_slug, show):
        
        db.add_session_to_cast(cast_id, session_slug, show)
        
        cast_dict = db.get_single_cast(cast_id)
        
        return AddSessionToCast(updatedCast=Cast(
            _id=cast_id, 
            firstName=cast_dict['firstName'], 
            lastName=cast_dict['lastName'], 
            sessions=expand.session_list(cast_dict['sessions'])
        ))
        
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
        
        cast = Cast(_id=result, firstName=first_name, lastName=last_name, sessions=[])
        
        return CreateCast(addedCast=cast)


class Mutations(graphene.ObjectType):
    
    # put the mutation into the root mutation class
    createCast = CreateCast.Field()
    
    addSessionToCast = AddSessionToCast.Field()
    
    # punchIn = PunchIn
        

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

            object_types.append(cast_instance)
            
        return object_types
        

schema = graphene.Schema(query=Query, mutation=Mutations)
