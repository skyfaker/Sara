"""
web blueprint and web urls
"""

from flask import Blueprint

web_bp = Blueprint("web_api", __name__, url_prefix="/api")


def add_resource():
    """
    Helper function to add a resource to the web API.
    """
    from flask_restx import Api
    from .hello import HelloWorld
    from .chat import Chat
    from .file import UploadFile
    from .rag import RAGQuery

    web_api = Api(web_bp)
    web_api.add_resource(HelloWorld, "/hello")
    web_api.add_resource(Chat, "/chat")
    web_api.add_resource(UploadFile, "/upload_file")
    web_api.add_resource(RAGQuery, "/rag/query")


add_resource()
