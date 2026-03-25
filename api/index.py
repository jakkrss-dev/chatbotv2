import os
import sys

# Ensure the root is in the path
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root not in sys.path:
    sys.path.append(root)

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "Minimal entry point reached", "ver": "4"}

_import_error = None
try:
    from backend.main import app as backend_app
    app.mount("/api", backend_app)
except Exception as e:
    import traceback
    _import_error = {"error": str(e), "trace": traceback.format_exc()}

    @app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
    async def catch_all(request: Request, path: str):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Backend failed to start",
                "detail": _import_error["error"],
                "trace": _import_error["trace"],
                "requested_path": f"/api/{path}",
                "method": request.method,
            }
        )
