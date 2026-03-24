import os
import sys

# Ensure the root is in the path
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root not in sys.path:
    sys.path.append(root)

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "Minimal entry point reached", "ver": "3"}

try:
    from backend.main import app as backend_app
    app.mount("/api", backend_app)
except Exception as e:
    import traceback
    error_msg = str(e)
    error_trace = traceback.format_exc()
    @app.get("/api/crash")
    async def crash():
        return JSONResponse(status_code=500, content={"error": error_msg, "trace": error_trace})
