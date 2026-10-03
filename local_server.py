"""
本地全端伺服器：靜態 output/ ＋ POST /api/chat
執行：python3 local_server.py   →  http://localhost:8000
"""
import json
import os
import sys
import urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
sys.path.insert(0, BASE_DIR)

from ir_autopilot.src.ai.proactive_agent import ProactiveAgent  # noqa: E402

PORT = int(os.getenv("PORT", "8000"))
STATIC_DIR = os.path.join(BASE_DIR, "output")
ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN", "*")
MAX_BODY = 6 * 1024 * 1024          # 6 MB（含 Base64 截圖）
MAX_MSG = 2000

agent = ProactiveAgent()


def _valid_image(s):
    return isinstance(s, str) and s.startswith("data:image/") and ";base64," in s[:40] and len(s) <= 5 * 1024 * 1024


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=STATIC_DIR, **kw)

    def _json(self, code, obj):
        b = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.send_header("Access-Control-Allow-Origin", ALLOWED_ORIGIN)
        self.end_headers()
        self.wfile.write(b)

    def do_POST(self):
        if urllib.parse.urlparse(self.path).path != "/api/chat":
            return self._json(404, {"error": "not found"})
        n = int(self.headers.get("Content-Length", 0))
        if n <= 0 or n > MAX_BODY:
            return self._json(413, {"error": "請求過大或為空"})
        try:
            payload = json.loads(self.rfile.read(n).decode("utf-8"))
        except Exception:
            return self._json(400, {"error": "JSON 格式錯誤"})

        msg = str(payload.get("message", ""))[:MAX_MSG]
        image = payload.get("image")
        if image is not None and not _valid_image(image):
            return self._json(400, {"error": "image 須為 data:image/*;base64 且 ≤ 5MB"})
        history = payload.get("history") or []
        ctx = {"slug": payload.get("slug"), "default_slug": payload.get("default_slug", "ib")}
        try:
            return self._json(200, agent.process_chat(msg, ctx, history=history, image=image))
        except Exception as e:
            return self._json(500, {"error": str(e), "response": "伺服器處理錯誤"})

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", ALLOWED_ORIGIN)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, fmt, *args):
        line = fmt % args if args else fmt
        if "/api/" in line or "code 5" in line:
            super().log_message(fmt, *args)


if __name__ == "__main__":
    os.makedirs(STATIC_DIR, exist_ok=True)
    print(f"IR Autopilot  http://localhost:{PORT}   model={agent.client.model if agent.client.available else '未設定（僅數據模式）'}")
    try:
        ThreadingHTTPServer(("", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        pass
