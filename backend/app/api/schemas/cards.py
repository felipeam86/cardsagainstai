from pydantic import BaseModel


class BlackCard(BaseModel):
    id: int
    text: str
    pick: int
    watermark: str | None


class WhiteCard(BaseModel):
    id: int
    text: str
    watermark: str | None
