from fastapi import FastAPI

from orinfra_sentinelops.presentation.api.routes.incidents import router as incidents_router


def create_app() -> FastAPI:
    """Create and configure the SentinelOps FastAPI application."""
    app = FastAPI(
        title="Orinfra SentinelOps",
        description=(
            "Evidence-first platform for causal investigation "
            "and safe remediation of production AI incidents."
        ),
        version="0.1.0",
    )

    @app.get("/health", tags=["system"])
    async def health() -> dict[str, str]:
        """Return the application health status."""
        return {"status": "ok"}

    app.include_router(incidents_router)

    return app


app = create_app()
