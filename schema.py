# schema.py
import graphene

import db
import make

#################################
#        Type Defs              #
#################################

class Hours(graphene.ObjectType):
     _id = graphene.String()
     worker = graphene.String()
     comment = graphene.String()
     datestamp = graphene.String()
     timeIn = graphene.Float()
     timeOut = graphene.Float()
     castId = graphene.String()
     remote = graphene.Boolean()
     
class Session(graphene.ObjectType):
     slug = graphene.String()
     show = graphene.String()
     hours = graphene.List(Hours)
     active = graphene.Boolean()

class Cast(graphene.ObjectType):
     _id = graphene.String()
     firstName = graphene.String()
     lastName = graphene.String()
     sessions = graphene.List(Session)
     

#################################
#        Mutations              #
#################################

class PunchOut(graphene.Mutation):
    
    newHours = graphene.Field(Hours)
    
    class Arguments:
        
        cast_id = graphene.String()
        timeIn = graphene.Float()
        
    def mutate(self, info, cast_id, timeIn):
        
        hours_result = db.punch_out(cast_id, timeIn)
        
        updated_hours=make.hours(hours_result)
        
        return PunchOut(newHours=updated_hours)


class PunchIn(graphene.Mutation):
    
    newHours = graphene.Field(Hours)
    
    class Arguments:
        
        worker = graphene.String()
        session_slug = graphene.String()
        comment = graphene.String()
        cast_id = graphene.String()
        remote = graphene.Boolean()
        
    def mutate(self, info, worker, session_slug, comment, cast_id, remote):
        
        hours_result = db.punch_in(worker, session_slug, comment, cast_id, remote)
        
        updated_hours=make.hours(hours_result)
        
        return PunchIn(newHours=updated_hours)
        

class AddSessionToCast(graphene.Mutation):
    
    updatedCast = graphene.Field(Cast)
    
    class Arguments:
        
        cast_id = graphene.String()
        session_slug = graphene.String()
        show = graphene.String()
        
    def mutate(self, info, cast_id, session_slug, show):
        
        db.add_session_to_cast(cast_id, session_slug, show)
        
        cast_dict = db.get_single_cast(cast_id)
        
        _updatedCast = make.cast(cast_dict)
        
        return AddSessionToCast(updatedCast=_updatedCast)
        
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
        
        new_cast = make.cast(result)
        
        return CreateCast(addedCast=new_cast)


class Mutations(graphene.ObjectType):
    
    # put the mutation into the root mutation class
    createCast = CreateCast.Field()
    
    addSessionToCast = AddSessionToCast.Field()
    
    punchIn = PunchIn.Field()
    
    punchOut = PunchOut.Field()


#################################
#        Root Query             #
#################################
        

class Query(graphene.ObjectType):
    
    all_cast = graphene.List(Cast)
    
    def resolve_all_cast(self, info):
        
        object_types = []
        
        for result in db.get_all_cast():

            object_types.append(make.cast(result))
            
        return object_types
    
    single_cast = graphene.Field(
        Cast,
        _id=graphene.String()
    )
    
    def resolve_single_cast(self, info, _id):
        
        print(_id)
        
        result = db.get_single_cast(_id)
        
        return make.cast(result)
        
    active_cast = graphene.List(Cast)
    
    def resolve_active_cast(self, info):
        
        _all_cast = []
        
        for result in db.get_active_cast():
            
            _all_cast.append(make.cast(result))
            
        return _all_cast
        

schema = graphene.Schema(query=Query, mutation=Mutations)