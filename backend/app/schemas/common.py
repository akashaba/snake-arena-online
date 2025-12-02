"""Common schemas"""
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    message: str
    code: int | None = None


class ValidationErrorDetail(BaseModel):
    """Validation error detail"""
    field: str
    message: str


class ValidationErrorResponse(BaseModel):
    """Validation error response"""
    error: str = "ValidationError"
    message: str = "Request validation failed"
    details: list[ValidationErrorDetail]
