
from fastapi import FastAPI
from sqlmodel import Field
from routers import itemcurd
from database import create_db_and_tables
import uvicorn


app = FastAPI()

# Register the router
app.include_router(itemcurd.router)

# Create tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


if __name__ == "__main__":    
    uvicorn.run(app, host="0.0.0.0", port=8001)
