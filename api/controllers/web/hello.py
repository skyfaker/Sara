from flask_restx import Resource


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


def hello_world():
    """
    View function to return a simple hello world message.
    """
    return {'message': 'Hello, World!'}
