# cast.py
import graphene

class Cast(graphene.ObjectType):
     _id = graphene.String()
     firstName = graphene.String()
     lastName = graphene.String()
     
     # sessions = graphene.List(lambda: Session)
     # hours = graphene.List(lambda: Hours)

# from session import Session
# from hours import Hours

