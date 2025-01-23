from fastapi import FastAPI, HTTPException
from packages import braille, requests
import fastapi.responses as responses
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    try:
        html_content = open("templates/index.html", "r").read()
        return responses.HTMLResponse(content=html_content)
    except:
        return responses.Response(content="Internal Server Error", status_code=404)

@app.get("/static/{file_path}")
def static(file_path: str):
    try:
        return responses.FileResponse(f"static/{file_path}")
    except:
        return responses.Response(content="File not found", status_code=404)
    
@app.post("/api/encode")
def braille_encode(request: requests.Text):
    try:
        return {"encoded": braille.encode(request.text)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/decode")
def braille_decode(request: requests.Braille):
    try:
        return {"decoded": braille.decode(request.braille)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/to-stl")
def to_stl(request: requests.ToSTLRequest):
    try:
        size = request.size if request.size else 2
        spacing = request.spacing if request.spacing else 5
        kerning = request.kerning if request.kerning else 2.5
        subdivisions = request.subdivisions if request.subdivisions else 2
        surface_depth = request.surface_depth if request.surface_depth else 1
        unique_surface = request.unique_surface if request.unique_surface else False
        unique_width = request.unique_width if request.unique_width else False
        text_alignment = request.text_alignment if request.text_alignment else "left"

        stl_file = braille.toSTL(
            request.braille,
            size,
            spacing,
            kerning,
            subdivisions,
            surface_depth,
            unique_surface,
            unique_width,
            text_alignment
        )

        return responses.StreamingResponse(
            stl_file,
            media_type="application/vnd.ms-pkistl",
            headers={"Content-Disposition": f"attachment; filename=output.stl"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))