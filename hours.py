# hours.py
import graphene

class Hours(graphene.ObjectType):
     _id = graphene.String()
     worker = graphene.String()
     comment = graphene.String()
     datestamp = graphene.String()
     timeIn = graphene.Float()
     timeOut = graphene.Float()
