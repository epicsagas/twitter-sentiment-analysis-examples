from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer as Vader
import config

class listener(StreamListener):
    def on_data(self, data):
        all_data = json.loads(data)

        tweet_text = all_data["text"].replace('\n',' ').replace('\r',' ')
        outputFile = "data/streamout.tsv"

        vader = Vader()
        score = vader.polarity_scores(tweet_text)

        if score['pos'] > 0 and score['compound'] > 0:
            sentimentalStatus = 'Positive'
        elif score['neg'] > 0 and score['compound'] < 0:
            sentimentalStatus = 'Negative'
        else:
            sentimentalStatus = 'neutural'

        print(json.dumps(all_data))

        if all_data['retweeted'] == False:
            output = open(outputFile, "a", encoding='utf-8')
            output.write(all_data['timestamp_ms'] + "\t" + tweet_text + "\t" + str(score['pos']) + "\t" + str(score['neg']) + "\t" + str(score['compound']) + "\t" + sentimentalStatus)
            output.write("\n")
            output.close()

        time.sleep(1)

        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    auth = OAuthHandler(config.CKEY, config.CSECRET)
    auth.set_access_token(config.ATOKEN, config.ASECRET)
    twitterStream = Stream(auth, listener())

    # 검색어
    # twitterStream.filter(track=["Seoul"],languages=["ko"])
    # 맵좌표
    twitterStream.filter(locations=[125.76,33.16,129.63,38.52],languages=["ko"])

    # 홍대 예) 126.916268,37.546465,126.926227,37.555055
    # 대한민국 예) 125.76,33.16,129.63,38.52