from fastapi import FastAPI
from .core.config import settings
from .routers import users_router, books_router, loans_router
from .routers.auth import router as auth_router

app = FastAPI(
    title="📚 Library API",
    description=(
        "API de gestion de bibliothèque :\n"
        "- Authentification (JWT)\n"
        "- Gestion des livres (CRUD + recherche)\n"
        "- Emprunts / Retours\n"
        "- Historique des prêts utilisateur"
    ),
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(books_router)
app.include_router(loans_router)

@app.get("/health")
def health():
    return {
        "status": "ok",
        "env": settings.ENV,
        "db": {
            "host": settings.ORACLE_HOST,
            "service": settings.ORACLE_SERVICE
        }
    }
