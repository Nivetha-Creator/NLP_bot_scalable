def main() -> None:
    import uvicorn

    from nlp_bot_scalable.config.settings import settings

    uvicorn.run(
        "nlp_bot_scalable.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.app_env == "development",
    )
