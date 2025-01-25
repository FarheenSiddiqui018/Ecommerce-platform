import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routers import products, orders

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    if os.getenv("TESTING") != "1":
        init_db()
        print("DEBUG: init_db() called during startup (lifespan)")

    yield

    # Teardown logic (optional)
    print("DEBUG: No teardown steps currently.")

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    app = FastAPI(
        title="Simple E-Commerce Platform",
        version="1.0.0",
        redirect_slashes=False,
        lifespan=lifespan  # Use the new lifespan approach
    )

    # Mount your static directory
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    # Configure CORS to allow requests from your UI
    origins = [
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "file://",
        "*",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include Routers
    app.include_router(products.router)
    app.include_router(orders.router)

    return app

app = create_app()
