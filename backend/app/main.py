import uvicorn

from fastapi import FastAPI
from .api import auth, events_owner, events_public
from .db import engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "This is our backend!"}

app.include_router(auth.router)
app.include_router(events_owner.router)
app.include_router(events_public.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)