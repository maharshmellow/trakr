### The PRIVATE Repo for Trakr - Will be made PUBLIC later so keep that in mind when making commits

**Bug** 
When the website is pinging the websites, any edits made on the website won't persist. This is because when pinging, I get all the data from the database, process it, update it, and push the changes back (instead of doing one push per update which would completely use up my free quota). A possible fix is to just put those newly added values in a queue temporarily and then after the pinging is completed, put those values in the database so they can be pinged the next time. Since this app won't be used by anyone, I am not fixing this as there are better things to learn with my time :)  

Collaboration Guide: 
https://github.com/codepath/android_guides/wiki/Collaborating-on-Projects-with-Git
