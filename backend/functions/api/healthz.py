"""ヘルスチェックエンドポイント"""
from datetime import datetime
from firebase_functions import https_fn
from flask import jsonify


def cors_response(data, status_code=200):
    """CORSヘッダー付きレスポンスを作成"""
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
    }
    response = jsonify(data)
    for key, value in cors_headers.items():
        response.headers[key] = value
    response.status_code = status_code
    return response


def handle_healthz(req: https_fn.Request) -> https_fn.Response:
    """ヘルスチェックエンドポイント"""
    if req.method == 'OPTIONS':
        return cors_response({}, 204)
    
    return cors_response({
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "wb-backend"
    })

