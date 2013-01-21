# RefUnotify => http://hacks.rewiredstate.org/events/refunitedmod/refunotify

Refugees can receive a notification when we detect a new user that matches the criterias of the person they are looking for.


# How it works

For new users, they will have to create a new account.
Then, any user can connect this replica of the Refugee United website : http://m.dev.refunite2012.org/language.html
They precise certain criterias of the person they are missing (i.e. name, age, gender...)
Alternatively, they can send us those criterias by text and the Twilio API will parse those paramters over to the node.js app.

On the back-end, we use the API holding a staging version of the database.
We send a GET request to statistics_profileactions to pull the latest activity of users.
Then, we match the json response to the criterias the user gave us and if there is a match the user is notified by text (to do this we used the SMS API)
