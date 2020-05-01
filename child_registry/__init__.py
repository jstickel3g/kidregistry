# Import the necessary frameworks
import markdown
import os
import shelve
import datetime

from flask import Flask, g
from flask_restful import Resource, Api, reqparse
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# Create an instance of flask
app = Flask(__name__)
app.config["DEBUG"] = True

api = Api(app)

print( "Initializing..." )

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("children.db")

    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    print( "Request received..." )

    """ Present some documentation about this service """

    # Show the README for this service
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

        # Read the content of the file
        content = markdown_file.read()

        #convet to HTML
        return markdown.markdown(content)


class Children (Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())

        children = []

        for key in keys:
            children.append(shelf[key])

        return {'message': 'Success', 'data': children }, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('name', required=True)
        parser.add_argument('gender', required=True)
        parser.add_argument('dob', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        #Calculate Age in years
        dob = datetime.strptime(args['dob'], '%m/%d/%Y').date()
        today = date.today()
        age = relativedelta(today, dob).years
        args['age'] = str(age)
    
        shelf = get_db()
        shelf[args['name']] = args

        return {'message': 'Child is registered', 'data': args}, 201

    def delete(self):

        shelf = get_db()
        keys = list(shelf.keys())

        for key in keys:
            del shelf[key]

        return {'message': 'All Children Deleted', 'data': list(shelf.keys()) }, 204

class Child (Resource):
    def get(self, name):
        shelf = get_db()

        # If the key doesn't exist in the DB, return a 404
        if not (name in shelf):
            return {'message': 'Child named ' + name + ' has not been registered', 'data': {}}, 404

        return {'message': 'Child found! ', 'data': shelf[name]}, 404

    def delete(self, name):
        shelf = get_db()

        # If the name of the kid doesn't exist, return a 404
        if not (name in shelf):
            return {'message': 'Child named ' + name + ' has not been registered', 'data': {}}, 404

        del shelf[name]

        return {'message': 'Child named ' + name + ' has been deleted'}, 204

api.add_resource(Children, '/children')
api.add_resource(Child,    '/child/<string:name>')
