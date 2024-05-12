import uvicorn


if __name__ == "__main__":
    uvicorn.run('overseer.main:app', reload=True)
