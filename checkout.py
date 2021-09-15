from utils import FirebaseApi, camera
from dotenv import dotenv_values

config = dotenv_values(".env")
api = FirebaseApi(config['creds_file'], config['db_url'], config['location_id'])
oldUserId = None

while True:
  if oldUserId:
    userId = oldUserId
  else:
    userId = camera()
    if not str(userId).isnumeric():
      print("something went wrong. wrong user id scanned")
      continue

  cupId = camera()
  if not str(cupId).isnumeric():
    print("something went wrong. invalid cup scanned")
    oldUserId = userId
    continue


  print(userId, cupId)
  api.checkOut(userId, cupId)