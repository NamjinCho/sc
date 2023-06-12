from fastapi import FastAPI, Request
from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from urllib import parse
import uvicorn

app = FastAPI(
    title="sc",
)
app.mount("/static", StaticFiles(directory="static"), name="static")
from fastapi import FastAPI

app = FastAPI()
print("ssibala")

@app.get("/api", response_class=HTMLResponse)
async def api(request: Request):
    print(request)
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        request.method,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in request.query_params.items()),
        request.body,
    ))
    
    result = 0
    for k,v in request.query_params.items():
        if k in "form":
            continue
        add = 0
        if "전혀그렇지 않다" in v:
            add = 0
        elif "약간 혹은 가끔" in v:
            add = 1
        elif "상당히 혹은 자주" in v:
            add = 2
        elif "매우 자주" in v:
            add = 3
        print(k, v, add)
        result += add
    val = ""
    if result >= 19:
        val = "ADHD 입니다."
    else:
        val = "ADHD가 아닙니다"
    ret = '총점 {}임으로 {}'.format(result, val)
    
    return ret

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)