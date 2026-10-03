import io

import c2pa
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Otter Truth API 🦦")

# Allow your browser extension or frontend to make cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"status": "online", "message": "Otter pool is ready for inspection! 🦦"}


def _read_c2pa_manifest(filename: str | None, contents: bytes):
    if not filename:
        return None

    try:
        return c2pa.Reader(filename, io.BytesIO(contents)).json()
    except Exception:
        return None


@app.post("/inspect")
async def inspect_file(file: UploadFile = File(...)):
    contents = await file.read()
    filename = file.filename or "uploaded_file"

    # Tier 1: C2PA Manifest Verification
    c2pa_data = _read_c2pa_manifest(filename, contents)
    has_c2pa = c2pa_data is not None

    return {
        "filename": filename,
        "has_c2pa_manifest": has_c2pa,
        "c2pa_details": c2pa_data,
        "otter_verdict": "Verified Authentic" if has_c2pa else "No C2PA manifest found (Metadata stripped or unsigned).",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)