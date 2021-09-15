from utils import FirebaseApi, camera
from dotenv import dotenv_values

config = dotenv_values(".env")
api = FirebaseApi(config['creds_file'], config['db_url'], config['location_id'])


while True:
  ItemID = cameraQR()
  api.returnItem(ItemID)
  
