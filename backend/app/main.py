from fastapi import FastAPI
from app.routes import ticket

app = FastAPI()

# Register routers
app.include_router(ticket.router, prefix="/tickets", tags=["Tickets"])

@app.get("/")
async def root():
    return {"message": "SmartTicket API is running"}
