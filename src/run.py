import uvicorn


# запуск uvicorn-сервера
if __name__ == "__main__":
    uvicorn.run("src.api.app:create_app", host="0.0.0.0", port=8000, factory=True)
