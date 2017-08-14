import json

f = open("output.json")

data = json.load(f)
changed = {}    # {"id":{"modified_time":"new_time"}}
print(data, "\n")
for user in data:
    user_id = user[0]
    # if user_id not in changed: continue -- nothing has changed for this user
    if "websites" not in user[1]["attributes"] or user[1]["attributes"]["websites"]["S"] == "{}":
        continue

    user_websites = json.loads(user[1]["attributes"]["websites"]["S"])

    # print(user_websites)
    print(user)
    for website in user_websites:
        # add to the tasks here
        current_website = user_websites[website]
        print(current_website)
        # TODO do all modification here
        current_website["hash"] = current_website.pop("source_code")        # replacing the old source_code with hash because we are no longer storing the source code
        current_website["modified_time"] = "11:12:11"

        print(current_website)

    user[1]["attributes"]["websites"]["S"] = user_websites
    print(user)
    print()

print(data) # NOTE this data is now updated with the times - just need to dump it back now
