# hours.py
import graphene

class Hours(graphene.ObjectType):
     _id = graphene.String()
     worker = graphene.String()
     comment = graphene.String()
     datestamp = graphene.String()
     timeIn = graphene.Float()
     timeOut = graphene.Float()
     
     cast = graphene.Field(lambda: Cast)
     session = graphene.Field(lambda: Session)

from session import Session
from cast import Cast

