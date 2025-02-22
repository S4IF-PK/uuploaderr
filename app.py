import streamlit as st
from sqlalchemy import String, create_engine, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from PIL import Image as PILImage

engine = create_engine("sqlite:///images.db")
Base = declarative_base()
class Image(Base):
    __tablename__ = "images"
    id = Column(Integer,primary_key=True)
    filename = Column(String(255),unique=True)
    url = Column(String(500),unique=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

UPLOAD_FOLDER = "upload_images"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
st.markdown("## Upload your Pic Here")
upload_file = st.file_uploader("Upload Pic Here",type=["png","jpeg","jpg","gif"])
if upload_file is not None:
    import uuid
    file_id = str(uuid.uuid4())
    file_id = str(file_id[::-1])
    file_extension = os.path.splitext(upload_file.name)[1]
    filename = f"{file_id}{file_extension}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    # Image ko save karna
    image = PILImage.open(upload_file)
    image.save(file_path)
    
    # Localhost URL banana
    file_url = f"http://localhost:8501/{file_path}"
    
    # Database mein record insert karna
    new_image = Image(filename=filename, url=file_url)
    session.add(new_image)
    session.commit()
    
    st.success("Picture Uploaded! !")
    st.write(f"Image URL: {file_url}")
    st.image(file_path)

st.markdown("## Made By Munna RDX")
