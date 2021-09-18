from utils import FirebaseApi, camera
from dotenv import dotenv_values

config = dotenv_values(".env")
api = FirebaseApi(config['creds_file'],
                  config['db_url'])

while True:
    itemId = camera("QR")
    if not str(itemId).isnumeric():
        print("something went wrong. invalid cup scanned")
        continue
    api.returnItem(itemId)
