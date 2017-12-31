# cast.py
import graphene

from session import Session

class Cast(graphene.ObjectType):
     _id = graphene.String()
     firstName = graphene.String()
     lastName = graphene.String()
     sessions = graphene.List(Session)

