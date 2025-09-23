from app.routers.users import router as users_router
from app.routers.books import router as books_router
from app.routers.loans import router as loans_router
__all__ = ["users_router", "books_router", "loans_router"]
