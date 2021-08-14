from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import db
import user
import auth_user

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/get/user/{name}")
app.mount("/scripts/reference", StaticFiles(directory="scripts"), name="scripts")
app.mount("/scripts/register", StaticFiles(directory="scripts"), name="scripts")

@app.get("/")
def get_index():
    return FileResponse('index.html')

@app.get("/reference")
def get_reference():
    return FileResponse('reference.html')

@app.get("/register")
def get_register():
    return FileResponse('register.html')

@app.get("/scripts/reference")
def get_reference_js():
    return FileResponse('scripts/reference.js')

@app.get("/scripts/register")
def get_register_js():
    return FileResponse('scripts/register.js')

@app.post("/post/user")
async def post_user(user: user.User):
    json_data = jsonable_encoder(db.post_user(user))
    return JSONResponse(content = json_data)

@app.post("/get/user/info")
async def post_user_authinfo(auth_user: auth_user.User):
    json_data = jsonable_encoder(db.get_user_info(auth_user))
    if json_data == False:
        raise HTTPException(status_code = 401, detail = "Authorization Failed")
    return JSONResponse(content = json_data)


#Authentication
@app.get("/auth/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}



