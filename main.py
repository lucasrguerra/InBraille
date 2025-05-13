from fastapi import FastAPI, HTTPException
from packages import braille, requests
import fastapi.responses as responses
import uvicorn



PORT = 3000
app = FastAPI()



@app.get("/")
def homePtBr():
    try:
        html_content = open("templates/index_pt_br.html", "r", encoding="utf-8").read()
        return responses.HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")
    except:
        return responses.Response(content="Internal Server Error", status_code=404)



@app.get("/en")
def homeEn():
    try:
        html_content = open("templates/index_en.html", "r", encoding="utf-8").read()
        return responses.HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")
    except:
        return responses.Response(content="Internal Server Error", status_code=404)



@app.get("/public/{file_path}")
def static(file_path: str):
    try:
        if file_path == "style.css":
            style_content = open(f"public/{file_path}", "r", encoding="utf-8").read()
            return responses.HTMLResponse(content=style_content, media_type="text/css; charset=utf-8")
        elif file_path == "script.js":
            script_content = open(f"public/{file_path}", "r", encoding="utf-8").read()
            return responses.HTMLResponse(content=script_content, media_type="text/javascript; charset=utf-8")
        else:
            return responses.FileResponse(f"public/{file_path}")
    except:
        return responses.Response(content="File not found", status_code=404)



@app.post("/api/encode")
def braille_encode(request: requests.Text):
    try:
        alphabet = request.alphabet if request.alphabet else "North American"

        return {"encoded": braille.encode(request.text, alphabet)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/api/decode")
def braille_decode(request: requests.Braille):
    try:
        alphabet = request.alphabet if request.alphabet else "North American"

        return {"decoded": braille.decode(request.braille, alphabet)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/api/to-stl")
def to_stl(request: requests.ToSTLRequest):
    try:
        unique_plate = request.unique_plate if request.unique_plate else False
        symbols_per_line = request.symbols_per_line if request.symbols_per_line else 22
        if symbols_per_line < 8:
            symbols_per_line = 8
        elif symbols_per_line > 50:
            symbols_per_line = 50

        text_alignment = request.text_alignment if request.text_alignment else "left"
        rounded = request.rounded if request.rounded else False
        resolution = request.resolution if request.resolution else 20
        if resolution < 15:
            resolution = 15
        elif resolution > 50:
            resolution = 50

        plate_thickness = request.plate_thickness if request.plate_thickness else 2
        if plate_thickness < 2:
            plate_thickness = 2
        elif plate_thickness > 100:
            plate_thickness = 100

        stl_file = braille.toSTL(
            request.braille,
            resolution,
            plate_thickness,
            unique_plate,
            symbols_per_line,
            text_alignment,
            rounded
        )

        return responses.StreamingResponse(
            stl_file,
            media_type="application/vnd.ms-pkistl",
            headers={"Content-Disposition": f"attachment; filename=output.stl"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")