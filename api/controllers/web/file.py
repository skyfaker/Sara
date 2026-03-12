from flask import request
import logging
from flask_restx import Resource
from pydantic import BaseModel, Field
from flask_pydantic import validate
from configs import app_config
from services.file_service import FileService, FileTooLargeError, UnsupportedFileTypeError
from extensions.ext_storage import storage


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
    indexed: bool = False


class UploadFile(Resource):
    @validate()
    def post(self, form: RequestFormDataModel) -> UploadFileResponse:
        file = request.files["file"]
        filename = file.filename
        user_id = form.user_id
        indexed = False
        
        try:
            # Prevent OOM: check content length before reading
            if request.content_length and request.content_length > app_config.FILE_SIZE_LIMIT * 1024 * 1024:
                raise FileTooLargeError()

            if not filename:
                raise ValueError("Filename is required")

            file_info = FileService.upload_file(
                filename=filename,
                content=file.read(),
                user_id=user_id
            )
            logging.info(f"Upload file: {filename} success, uuid: {file_info['file_uuid']}")
            
            # Auto-index for supported document types
            if file_info["extension"] in ["docx"]:
                try:
                    from core.rag.file_loader.docling_loader import DoclingLoader
                    from core.rag.file_indexer import FileIndexer
                    
                    # Load file from storage
                    file_path = storage.load(file_info["file_key"])
                    
                    # Load and chunk document
                    loader = DoclingLoader()
                    documents = loader.load_file(file_path)
                    logging.info(f"Loaded {len(documents)} document chunks from {filename}")
                    
                    # Index documents
                    indexer = FileIndexer()
                    index_path = indexer.index_documents_sync(
                        documents=documents,
                        source_file=filename,
                        file_id=file_info["file_uuid"]
                    )
                    logging.info(f"Indexed file saved to {index_path}")
                    indexed = True
                    
                except Exception as e:
                    logging.error(f"Failed to index file {filename}: {e}")
                    # Continue even if indexing fails - file is still uploaded
            
        except FileTooLargeError as e:
            logging.error('{}'.format(e))
            response = {
                "message": e.message,
                "status": 413,
            }
            return UploadFileResponse(**response)
        except UnsupportedFileTypeError as e:
            logging.error('{}'.format(e))
            response = {
                "message": e.message,
                "status": 415,
            }
            return UploadFileResponse(**response)
        except ValueError as e:
            logging.error('{}'.format(e))
            response = {
                "message": str(e),
                "status": 400,
            }
            return UploadFileResponse(**response)

        response = {
            "message": "File uploaded successfully",
            "status": 200,
            "indexed": indexed,
        }
        return UploadFileResponse(**response)
