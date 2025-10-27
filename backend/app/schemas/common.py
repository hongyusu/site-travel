"""Common Pydantic schemas."""

from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = Field(default=1, ge=1, description="Page number")
    per_page: int = Field(default=20, ge=1, le=100, description="Items per page")

    @property
    def offset(self) -> int:
        """Calculate offset for database query."""
        return (self.page - 1) * self.per_page


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response."""
    success: bool = True
    data: List[T]
    message: Optional[str] = None
    pagination: dict

    class Config:
        from_attributes = True

    @staticmethod
    def create(data: List[T], page: int, per_page: int, total: int, message: Optional[str] = None):
        """Create a paginated response."""
        total_pages = (total + per_page - 1) // per_page
        return PaginatedResponse(
            data=data,
            message=message,
            pagination={
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
        )


class MessageResponse(BaseModel):
    """Simple message response."""
    success: bool = True
    message: str
    data: Optional[dict] = None