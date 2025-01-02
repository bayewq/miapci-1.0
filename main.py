import pytesseract
from PIL import Image,ImageEnhance, ImageFilter
import mss
import mss.tools
from ahk import AHK
from time import sleep 
from PIL import Image
import requests

##########################################
#               EDIT THESE               #

max_shares = 50
buy_at     = 199999
sell_at    = 800902020

#change this to the tesseract.exe Location
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

#                                        # 
##########################################

ahk = AHK()
item_coordinates = { # Made for 1980 x 1080 Monitor
    "empty"            : {"x": 1000, "y": 40},

    "enter"            : {"x": 620, "y": 340},
    "portfolio"        : {"x": 730, "y": 550},
    "buy_menu"         : {"x": 1200, "y": 550},
    "back"             : {"x": 500, "y": 180},

    "box1_buy_amount"  : {"x": 1140, "y": 485},
    "box1_buy"         : {"x": 1140, "y": 500},
    "box1_sell_amount" : {"x": 1250, "y": 485},
    "box1_sell"        : {"x": 1250, "y": 500},

    "box2_buy_amount"  : {"x": 1140, "y": 540},
    "box2_buy"         : {"x": 1140, "y": 560},
    "box2_sell_amount" : {"x": 1250, "y": 540},
    "box2_sell"        : {"x": 1250, "y": 560}, 

    "box3_buy_amount"  : {"x": 1140, "y": 595},
    "box3_buy"         : {"x": 1140, "y": 620},
    "box3_sell_amount" : {"x": 1250, "y": 595},
    "box3_sell"        : {"x": 1250, "y": 620},     
}

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

def get_stock_data(vol,price,ticker):
    price_data = [1,1,ticker]
    vol_data = translate(vol)
    raw_price = translate(price)[1:]
    price_data[0]=int(vol_data)
    price_data[1]=int(raw_price)
    return (price_data)

def enter_stocks_menu():
    print("Entering Stocks Menu")
    ahk.mouse_move(item_coordinates["enter"]["x"], item_coordinates["enter"]["y"])
    sleep(3)
    ahk.click()
    sleep(3)
    return 0

def enter_market():
    print("Entering Stock Market")
    ahk.mouse_move(item_coordinates["buy_menu"]["x"], item_coordinates["buy_menu"]["y"])
    sleep(3)
    ahk.click()
    sleep(3)
    ahk.mouse_move(item_coordinates["empty"]["x"], item_coordinates["empty"]["y"])
    sleep(1)
    return 0

def remount():
    print("Remounting")
    ahk.key_press('space')
    sleep(3)
    ahk.key_press('e')
    sleep(3)
    return 0 

def startup():
    print_logo()
    
    input('Press Enter To Continue...')
    print('TAB BACK INTO ROBLOX')
    sleep(3)
    
    remount()
    enter_stocks_menu()
    enter_market()

def buy(stock,shares):
    print ("Buying"+stock[2])
    
    if (stock[2] == 'meinc'):
        amt_x=item_coordinates["box1_buy_amount"]["x"]
        amt_y=item_coordinates["box1_buy_amount"]["y"]

        buy_x = item_coordinates["box1_buy"]["x"]
        buy_y = item_coordinates["box1_buy"]["y"]
    elif (stock[2] == 'sesh'):
        amt_x=item_coordinates["box2_buy_amount"]["x"]
        amt_y=item_coordinates["box2_buy_amount"]["y"]
    elif (stock[2] == 'tsv'):
        amt_x=item_coordinates["box3_buy_amount"]["x"]
        amt_y=item_coordinates["box3_buy_amount"]["y"]
    
    ahk.mouse_move(amt_x,amt_y)
    sleep(0.1)
    ahk.click()
    sleep(0.1)
    ahk.type(f"{shares}")
    sleep(0.1)
    ahk.mouse_move(buy_x,buy_y)
    sleep(0.1)
    ahk.click()
    sleep(1)
    remount()
    enter_stocks_menu()
    enter_market()
    return shares

def sell(stock):
    return

startup()

while (True):
    capture_prices()
    try:
            meinc_data = (get_stock_data('meinc_vol.png','meinc_price.png','meinc'))
            sesh_data = (get_stock_data('sesh_vol.png','sesh_price.png','sesh'))
            tsv_data = (get_stock_data('tsv_vol.png','tsv_price.png','tsv'))

            stock_data = [meinc_data,sesh_data,tsv_data]

            print('')
            print (stock_data)

            for stock in stock_data:
                if stock[1] < buy_at and stock[0] > 0 and max_shares > 0:
                    if stock[0] > max_shares:
                        shares = max_shares
                    else:
                        shares = stock[0]
                    max_shares = max_shares - buy(stock,shares)
                    print("shares now available ",max_shares)
                    break
            sleep(5)

    except:
        print('image capture error')
        remount()
        enter_stocks_menu()
        enter_market()
        sleep(3)    