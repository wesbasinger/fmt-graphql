# schema.py
import graphene

from cast import Cast
from hours import Hours
from session import Session


class Query(graphene.ObjectType):
     
     cast = graphene.Field(Cast)

schema = graphene.Schema(query=Query)
