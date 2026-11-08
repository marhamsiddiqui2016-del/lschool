from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"ok": True}


@app.get("/{path:path}")
def catch_all(path: str):
    return {"path": path}
