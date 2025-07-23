from flask import request, jsonify
from flask_pydantic import validate
from flask_restx import Resource
from pydantic import BaseModel, ValidationError


class CompletionField(BaseModel):
    name: str
    description: str | None = None


class CompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: list[CompletionField]
    status: str = 200


class CompletionRawPydatic(Resource):
    def post(self):
        try:
            data = request.get_json()
            item = CompletionField(**data).model_dump()
        except ValidationError as e:
            return jsonify({'error': e.errors()}), 400

        res = {
            "id": "cmpl-1234567890",
            "object": "text_completion",
            "created": 1700000000,
            "model": "gpt-3.5-turbo",
            "choices": [
                {
                    "name": item["name"],
                    "description": item.get("description", None)
                }
            ]
        }
        response = CompletionResponse(**res)
        return jsonify(response.dict())


class Completion(Resource):
    @validate()
    def post(self, body: CompletionField):
        name = body.name
        print(name)
        res = {
            "id": "cmpl-1234567890",
            "object": "text_completion",
            "created": 1700000000,
            "model": "gpt-3.5-turbo",
            "choices": [
                {
                    "name": body.name,
                    "description": body.description
                }
            ]
        }
        return CompletionResponse(**res)
