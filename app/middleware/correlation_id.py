import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.core.logging import logger, set_correlation_id, clear_correlation_id


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to extract or generate correlation IDs for request tracing.
    
    The correlation ID can be:
    1. Provided by client via X-Correlation-ID header
    2. Auto-generated if not provided
    
    The correlation ID is:
    - Added to response headers
    - Set in context for logging
    - Logged for each request
    - Cleaned up after request completes
    """
    
    def __init__(self, app, correlation_id_header: str = "X-Correlation-ID"):
        """
        Initialize middleware with custom header name.
        
        Args:
            app: FastAPI application
            correlation_id_header: Header name for correlation ID (default: X-Correlation-ID)
        """
        super().__init__(app)
        self.correlation_id_header = correlation_id_header
    
    async def dispatch(self, request: Request, call_next):
        """
        Process the request and add correlation ID.
        
        Args:
            request: The incoming request
            call_next: The next middleware or endpoint
            
        Returns:
            Response with correlation ID header
        """
        # Extract correlation ID from request headers (case-insensitive)
        correlation_id = (
            request.headers.get(self.correlation_id_header) or
            request.headers.get(self.correlation_id_header.lower())
        )
        
        # Generate new correlation ID if not provided
        if not correlation_id:
            correlation_id = str(uuid.uuid4())
        
        # Set correlation ID in context for logging
        set_correlation_id(correlation_id)
        
        # Log incoming request
        logger.info(
            "Incoming %s %s from %s",
            request.method,
            request.url.path,
            request.client.host if request.client else "unknown"
        )
        
        try:
            # Process request
            response: Response = await call_next(request)
            
            # Add correlation ID to response headers for client tracking
            response.headers[self.correlation_id_header] = correlation_id
            
            # Log response status
            logger.info(
                "Completed %s %s with status %s",
                request.method,
                request.url.path,
                response.status_code
            )
            
            return response
            
        except Exception as e:
            # Log error with correlation ID
            logger.error(
                "Error processing %s %s: %s",
                request.method,
                request.url.path,
                str(e),
                exc_info=True
            )
            raise
        finally:
            # Context cleanup after request completes
            clear_correlation_id()
