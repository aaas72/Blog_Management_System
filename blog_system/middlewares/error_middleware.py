from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from utils.exceptions import AppError
from utils.responses import standard_response
import uuid
import traceback

async def global_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    
    if isinstance(exc, AppError):
        return JSONResponse(
            status_code=exc.status_code,
            content=standard_response(
                success=False,
                error={"code": exc.code, "message": exc.message},
                request_id=request_id
            )
        )
    
    if isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=standard_response(
                success=False,
                error={"code": "VALIDATION_ERROR", "message": str(exc.errors())},
                request_id=request_id
            )
        )

    # Unexpected error
    print(f"Unexpected error: {str(exc)}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=standard_response(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": "An unexpected error occurred"},
            request_id=request_id
        )
    )

def add_exception_handlers(app):
    app.add_exception_handler(Exception, global_exception_handler)
    app.add_exception_handler(AppError, global_exception_handler)
    app.add_exception_handler(RequestValidationError, global_exception_handler)
