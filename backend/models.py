from sqlalchemy import Column, Integer, String
from database import Base


# ==========================
# User Table
# ==========================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))


# ==========================
# Uploaded Images Table
# ==========================

class UploadedImage(Base):
    __tablename__ = "uploaded_images"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String(255))

    filepath = Column(String(500))