"""
OpenRouter client（精簡版）
- 啟動時驗證模型是否存在；不存在直接拋錯，不做靜默 fallback。
- 連線失敗回傳 success=False；由代理人決定如何呈現，絕不在此生成內容。
"""
import os
from typing import Any, Dict, List, Optional

import requests


class ModelUnavailable(RuntimeError):
    pass


class OpenRouterClient:
    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    MODELS_URL = "https://openrouter.ai/api/v1/models"

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, validate: bool = True):
        self._load_dotenv()
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY") or ""
        self.model = model or os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash")
        self.fallback_model = os.getenv("OPENROUTER_FALLBACK_MODEL", "")
        self.enable_reasoning = os.getenv("OPENROUTER_REASONING", "false").lower() == "true"
        self.timeout = int(os.getenv("OPENROUTER_TIMEOUT", "40"))
        self.available = bool(self.api_key) and "your_openrouter_api_key_here" not in self.api_key
        self.model_ok: Optional[bool] = None
        if self.available and validate:
            self.validate_models()

    @staticmethod
    def _load_dotenv() -> None:
        path = os.path.join(os.getcwd(), ".env")
        if not os.path.exists(path):
            return
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": os.getenv("SITE_URL", "http://localhost:8000"),
            "X-Title": os.getenv("SITE_NAME", "NUTC-IR-Autopilot"),
        }

    def validate_models(self) -> None:
        try:
            resp = requests.get(self.MODELS_URL, headers=self._headers(), timeout=15)
            ids = {m.get("id") for m in resp.json().get("data", [])}
        except Exception as e:
            print(f"[OpenRouter] 無法取得模型清單：{e}（略過驗證）")
            self.model_ok = None
            return
        if self.model not in ids:
            raise ModelUnavailable(f"OPENROUTER_MODEL='{self.model}' 不在 OpenRouter 模型清單中。請改 .env。")
        if self.fallback_model and self.fallback_model not in ids:
            print(f"[OpenRouter] 警告：備用模型 '{self.fallback_model}' 不存在，已停用備用。")
            self.fallback_model = ""
        self.model_ok = True
        print(f"[OpenRouter] 模型驗證通過：{self.model}")

    def chat(self, messages: List[Dict[str, Any]], system_prompt: Optional[str] = None,
             image_data_url: Optional[str] = None) -> Dict[str, Any]:
        if not self.available:
            return {"success": False, "error": "未設定 OPENROUTER_API_KEY"}

        full: List[Dict[str, Any]] = []
        if system_prompt:
            full.append({"role": "system", "content": system_prompt})
        if image_data_url and messages:
            last = messages[-1]
            full.extend(messages[:-1])
            full.append({"role": last.get("role", "user"), "content": [
                {"type": "text", "text": last.get("content", "")},
                {"type": "image_url", "image_url": {"url": image_data_url}},
            ]})
        else:
            full.extend(messages)

        for model in [self.model] + ([self.fallback_model] if self.fallback_model else []):
            payload: Dict[str, Any] = {"model": model, "messages": full, "temperature": 0.2}
            if self.enable_reasoning:
                payload["reasoning"] = {"enabled": True}
            try:
                resp = requests.post(self.API_URL, headers=self._headers(), json=payload, timeout=self.timeout)
                data = resp.json()
            except Exception as e:
                last_err = f"{model}: {e}"
                continue
            if resp.status_code != 200 or "error" in data or not data.get("choices"):
                last_err = f"{model}: HTTP {resp.status_code} {data.get('error', {}).get('message', '')}"
                continue
            msg = data["choices"][0].get("message", {})
            reasoning = msg.get("reasoning") or msg.get("reasoning_details")
            if isinstance(reasoning, list):
                reasoning = "\n".join(r.get("text", "") if isinstance(r, dict) else str(r) for r in reasoning)
            return {"success": True, "content": msg.get("content", ""), "reasoning": reasoning or None,
                    "model": data.get("model", model), "usage": data.get("usage")}
        return {"success": False, "error": last_err}
