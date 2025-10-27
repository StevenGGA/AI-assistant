"""
Database dependencies for FastAPI
"""
from app.database import get_db

# Re-export for convenience
__all__ = ["get_db"]