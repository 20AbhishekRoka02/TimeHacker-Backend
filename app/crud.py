# import imp
from sqlalchemy.orm import Session
from sqlalchemy import update
from . import models, schemas

def get_all_user(db: Session):
    return db.query(models.User).all()

def get_user_by_email(db:Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
    
from .passwordHashers import get_password_hash
def save_new_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(user_name=user.user_name, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    
    
def save_otp(db: Session, email: str, otp: str):
    try:
        # Deleting old otp
        otp_to_delete = db.query(models.verification_otps).filter(models.verification_otps.email==email).first()
        db.delete(otp_to_delete)
        db.commit()
    except Exception as e:
        print(e)
        pass
    
    # saving new otp
    db_otp = models.verification_otps(email=email, otp=otp)
    db.add(db_otp)
    db.commit()
    db.refresh(db_otp)
    return db_otp

def updateEmailVerified(db: Session, email: str):
    user = get_user_by_email(db=db, email=email)
    user.email_verified=True
    db.commit()
    pass
    
def get_otp(db: Session, email: str):
    return db.query(models.verification_otps).filter(models.verification_otps.email==email).first()
    
# def get_college_by_id(db: Session, clgid: str):
#     return db.query(models.College).filter(models.College.college_id == clgid).first()

# def save_media(db: Session, media: dict):
#     db_media = models.MediaFiles(filename=media["filename"], size=media["size"])
#     db.add(db_media)
#     db.commit()
#     db.refresh(db_media)
#     return db_media

# def create_college(db: Session, college: dict):
#     db_college = models.College(college_name=college["college_name"],address=college["address"], official_email=college["official_email"],official_phone=college["official_phone"],signatory=college["signatory"],logo_id=college["logo_id"])
#     db.add(db_college)
#     db.commit()
#     db.refresh(db_college)
#     return db_college