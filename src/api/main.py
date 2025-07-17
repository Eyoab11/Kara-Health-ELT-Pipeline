from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
from src.api import database, schemas, crud

app = FastAPI(title="Kara Analytical API")

@app.get("/api/reports/top-products", response_model=List[schemas.TopProduct])
def get_top_products(limit: int = 10):
    return crud.get_top_products(limit)

@app.get("/api/channels/{channel_name}/activity", response_model=schemas.ChannelActivity)
def get_channel_activity(channel_name: str):
    result = crud.get_channel_activity(channel_name)
    if not result:
        raise HTTPException(status_code=404, detail="Channel not found or no activity.")
    return result

@app.get("/api/search/messages", response_model=List[schemas.MessageSearchResult])
def search_messages(query: str = Query(..., min_length=1)):
    return crud.search_messages(query)