# session.py
import graphene

from hours import Hours

class Session(graphene.ObjectType):
     slug = graphene.String()
     show = graphene.String()
     hours = graphene.List(Hours)
