from fastapi import FastAPI, Request
from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from urllib import parse
import uvicorn
import random



app = FastAPI(
    title="sc",
)
app.mount("/static", StaticFiles(directory="static"), name="static")
print("ssibala")
# 0부터 1 사이의 임의의 부동소수점 숫자를 반환합니다.
random.random()
templates = Jinja2Templates(directory="templates")
@app.get("/loading", response_class=HTMLResponse) 
async def loading(request:Request):
    replaced = str(request.url).replace('loading', 'api')
    rand = random.randint(1, 3)
    img = "/static/img/"
    if rand == 1:
        img += "mia_loading1.jpg"
    elif rand == 2:
        img += "mia_loading2.jpg"
    else:
        img += "mia_loading3.jpg"
    context = {"request": request, "result_url": replaced, "loading_img":img}
    return templates.TemplateResponse("loading.html",context)

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

    context = {"request": request, "total": result}
    print(context)
    if result >= 19:
        return templates.TemplateResponse("abnormal.html", context)
    else:
        return templates.TemplateResponse("normal.html",context)

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)