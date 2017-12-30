# session.py
import graphene

class Session(graphene.ObjectType):
     slug = graphene.String()
     show = graphene.String()
     
     cast = graphene.Field(lambda: Cast)

from cast import Cast
