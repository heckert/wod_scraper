# WoD Scraper
My gym (https://crossfitarch.com/) releases a workout schedule for the upcoming week on Sundays at irregular times. Which typically leaves me anxiously checking their website in five-minute-intervals, impatiently waiting for the new plan to appear. In order to release me from this burden and practice webscraping a little along the way, I automated this process with Python and Cron.

This script scrapes their website, checks the week number of the header and sends out an e-mail with the new workouts if they are available already.

## Website view
This is how the workout schedule looks on my gyms website (I did of course not create the website, this project revolves around parsing its content): <br>
<img src="screenshot_website.png" width="550">

## E-Mail view
This is what the text of the generated e-mail notification looks like: <br>
<img src="screenshot_mail.png " width="550">