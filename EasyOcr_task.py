%%writefile ocr_task.py

import easyocr as ocr
import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
from easyocr import Reader
import base64
import mysql.connector
import pandas as pd 

EasyOcrTask=mysql.connector.connect(host='localhost',
                        database='EasyOcrTask',
                        user='root',
                        password='2668')
mycursor = EasyOcrTask.cursor()


img = Image.open('/content/maxresdefault (2).jpg')
col1, col2, col3, col4 = st.columns([0.2, 5, 0.2,0.1])
col2.image(img, width=500)

#title
st.title("Easy OCR - Extract Text from Images")

#subtitle
st.markdown("## Optical Character Recognition - Using `easyocr`, `streamlit`")


#image uploader
image = st.file_uploader(label = "Upload your image here",type=['png','jpg','jpeg'])

@st.cache_data
def Ocr_model():
  reader = ocr.Reader(['en','ta'])
  return reader

reader = Ocr_model()

if image is not None:

  Ocr_image = Image.open(image)
  st.image(Ocr_image)

  with st.spinner("Preparing your Text! "):
      

      result = reader.readtext(np.array(Ocr_image))

      result_text = []


      for text in result:
          result_text.append(text[1])

      st.write(result_text)

  st.snow()

else:
    st.write("Upload a image")

with st.sidebar:
    st.title("Upload to Database")
    
    if st.button("Submit to Database"):
        st.write(result_text)

    else:
        print("Invalid Attempt")

if result_text:
    sql= "CREATE TABLE Easy_Ocr_Task (MyIndex INT NOT NULL AUTO_INCREMENT,Name VARCHAR(50),Business_type VARCHAR(25),phone INT,phone1 INT, Website_url VARCHAR(30),Email VARCHAR(30),Address VARCHAR(50) ,Business_Name VARCHAR(50),PRIMARY KEY (MyIndex))"
mycursor.execute(sql)
print('Table created successfully.')
EasyOcrTask.commit()
df = result_text
for index, row in df.iterrows():
     quer="INSERT INTO EasyOcrTask.Easy_Ocr_Task(Name,Business_type,phone,phone1,Website_url,Email,Address,Business_Name) values(%s,%s,%s,%s,%s,%s,%s,%s)"
     mycursor.execute(quer,(row.Name,row.Business_type,row.phone,row.phone1,row.Website_url,row.Email,row.Address,row.Business_Name))
print('DataFrame Inserted successfully.')
EasyOcrTask.commit()
mycursor.close()









page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background-image: url();
background-size: cover;
}

[data-testid="stHeader"]{
background-color: rgba(0,0,0,0);
}

[data-testid="stToolbar"] {
right: 2rem;
}

[data-testid="stSidebar"] {
background-image: url("")
backgound-size: cover;
}

</style>
"""

st.markdown(page_bg_img,unsafe_allow_html=True)
