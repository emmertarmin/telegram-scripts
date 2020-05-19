# Python scripts I use to get notifications in Telegram

## 1yearago.py
I'm tracking daily diary entries with the daylio app on Android which has an export function. I find it's fun to see every day what I've been up to a year ago. Often it gives me a reason to share my nostalgia with others, or to reflect on the progress I've been making during this time.

## blinkist.py
Blinkist releases one book for free every day, and I thought it would be nice to get notified what that book is. During the first few weeks these daily free offers were classic titles from the past. After a while though I've noticed they've turned into very recent titles. I wonder who decides what the daily free book title is, and whether it's the same for everybody, or customized for returning users.

## f1.py
There's three basic functions:
* The `main` one tells me some details about the upcoming race, like date and city.
* The one called `f1last` prints out results of the last race.
* And `f1standing` is there to print the current driver standings in the championship.

## rss.py
Podcasts, blogs and even reddit forums have RSS feeds. Since Spotify doesn't notify you about new episodes, I made my own script, that does it for me. Sadly, RSS feeds aren't standardized enough, so some of them have to be parsed differently than the others, which is annoying.

## sun.py
Just two lines: When the sun goes up, and when the sun goes down that day.

## xkcd.py
If there's a new XKCD, then that's going to be sent. If it was sent earlier already, then it sends a random one. There's some lazy implementation to semi-prevent repetition of random comics.