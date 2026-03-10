from flask import request, jsonify
from flask_pydantic import validate
from flask_restx import Resource
from pydantic import BaseModel, ValidationError


class ChatField(BaseModel):
    name: str
    description: str | None = None


class ChatResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: list[ChatField]
    status: int = 200


class Chat(Resource):
    @validate()
    def post(self, body: ChatField):
        name = body.name
        test_res = {"id": "chatcmpl-123"}
        return ChatResponse(**test_res)
