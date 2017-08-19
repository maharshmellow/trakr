# Trakr
Automatically checks for updates on websites!

### Features / Tech
- Firebase login
- unlimited website tracks
- data stored on Amazon DynamoDB
- email notifications using Sendgrid
- websites pinged in parallel to decrease time
- only checks for data changes - hides CSS or JS changes
- has the foundation to add features such a SMS or varying notification times

**Known Bug**
When the website is pinging the websites, any edits made on the website won't persist. This is because when pinging, I get all the data from the database, process it, update it, and push the changes back all at once. **This is easy to fix by just updating user by user but that would completely use up my free quota.** Since this is just a side project, I don't necessarily want to pay for this, so for the time being, this issue will not be fixed. So a ping for all the websites occurs every 10 minutes and during that pinging time, no changes will be saved.
