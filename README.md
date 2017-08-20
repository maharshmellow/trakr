# Trakr
Automatically checks for updates on websites! <br><br>
<a href="https://trakr.maharsh.net"><img src="https://cdn.rawgit.com/maharshmellow/550f99fcf7934352e83bb29d85176a04/raw/97e9b2d71bb78961605685ab372c134150c6bd40/demo.svg" width="150px;"/></a>

### Features / Tech
- Firebase login
- unlimited website tracks
- data stored on Amazon DynamoDB
- email notifications using Sendgrid
- websites pinged in parallel to decrease time
- only checks for data changes - hides CSS or JS changes
- has the foundation to add features such a SMS or varying notification times

### Screenshots

##### Login Page

![main](https://user-images.githubusercontent.com/4590693/29491171-261b0540-8510-11e7-954b-6d8d687e2e9e.png)

##### Home Page
![home](https://user-images.githubusercontent.com/4590693/29491172-261b6aee-8510-11e7-9aed-34bbb1360535.png)

##### Add Website Dialog
![add_website](https://user-images.githubusercontent.com/4590693/29491170-261952d6-8510-11e7-815d-b37d5969d5e3.png)

##### Edit Website Dialog
![edit_website](https://user-images.githubusercontent.com/4590693/29491173-261bb292-8510-11e7-90b9-416262f7d82f.png)

##### Status Page
![status](https://user-images.githubusercontent.com/4590693/29491174-261d98aa-8510-11e7-9ca8-997be5942d4e.png)


**Known Bug** <br>
When the website is pinging the websites, any edits made on the website won't persist. This is because when pinging, I get all the data from the database, process it, update it, and push the changes back all at once. **This is easy to fix by just updating user by user but that would completely use up my free quota.** Since this is just a side project, I don't necessarily want to pay for this, so for the time being, this issue will not be fixed. So a ping for all the websites occurs every 10 minutes and during that pinging time, no changes will be saved.
