"""ヘルスチェックエンドポイント"""
from fastapi import APIRouter
from datetime import datetime
from typing import Dict

router = APIRouter()


@router.get("/healthz", tags=["health"])
async def health_check() -> Dict[str, str]:
    """ヘルスチェックエンドポイント"""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "wb-backend"
    }

