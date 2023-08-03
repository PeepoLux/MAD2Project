import os
from flask import Flask
import config
from config import LocalDevelopmentConfig
from database import db
from flask_restful import Api
from flask_cors import CORS


app = None
api = None

def create_app():
    app = Flask(__name__)
    CORS(app)
    if os.getenv('ENV',"development") == "production":
        raise Exception("Currently no production confi is set up.")
    else:
        print("Starting local development")
        app.config.from_object(LocalDevelopmentConfig)
    
    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    
    return app,api


app,api = create_app()

from controllers import *
from api import *



#------------------------------------API------------------------------------------
api.add_resource(VenueAPI, "/api/venue", "/api/venue/<string:venue_name>")
api.add_resource(ShowAPI, "/api/shows", "/api/shows/<int:show_id>")
api.add_resource(MakeBooking, "/api/makebooking")

if __name__ == '__main__':
    app.run(threaded=True,debug=True)