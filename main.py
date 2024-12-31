import pytesseract
from PIL import Image,ImageEnhance, ImageFilter
import mss
import mss.tools
from ahk import AHK
from time import sleep 
from PIL import Image
import requests

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def print_logo():
    print('')
    print(f"              $$\                               $$\ ")
    print(f"              \__|                              \__|")
    print(f"$$$$$$\$$$$\  $$\  $$$$$$\   $$$$$$\   $$$$$$$\ $$\ ")
    print(f"$$  _$$  _$$\ $$ | \____$$\ $$  __$$\ $$  _____|$$ |")
    print(f"$$ / $$ / $$ |$$ | $$$$$$$ |$$ /  $$ |$$ /      $$ |")
    print(f"$$ | $$ | $$ |$$ |$$  __$$ |$$ |  $$ |$$ |      $$ |")
    print(f"$$ | $$ | $$ |$$ |\$$$$$$$ |$$$$$$$  |\$$$$$$$\ $$ |")
    print(f"\__| \__| \__|\__| \_______|$$  ____/  \_______|\__|")
    print(f"version 1.0                 $$ |                    ")           
    print(f"                            $$ |                    ")         
    print(f"                            \__|                    ")             
    return 0 


def translate(image):
    img = Image.open(image)
    img = img.convert("L")
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    
    
    output = pytesseract.image_to_string(img, config = "--psm 8 -c tessedit_char_whitelist='0123456789$'")
    price_data = output[0:-2]
    return price_data

def capture_prices():
    with mss.mss() as sct:
        monitor = {"top": 475, "left": 815, "width": 60, "height": 35}
        output = "meinc_vol.png"
        sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    with mss.mss() as sct:
        monitor = {"top": 475, "left": 960, "width": 100, "height": 35}
        output = "meinc_price.png"
        sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    
    with mss.mss() as sct:
        monitor = {"top": 531, "left": 815, "width": 60, "height": 35}
        output = "sesh_vol.png"
        sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    with mss.mss() as sct:
        monitor = {"top": 531, "left": 960, "width": 100, "height": 35}
        output = "sesh_price.png"
        sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    
    with mss.mss() as sct:
        monitor = {"top": 588, "left": 815, "width": 60, "height": 35}
        output = "tsv_vol.png"
        sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    with mss.mss() as sct:
        monitor = {"top": 588, "left": 960, "width": 100, "height": 35}
        output = "tsv_price.png"
        sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

def get_stock_data(vol,price):
    price_data = [1,1]
    vol_data = translate(vol)
    raw_price = translate(price)[1:]
    price_data[0]=int(vol_data)
    price_data[1]=int(raw_price)
    return (price_data)

def main():
    print_logo()
    while (True):
        capture_prices()
        try:
            meinc_data = (get_stock_data('meinc_vol.png','meinc_price.png'))
            sesh_data = (get_stock_data('sesh_vol.png','sesh_price.png'))
            tsv_data = (get_stock_data('tsv_vol.png','tsv_price.png'))
            
            print(meinc_data)
            print(sesh_data)
            print(tsv_data)
        except:
            print('error')
        sleep(1)
main()