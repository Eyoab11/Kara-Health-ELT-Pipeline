from pydantic import BaseModel
from typing import List, Optional

class TopProduct(BaseModel):
    product: str
    count: int

class ChannelActivity(BaseModel):
    channel_name: str
    total_messages: int
    messages_per_day: List[dict]

class MessageSearchResult(BaseModel):
    message_id: int
    channel_name: str
    message_date: str
    text: str