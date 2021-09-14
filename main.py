import firebase_admin
from firebase_admin import db
import datetime
from dotenv import dotenv_values

class FirebaseApi:
    def __init__(self, credFilePath, databaseUrl, locationId):
        cred_obj = firebase_admin.credentials.Certificate(credFilePath)
        firebase_admin.initialize_app(cred_obj, {
	        'databaseURL': databaseUrl
    	})
        self.locationId = locationId
        self.ref = db.reference('/database/checkedOut')


    def checkOut(self, userId, cupId):
        contents = self.ref.get()
        for item in contents:
            item = contents[item]
            if not item['returned'] and item['cupId'] == cupId:
                print("item already exists")
                return
        self.ref.push().set({
            "abandoned": False,
            "returned": False,
            "timeCheckedOut": int(datetime.datetime.timestamp(datetime.datetime.now())),
            "locationId": self.locationId,
            "cupId": cupId,
            "userId": userId
        })

    def returnItem(self, cupId, abandoned = False):
        for key, item in self.ref.get().items():
            if item['cupId'] == cupId and not item['returned']:
                self.ref.child(key).update({'returned': True, 'abandoned': abandoned})
                return
        print("no item wth id")

config = dotenv_values(".env")
api = FirebaseApi(config['creds_file'], config['db_url'], config['location_id'])
