import json
import time
import pytz
from trakr.api import aws_models
from datetime import datetime
import validators
from concurrent.futures import ProcessPoolExecutor
import concurrent.futures
import hashlib
import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get("SENDGRID"))
from_email = Email("trakr@maharsh.net")


def getHash(url, userID, old_hash, email):
    try:
        html = requests.get(url, verify=False).text
    except:
        # NOTE - in the future there can be an implementation where
        # we send notifications when there is an error reaching the page
        # add that notification sending feature right here
        return {"old_hash": old_hash, "new_hash": old_hash, "user_id":userID, "url":url}

    soup = BeautifulSoup(html, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()
    new_hash = hashlib.md5(text.encode("utf-8")).hexdigest()

    return {"old_hash": old_hash, "new_hash": new_hash, "user_id":userID, "url":url, "email":email}

def main():
    print("Ping Started at:", time.time())
    timezone = pytz.timezone("Canada/Mountain")
    users = {}
    data = json.loads(aws_models.User.dumps())
    updates = {}            # all the values to update -> {"user_id":{"url":{"modified_time":"new_time"...}...}...}

    with ProcessPoolExecutor(max_workers=10) as executor:
        tasks = []
        for user in data:
            user_id = user[0]

            if "websites" not in user[1]["attributes"] or user[1]["attributes"]["websites"]["S"] == "{}":
                continue
            user_websites = json.loads(user[1]["attributes"]["websites"]["S"])
            email = user[1]["attributes"]["email"]["S"]

            for website in user_websites:
                tasks.append(executor.submit(getHash, website, user_id, user_websites[website]["hash"], email))

        # get all the hashed website and figure out what needs to be changed in the database
        for future in concurrent.futures.as_completed(tasks):
            try:
                result = future.result()
            except:
                print("ERROR")
                continue

            old_hash = result["old_hash"]
            new_hash = result["new_hash"]
            user_id = result["user_id"]
            url = result["url"]
            email = result["email"]

            website_changes = {}       # changes to make for this particular website for this particular user
            # update the website checked time for this website
            current_time = datetime.fromtimestamp(int(time.time()), timezone).strftime("%B %d, %H:%M MST")
            website_changes["checked_time"] = current_time

            if old_hash != new_hash:
                website_changes["modified_time"] = current_time
                website_changes["hash"] = new_hash
                # send notification if change detected
                if old_hash != "" and old_hash != new_hash:
                    to_email = Email(email)
                    subject = "Trakr - Website Change Detected"
                    content = Content("text/plain", url+" was updated on " + datetime.fromtimestamp(int(time.time()), timezone).strftime("%B %d, %H:%M MST"))
                    mail = Mail(from_email, subject, to_email, content)
                    response = sg.client.mail.send.post(request_body=mail.get())

            # add to the dictionary of updates to make to the database
            if user_id in updates:
                updates[user_id][url] = website_changes
            else:
                updates[user_id] = {url:website_changes}        # creating a new dict since it didn't exist yet

            print(old_hash, new_hash, url)

    # change everything at once to not waste dynamodb write capacity by updating each user individually
    for user in data:
        user_id = user[0]

        # no data for this user has been changed, skip them
        if user_id not in updates: continue;
        # skip the users with no websites
        if "websites" not in user[1]["attributes"] or user[1]["attributes"]["websites"]["S"] == "{}": continue

        user_websites = json.loads(user[1]["attributes"]["websites"]["S"])
        for website in user_websites:
            # add to the tasks here
            current_website = user_websites[website]
            # make all the modification to this website here

            for update_item in updates[user_id][website]:
                update_value = updates[user_id][website][update_item]
                current_website[update_item] = update_value

        user[1]["attributes"]["websites"]["S"] = json.dumps(user_websites)

    # print(data)
    # upload the new data to dynamodb
    aws_models.User.loads(json.dumps(data))
    print("Ping Ended at:", time.time())
main()
