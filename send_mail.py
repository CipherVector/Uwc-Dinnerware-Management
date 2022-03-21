from utils import FirebaseApi, make_ordinal
import json
from dotenv import dotenv_values
import datetime
import smtplib
from email.mime.text import MIMEText
import schedule
from time import sleep

config = dotenv_values(".env")
api = FirebaseApi(config['creds_file'],
                  config['db_url'])


def emailBadPeople():
    f = open(config['ids_file'])
    j = json.load(f)
    users = api.abandonedItems()
    for key, value in users.items():
        abandoned = api.getAbandoned(key)
        ninetyDays = int(datetime.datetime.timestamp(
            datetime.datetime.now())) + 1
        countAbandoned = 0
        #TODO fix the 90 day count, Should we do this? / what period should this be over this
        for item in abandoned:
            if item['timeCheckedOut'] < ninetyDays:
                countAbandoned += 1
        msg = MIMEText(
            f"""\
Dear student,

You are recieving this email because you failed to return {"a cup" if len(value) == 1 else "multiple cups"} that you recieved more than 24 hours ago.
This is the {make_ordinal(countAbandoned)} time that you have failed to return a cup.
If you fail to return a cups 3 times in 90 days, you will be reprimanded by the school.

Sincerely,
The Campus Cup Team\
        """)
        msg['subject'] = "Failed to return cup"
        msg['From'] = config['email_address']
        print(j[str(key)])
        msg['To'] = j[str(key)]
        print(msg)
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(config['email_address'], config['email_password'])
            server.sendmail(config['email_address'],
                            j[str(key)], msg.as_string())
            server.close()
            print(f'Email sent to {j[str(key)]}')
            for item in value:
                api.ref.child(item).update({"email_sent": True})
        except Exception as e:
            print(e)


schedule.every().day.at("15:00").do(emailBadPeople)
while True:
    emailBadPeople()
    schedule.run_pending()
    sleep(1)
