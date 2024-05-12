


# import imp
# import shutil
from uuid import UUID, uuid4
from fastapi import FastAPI, File, HTTPException, Form, Depends,UploadFile, status
from pydantic import BaseModel, Field
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

# from backendwork.app.mediaHandler import mediaSaver
from . import crud, models, schemas
from .database import SessionLocal, engine
# from backendwork.app import EmailSender

# from fastapi.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)

#dependency
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
        
        
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET","POST"],
    # allow_headers=["*"],
)

# app.mount('/uploadedFiles', StaticFiles(directory='uploadedFiles'),'uploadedFiles')

# class College(BaseModel):
    
#     name: str= Form(...)
#     address: str= Form(...)
#     email: str= Form(...)
#     phone: str= Form(...)
#     signatory: str = Form(...) 
    # logo: UploadFile = File(...)

# class TestCollege(BaseModel):
#     name: str
    # logo: FilePath
class Message(BaseModel):
    message: str
    
@app.get("/all", response_model=list[schemas.UserBase])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/")
async def root(message: Message):
        return JSONResponse(content="You've been registered successfully.", status_code=status.HTTP_201_CREATED)
    
    # return {"message": f"Hello World! \n Your message: {message.message}"}
# @app.post("/register")
# async def register(college: College):
#     print(college)
    
#     return {"message":"Success"}

from .validators import validate_email
# from .EmailSender import send_registration_email
from .emailVerification import send_otp
# from .mediaHandler import mediaSaver

# @app.post("/register", response_model=list[schemas.CollegeBase])
from .EmailSender import send_registration_email
@app.post("/register")
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # print(user.email.lower(), user.password, user.user_name.lower())
    # print("Hello, World!")
    
    if not validate_email(user.email):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid Email. Email must be like example@mail.com")

    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered!")
    else:
        user = crud.save_new_user(db=db, user=user)
        
        message = f"""
        <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
</head>
<body style="font-family: Arial, sans-serif;
      background-color: #f0f0f0;
      text-align: center;
      padding: 20px;">
  <div style="max-width: 600px;
      margin: 0 auto;
      background-color: #fff;
      padding: 30px;
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
    <h1 style="  color: #333;">Welcome to Time Hackers!</h1>
    <p style = "color: #666;
      font-size: 18px;">Hello {user.user_name},</p>
    <p style = "color: #666;
      font-size: 18px;">Thank you for joining Time Hackers! With our app, you can easily manage your time and stay organized.</p>
    <p style = "color: #666;
      font-size: 18px;">Get started now and make the most out of your time!</p>
  </div>
</body>
</html>

        """
        # send_registration_email(user.email, subject="Welcome to Time Hackers!", message=message)
        # otp = send_otp(user.user_name, user.email)
        # crud.save_otp(db=db, email=user.email, otp=otp)
        # return JSONResponse(content="An Email Verification OTP is send to your email address.", status_code=status.HTTP_201_CREATED)
        return JSONResponse(content="You've been registered successfully.", status_code=status.HTTP_201_CREATED)
    # return JSONResponse(content="You've been registered successfully.", status_code=status.HTTP_200_OK)
    
from datetime import timedelta
from .passwordHashers import verify_password, create_access_token
import os
@app.post("/login")
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        valid_password = verify_password(user.password, db_user.password)
        if valid_password:
            # return JSONResponse(content={"token":create_access_token({"id":str(db_user.user_id)}, expires_delta=timedelta(minutes=int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])))}, status_code=status.HTTP_202_ACCEPTED)
            message = f"""<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f0f0f0; text-align: center; padding: 20px;">
  <div style="max-width: 600px; margin: 0 auto; background-color: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
    <h1 style="color: #333;">Welcome Back!</h1>
    <p style="color: #666; font-size: 18px;">Hello {db_user.user_name},</p>
    <p style="color: #666; font-size: 18px;">We're excited to see you back in the Time Hackers! Your journey continues with us.</p>
    <p style="color: #666; font-size: 18px;">Stay organized, stay productive!</p>
  </div>
</body>
</html>
"""
            # send_registration_email(recipient_email=user.email, subject="Welcome Back!", message=message)
            return JSONResponse(content={"token":create_access_token({"id":str(db_user.user_id),"username":str(db_user.user_name),"email":str(db_user.email)})}, status_code=status.HTTP_202_ACCEPTED)
        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Incorrect Password")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with given email not exists." )
    

