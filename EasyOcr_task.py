import easyocr as ocr  #OCR
import streamlit as st  #Web App
from PIL import Image #Image Processing
import numpy as np #Image Processing 
import mysql.connector
import pandas as pd
#import matplotlib as plt
# Database Connection

EasyOcrTask=mysql.connector.connect(host='localhost',
                        database='EasyOcrTask',
                        user='root',
                        password='2668')
mycursor = EasyOcrTask.cursor()




#title
st.title("Easy OCR - Extract Text from Images")

#subtitle
st.markdown("## Optical Character Recognition - Using `easyocr`, `streamlit`")

st.markdown("")

#image uploader
image = st.file_uploader(label = "Upload your image here",type=['png','jpg','jpeg'])


@st.cache_data
def load_model(): 
    reader = ocr.reader(['en'],model_storage_directory='.')
    return reader 

reader = load_model() #load model

if image is not None:

    input_image = Image.open(image) #read image
    st.image(input_image) #display image

    with st.spinner("🤖 AI is at Work! "):
        

        result = reader.readtext(np.array(input_image))

        result_text = [] #empty list for results


        for text in result:
            result_text.append(text[1])

        st.write(result_text)
    #st.success("Here you go!")
    st.snow()
else:
    st.write("Upload an Image")


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
