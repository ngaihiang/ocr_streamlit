import pandas as pd
import streamlit as st
# from pytesserract_extractor import ocr_model
# from ocr_info_extractor import ocr_model


# Streamlit App
from PIL import Image
import pandas as pd
import pytesseract


# Classes
class OCR:
    def __init__(self):
        pass
    # def __init__(self, detection_model_name='DB_r18', recognizer_model_name='RobustScanner', device='cpu', merge=True,
    #              details=True):
        # self.ocr_model = MMOCR(config_dir="~/mmocr/configs/",
        #                        det=detection_model_name,
        #                        recog=recognizer_model_name,
        #                        # kie='SDMGR',
        #                        device=device)
        # self.merge = merge
        # self.details = details
    
   
    def _read_jpg_oriented(self, filename):
        im=Image.open(filename)
        try:
            image_exif = im._getexif()
            image_orientation = image_exif[274]
            if image_orientation in (2,'2'):
                return im.transpose(Image.FLIP_LEFT_RIGHT)
            elif image_orientation in (3,'3'):
                return im.transpose(Image.ROTATE_180)
            elif image_orientation in (4,'4'):
                return im.transpose(Image.FLIP_TOP_BOTTOM)
            elif image_orientation in (5,'5'):
                return im.transpose(Image.ROTATE_90).transpose(Image.FLIP_TOP_BOTTOM)
            elif image_orientation in (6,'6'):
                return im.transpose(Image.ROTATE_270)
            elif image_orientation in (7,'7'):
                return im.transpose(Image.ROTATE_270).transpose(Image.FLIP_TOP_BOTTOM)
            elif image_orientation in (8,'8'):
                return im.transpose(Image.ROTATE_90)
            else:
                return im
        except (KeyError, AttributeError, TypeError, IndexError):
            return im
    
    def _get_text_df(self, input_img):
        custom_config = r'--psm 11' #try 8 
        # text = pytesseract.image_to_string(img, lang='eng', config=custom_config)
        img_word_df = pytesseract.image_to_data(input_img, lang='eng', config=custom_config, output_type='data.frame')
        img_word_df = img_word_df[img_word_df.conf > -1] # -1 returns Nan
        img_word_df = img_word_df[img_word_df.conf >= 80] # -1 returns Nan
    
        return img_word_df

    def get_text(self, image_path):
        img = self._read_jpg_oriented(image_path)

        # Pytesseract get text
        img_word_df = self._get_text_df(img)
        doc_str = " ".join(img_word_df['text'])
       
        return [img, doc_str]


ocr_model = OCR()


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
