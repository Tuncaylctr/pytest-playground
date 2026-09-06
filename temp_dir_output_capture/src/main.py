from fastapi import FastAPI, UploadFile, File
#import logging

app = FastAPI()

#logger = logging.getLogger(__name__)


@app.get("/user/{user_id}/profile")
def user_profile(user_id: int):
    return {"user_id": user_id, "profile": "UserProfileData"}


@app.get("/user/{user_id}/files")
def user_files(user_id: int):
    return {"user_id": user_id, "files": ["file1.txt", "file2.txt"]}


@app.post("/user/{user_id}/file")
async def upload_file(user_id: int, file: UploadFile = File(...)):
    contents = await file.read()
    print(f"Received file: {file.filename} from user {user_id}")
    #logger.info(f"Received file: {file.filename} from user {user_id}")
    return {
        "user_id": user_id,
        "filename": file.filename,
        "content": contents.decode()
    }


@app.get("/analytics/sales")
def analytics_sales():
    return {"sales": 1000}


@app.get("/analytics/stock")
def analytics_stock():
    return {"stock": 42}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
