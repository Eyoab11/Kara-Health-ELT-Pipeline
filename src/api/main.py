from fastapi import FastAPI

app = FastAPI(
    title="Medical Data Insights API",
    description="API for querying analytical data from Telegram channels.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Medical Data Insights API"}

# Placeholder for Task 4 endpoints
# GET /api/reports/top-products?limit=10
# GET /api/channels/{channel_name}/activity
# GET /api/search/messages?query=paracetamol