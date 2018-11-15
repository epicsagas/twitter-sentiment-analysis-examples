# Python Twitter Korean Sentiment Analysis Example

These examples require Python 3.6 To install prerequisites.

```pip install -r requirements.txt```

## Twitter authenticate

You will need to authenticate with Twitter to use these scripts. To do so, sign up for developer credentials:

https://apps.twitter.com/

You can create access credentials directly through Twitter's web interface, authorized under the username you used to create the app.

Then add your consumer and access tokens to .env file.

## Tweepy environment

If you have a problem to run the Tweepy, please check your python version is lower than 3.6 and change your venv.
Or if you want to run on python version 3.7, change all variables "async" to "async_" on the file "venv/lib/python3.7/site-packages/tweepy/streaming.py".

## Sentiment Lexicon

Please download [KOSAC sentiment lexicon data](http://word.snu.ac.kr/kosac/lexicon.php) to "kosac-lexicon" directory. You would send the usage agreement about this lexicon data to SNU.
 
## Sentiment Analysis Method

This work is based on Okt(Open Korean Text by twitter)'s parser and KOSAC's sentiment lexicon polarity data and the sentiment score is calculated as below. 

> (P - N) / (P + N)
> * P: Sum of positive scores of input sentence, N: Sum of negative scores of input sentence

This is just an example. So if you want more accurate works, need to develop more detailed algorithm for testing and calculating korean text.
