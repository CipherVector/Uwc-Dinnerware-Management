from utils import *
from dotenv import dotenv_values

config = dotenv_values(".env")
api = FirebaseApi(config['creds_file'],
                  config['db_url'])
license = ""
with open("license.txt", "r") as f:
    license = f.read()

reader = dbr.BarcodeReader()
reader.init_license(license)
error = reader.init_runtime_settings_with_file('normal.json')
print(error)
print(reader.get_runtime_settings().__dict__)

while True:
    itemId = detect('QR','Color', image_copy, dbr.EnumImagePixelFormat.IPF_RGB_888)
   
    if not str(itemId).isnumeric():
        print("something went wrong. invalid cup scanned")
        continue
    api.returnItem(itemId)
