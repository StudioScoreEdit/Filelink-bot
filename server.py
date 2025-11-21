import os
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from dotenv import load_dotenv

load_dotenv()
DOWNLOAD_DIR = Path(os.getenv("DOWNLOAD_DIR", "downloads"))
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI()

def iter_file(path, start=0, end=None, chunk_size=8192):
    with open(path, "rb") as f:
        f.seek(start)
        remaining = None if end is None else (end - start + 1)
        while True:
            if remaining is None:
                chunk = f.read(chunk_size)
            else:
                to_read = min(chunk_size, remaining)
                chunk = f.read(to_read)
                remaining -= len(chunk)
            if not chunk:
                break
            yield chunk

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/d/{file_id}/{filename}")
async def serve_file(request: Request, file_id: str, filename: str):
    candidate = DOWNLOAD_DIR / f"{file_id}_{filename}"
    if not candidate.exists():
        raise HTTPException(status_code=404, detail="File not found")

    size = candidate.stat().st_size
    range_header = request.headers.get("range")

    if range_header:
        try:
            _, r = range_header.split("=")
            start_s, end_s = r.split("-")
            start = int(start_s)
            end = int(end_s) if end_s else size - 1
        except:
            raise HTTPException(status_code=416, detail="Invalid Range")

        length = end - start + 1
        headers = {
            "Content-Range": f"bytes {start}-{end}/{size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(length),
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
        return StreamingResponse(iter_file(str(candidate), start, end), status_code=206, headers=headers)

    return FileResponse(str(candidate), filename=filename)
