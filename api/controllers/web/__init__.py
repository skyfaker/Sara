"""
web blueprint and web urls
"""
from flask import Blueprint

web_bp = Blueprint('web_api', __name__, url_prefix='/web_api')


def add_resource():
    """
    Helper function to add a resource to the web API.
    """
    from flask_restx import Api
    from .hello import HelloWorld
    from .completion import Completion
    from .file import UploadFile

    web_api = Api(web_bp)
    web_api.add_resource(HelloWorld, '/hello')
    web_api.add_resource(Completion, '/completion')
    web_api.add_resource(UploadFile, '/upload_file')


add_resource()
