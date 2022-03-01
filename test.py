from utils import FirebaseApi, camera
from dotenv import dotenv_values

config = dotenv_values(".env")
api = FirebaseApi(config['creds_file'],
                  config['db_url'])
oldUserId = None
api.checkOut(65421, 65431)

