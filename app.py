
import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

MARKETAPI_URL = "https://api.marketapi.app/v1/prices/latest"


@app.get("/")
def home():
    return jsonify({
        "app": "AL FATEH GOLD AI PRO",
        "status": "backend_ready"
    })


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/signal")
def signal():
    api_key = os.environ.get("MARKETAPI_API_KEY")

    if not api_key:
        return jsonify({
            "status": "error",
            "message": "MarketAPI key belum ditetapkan"
        }), 503

    try:
        response = requests.get(
            MARKETAPI_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            params={
                "symbols": "XAUUSD",
                "require_live": "true"
            },
            timeout=15
        )

        if response.status_code != 200:
            return jsonify({
                "status": "error",
                "message": "MarketAPI request gagal",
                "http_status": response.status_code
            }), 502

        result = response.json()
        data = result.get("data", [])

        quote = next(
            (item for item in data
             if item.get("symbol") == "XAUUSD"),
            None
        )

        if not quote:
            return jsonify({
                "symbol": "XAUUSD",
                "status": "NO_LIVE_DATA",
                "signal": "NO_SIGNAL",
                "message": "Tiada harga LIVE tersedia"
            }), 200

        return jsonify({
            "symbol": "XAUUSD",
            "status": quote.get("status"),
            "time": quote.get("time"),
            "bid": quote.get("bid"),
            "ask": quote.get("ask"),
            "signal": "NO_SIGNAL",
            "message": "Harga LIVE diterima; strategi signal belum dipasang"
        })

    except requests.RequestException:
        return jsonify({
            "status": "error",
            "message": "Sambungan MarketAPI gagal"
        }), 502


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