from datetime import datetime as dt

@app.post("/verify-otp")
async def verify_otp(verify: schemas.VerifyOTP, db: Session = Depends(get_db)):
    # print(verify.email)
    if len(verify.otp) != 6:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid OTP size.")
    else:
        db_otp = crud.get_otp(db=db,email=verify.email)
        current_time = dt.now()
        otp_time = db_otp.creation_time
        # print("Current time: ",current_time)
        # print("Creation time: ", otp_time)
        
        if (current_time-otp_time).seconds/60 > 5:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="OTP time out.")
        if db_otp.otp==verify.otp:
            crud.updateEmailVerified(db=db, email=verify.email)
            return JSONResponse(content="Email is verified!", status_code=status.HTTP_202_ACCEPTED)
            
        
    
@app.post("/resend-otp")
async def resend_otp(resend: schemas.resendOTP, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db=db, email=resend.email)
    if not user.email_verified:
        otp = send_otp(user.user_name, resend.email)
        crud.save_otp(db=db, email=user.email, otp=otp)
        return JSONResponse(content="An email with OTP is send to your email address.", status_code=status.HTTP_202_ACCEPTED)
    elif user.email_verified:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Email already verified")
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="No such email exists.")

from .scheduleGenerator import schedule_tasks

@app.post("/generate-time-table")
async def generate_time_table(userdata: schemas.TimeTableCreate, db: Session = Depends(get_db)):
    # print(userdata.task_list, userdata.allocated_time)
    schedule = schedule_tasks(userdata.task_list, userdata.allocated_time)
    # print(schedule)
    if (len(schedule)==0):
        # print("There is some issue with time slots you have provided.")
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail={"warning":"There is some issue with time slots you have provided."})
        # return JSONResponse(content={"warning":"There is some issue with time slots you have provided."}, status_code=status.HTTP_201_CREATED)
    else:
        # print(schedule)
        return JSONResponse(content={"schedule":schedule}, status_code=status.HTTP_201_CREATED)

    # db_college = crud.get_college_by_email(db,email)
    # if db_college:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered!")
    # else:
    #     if mediaSaver(logo):
    #         media_dict = {
    #             "filename":logo.filename,
    #             "size":logo.size
    #         }
    #         media = crud.save_media(db=db, media=media_dict)
            
    #         college_dict = {
    #             "college_name":name,
    #             "address":address,
    #             "official_email":email,
    #             "official_phone":phone,
    #             "signatory":signatory,
    #             "logo_id":media.media_id                
    #         }
            
    #         college = crud.create_college(db=db, college=college_dict)
    #         send_registration_email(username=name,user_id=college.college_id,recipient_email=email)
    #         return JSONResponse(content={"message":f"An email with College ID is send to your mail address: {email}."},status_code=status.HTTP_201_CREATED)             
                
    #     else:
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="There is problem in saving the given file.")
    

# @app.post("/login")
# async def login(clgid: str = Form(...), db: Session = Depends(get_db)):
#     college = crud.get_college_by_id(db=db,clgid=clgid)
#     if college:
#         return JSONResponse(content={"id":clgid}, status_code=status.HTTP_202_ACCEPTED)
#     else:
#         return JSONResponse(content="ID not exists", status_code=status.HTTP_401_UNAUTHORIZED)
    # return {"message":"Hello, World!"}
    # pass

# from PIL import Image
# import io
# import os
# from datetime import datetime
# import pytz

# @app.post("/upload_logo")
# async def upload_logo(logo: UploadFile = File(...),clgid: str=Form(...) ):
#     print(clgid)
#     print("Current Directory: ",os.getcwd())
#     os.chdir("uploadedFiles")
#     # path=f"{logo.filename}"
#     logo_name_splitted=str(logo.filename).split(".")
#     now_time = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d_%H-%M-%S-%f')
#     path= "".join(logo_name_splitted[:-1:]) + now_time + "." + logo_name_splitted[-1]
    
#     with open(path,"wb") as file:
#         shutil.copyfileobj(logo.file, file)
#     os.chdir("..")
    
#     print(f"""
# 'file':{logo.filename}
# 'content':{logo.content_type}
# 'path':{path}
#           """)
#     # image = Image.open(io.BytesIO(logo)) #png not suppported for conversion directly
#     # image.show()

#     # with open(f"uploadedFiles/file.jpg","wb"):
        
    
#     return {"message":"Hello, World!"}
    