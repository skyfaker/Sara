from flask import request
import logging
from flask_restx import Resource
from pydantic import BaseModel, ValidationError, Field
from flask_pydantic import validate
from services.file_service import FileService, FileTooLargeError, UnsupportedFileTypeError


class UploadFileField(BaseModel):
    user_id: str = 'Default'
    file: bytes
    filename: str
    mimetype: str


class RequestFormDataModel(BaseModel):
    user_id: str = Field(..., description="The ID of the user uploading the file")


class UploadFileResponse(BaseModel):
    message: str = "File uploaded successfully"
    status: int = 200


class UploadFile(Resource):
    @validate()
    def post(self, form: RequestFormDataModel) -> UploadFileResponse:
        # Here you would typically handle the file upload logic
        file = request.files["file"]
        filename = file.filename
        user_id = form.user_id
        try:
            upload_file = FileService.upload_file(
                filename=filename,
                content=file.read(),
                user_id=user_id
            )
            logging.info("Upload file: {} success".format(filename))
        except FileTooLargeError as e:
            logging.error('{}'.format(e))
            response = {
                "message": e.message,
                "status": 201,
            }
            return UploadFileResponse(**response)
        except UnsupportedFileTypeError as e:
            logging.error('{}'.format(e))
            response = {
                "message": e.message,
                "status": 201,
            }
            return UploadFileResponse(**response)

        response = {
            "message": "File uploaded successfully",
            "status": 200,
        }
        return UploadFileResponse(**response)
