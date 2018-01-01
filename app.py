from flask import Flask
from graphene import ObjectType, String, Schema
from flask_graphql import GraphQLView
from flask_cors import CORS


from schema import schema

view_func = GraphQLView.as_view('graphql', schema=schema, graphiql=True)

app = Flask(__name__)
CORS(app)
app.add_url_rule('/', view_func=view_func)

if __name__ == '__main__':
    app.run()
