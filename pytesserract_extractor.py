from PIL import Image
import numpy as np
import pandas as pd
from glob import glob
import pytesseract
import cv2


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
        # img_word_df = img_word_df[img_word_df.conf >= 50] # -1 returns Nan
    
        return img_word_df

    def get_text(self, image_path):
        img = self._read_jpg_oriented(image_path)

        # Pytesseract get text
        img_word_df = self._get_text_df(img)
        doc_str = " ".join(img_word_df['text'])

        # Convert image from PIL to CV2 format   
        cv2_img = np.array(img)
        h, w, _ = cv2_img.shape

        n_boxes = len(img_word_df['level'])
        for i in range(n_boxes):
            x, y, w, h = img_word_df['left'].values[i], img_word_df['top'].values[i], img_word_df['width'].values[i], img_word_df['height'].values[i]
            cv2.rectangle(cv2_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
       
        return [img, cv2_img, doc_str]


ocr_model = OCR()
