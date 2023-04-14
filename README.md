# Ski PNW
#### Video Demo:  https://youtu.be/mwnfb9QsWzU
#### Description:

I got my CSS from an extensive template I found online (cited in file) and supplemented it with fifteen methods of my own.
I used js for my navbar and weather widget. The former ensures that the website is easily navigable.
I used python in app.py to sanitize user input, select information from SQL queries, set up sessiosn to check if a user is logged in,
manage API data, and render/redirect templates.
I used a SQL database to keep track of (hashed) login information, chats, trip reports, and user-submitted media.
Each page changes slightly based on whether a user is logged in or not.

This website was created by a young skier raised by skiers.
Have questions? drop them in the chatroom and somebody is bound to answer.
We hope you can use our website to find new ski spots, connect with other skiers,
nab some sweet great at low prices, and watch your awesome fellow skiers on our media page.
I designed my own logo for the website. I wanted to create an inviting platform for all members of the ski community.
The demographic of skiers is becoming more diverse and we want to form a community where everybody can unite.
Ski PNW is a website that provides all of your skiing information and needs for the season at no cost.
Connect with other users through the chatroom or pick your next PNW resort destination (or undercover backountry adventure)
by browsing the trip reports. Looking for gear in good condition at a low price? Hoping to sell last year's skis? Head over to the marketplace!
Also, submit your coolest tricks on the media page for a chance to be featured in our season highlights newsletter.
We have news about road conditions, the snow forecast, and avalanche danger. Look below for the headlines in PNW skiing today.
Skiers of all ability and ages are welcome in our community. We also allow boarders, on a case-by-case basis :)
See you on the slopes, keep your fingers crossed for a powder day! And as always, we do not have information on all dangers.
So, KNOW BEFORE YOU GO.

about.html:
This page has information about the website, a contact form, and links to similar websites.

base.html:
Template for the rest of my html pages. This template controls the navbar, footer, and css links.

chatroom.html:
Only users who are logged in can view/submit chats. A user posts a chat and they are redirected back to the chatroom page.

index.html:
Index.html is the homepage. It has a blurb about Ski PNW, a weather widget displaying current weather, and pertinent headlines about skiing in the PNW.

login.html:
Page for users to login. There is also a log-out button in the nav bar.

media.html:
Page for users to submit and view media.

signup.html:
Page for users to sign-up.

market.html:
Page for users to buy/sell gear if they are logged in.

tripreport.html:
Page for users to submit/view user trip reports if they are logged in. If a user is not logged in, they can still view data from the WSDOT website
accessed via API and read the twitter feeds from PNW resorts.
