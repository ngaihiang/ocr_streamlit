import pandas as pd
import streamlit as st
from pytesserract_extractor import ocr_model
# from ocr_info_extractor import ocr_model


# Streamlit App
"""
# OCR Info Extractor
"""

document_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
if document_file is not None:
    with open(document_file.name, "wb") as dfh:
        dfh.write(document_file.getbuffer())
        st.success("File Upload Successfull")
        print(document_file)

    with st.spinner("Performing Magic and Extracting Text from the Uploaded Image !! Please Wait..."):
        img, doc_str = ocr_model.get_text(document_file.name)
        st.image(img)
        # detected_text = [item['text'] for item in result[1]]
        # text, label, label_score = [], [], []
        # tl_x, tl_y, tr_x, tr_y, br_x, br_y, bl_x, bl_y = [], [], [], [], [], [], [], []
        # for item in result[1]:
        #     text.append(item['text'])
        #     tl_x.append(item['box'][0])
        #     tl_y.append(item['box'][1])
        #     tr_x.append(item['box'][0])
        #     tr_y.append(item['box'][1])
        #     br_x.append(item['box'][0])
        #     br_y.append(item['box'][1])
        #     bl_x.append(item['box'][0])
        #     bl_y.append(item['box'][1])
        #     # label.append(item['label'])
        #     # label_score.append(item['label_score'])
        # df = pd.DataFrame({'Text': text, 'TLx': tl_x, 'TLy': tl_y, 'TRx': tr_x, 'TRy': tr_y, 'BRx': br_x, 'BRy': br_y, 'BLx': bl_x, 'BLy': bl_y}) #, 'Label': label, 'Label Score': label_score})
        # df['TLx_round'] = 5 * round(df['TLx']/5)
        # df['TLy_round'] = 5 * round(df['TLy']/5)
        # df = df.sort_values(['TLy_round', 'TLx_round'])
    st.balloons()
    st.write(doc_str)
    # st.write(df['Text'].tolist())
    # if st.checkbox("Show Labels"):
    #     st.write(df[['Text', 'Label', 'Label Score']])


    # streamlit run ocr_streamlit_app.py
