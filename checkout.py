from utils import FirebaseApi, camera
from dotenv import dotenv_values

config = dotenv_values(".env")
api = FirebaseApi(config['creds_file'],
                  config['db_url'])
oldUserId = None

while True:
    if oldUserId:
        userId = oldUserId
        oldUserId = None
    else:
        userId = camera("BARCODE")
        if not str(userId).isnumeric():
            print("something went wrong. wrong user id scanned")
            continue

    itemId = camera("QR")
    if not str(itemId).isnumeric():
        print("something went wrong. invalid cup scanned")
        oldUserId = userId
        continue

    print(userId, itemId)
    api.checkOut(userId, itemId)
