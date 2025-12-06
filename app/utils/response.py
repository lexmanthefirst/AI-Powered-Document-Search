from typing import Optional

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def success_response(
    status_code: int,
    message: str,
    data: Optional[dict] = None
) -> JSONResponse:
    """
    Returns a JSON response for success responses.
    
    Args:
        status_code: HTTP status code
        message: Success message
        data: Response data payload (defaults to empty dict)
    
    Returns:
        JSONResponse: Formatted success response
    """
    response_data = {
        "status": "success",
        "status_code": status_code,
        "message": message,
        "data": data or {},  # Ensure data is always a dictionary
    }

    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(response_data)
    )


def fail_response(
    status_code: int,
    message: str,
    context: Optional[dict] = None
) -> JSONResponse:
    """
    Returns a JSON response for failure responses.
    
    Args:
        status_code: HTTP status code
        message: Error message
        context: Additional error context (defaults to empty dict)
    
    Returns:
        JSONResponse: Formatted error response
    """
    response_data = {
        "status": "failure",
        "status_code": status_code,
        "message": message,
        "error": context or {},
    }

    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(response_data)
    )


def validation_error_response(errors: dict) -> JSONResponse:
    """
    Standardized validation error response.
    
    Args:
        errors: Dictionary of validation errors
    
    Returns:
        JSONResponse: Formatted validation error response
    """
    response = {
        "error": "VALIDATION_ERROR",
        "message": "The request contains invalid fields",
        "status_code": 422,
        "errors": errors,
    }

    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(response)
    )
