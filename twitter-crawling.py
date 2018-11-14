import datetime
import time
import re
import config
import csv

from selenium import webdriver

from konlpy.tag import Okt
okt = Okt()

SCRAP_URL = "https://twitter.com/search?l=ko&q={} since:{} until:{}&src=typd"
DRIVER_DIR = config.DRIVER_DIR

#dictionaries
polarityDic = []
with open('kosac-lexicon/polarity.csv', mode='r') as infile:
    polarity = csv.reader(infile)

    for row in polarity:
        header = row[0].split(";")[0]
        maxValue = row[7]
        maxProp = row[8]

        polarityDic.append({
            "header": header,
            "maxValue": maxValue,
            "maxProp": maxProp
        })

def getRecommendNumber(number):
    if (number.find('K') > -1):
        return str(int(float(number.replace('K', '')) * 1000))

    if len(number) > 0:
        return number

    return "0"

def getSentimentScore(text):
    score = 0.0
    neg = 0.0
    pos = 0.0

    textPos = okt.pos(text)

    for row in polarityDic:
        for text in textPos:
            if text[0] in row['header']:
                if(row['maxValue']=="POS"):
                    pos += float(row['maxProp'])
                elif (row['maxValue'] == "NEG"):
                    neg += float(row['maxProp'])

    if(pos-neg != 0.0):
        score = (pos-neg)/(pos+neg)

    return score

def crawling(pages,keyword,since,until):
    driver = webdriver.Chrome(DRIVER_DIR)
    driver.implicitly_wait(10)
    driver.get(SCRAP_URL.format(str(keyword),str(since),str(until)))

    pages = int(pages)

    outputName = "data/%s_%s_%s.tsv" % (keyword,since,until)
    output = open(outputName, "a", encoding='utf-8')

    try:
        page = 0

        while page < pages:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight * 0.3)')
            time.sleep(1)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight * 0.7)')
            time.sleep(1)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight * 0.9)')
            time.sleep(1)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(1.5)

            page += 1

        print("search uri: %s" % SCRAP_URL.format(str(keyword),str(since),str(until)))
        contents = driver.find_elements_by_css_selector('div.content')

        print("searched tweets: ", len(contents))

        for content in contents:
            #Text
            tweet_text = str(content.find_element_by_css_selector('p.tweet-text').text).replace('\n',' ').replace('\r',' ')
            #remove url, hash tags, etc
            tweet_text = re.sub(
                r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''',
                "", tweet_text)
            tweet_text = re.sub('(^pic.twitter.com|#|@)(\w+)', '', tweet_text)

            #Retweets
            retweet = getRecommendNumber(content.find_element_by_css_selector('button.js-actionRetweet').find_element_by_css_selector('span.ProfileTweet-actionCountForPresentation').text)

            #Favorites
            favorite = getRecommendNumber(content.find_element_by_css_selector('button.js-actionFavorite').find_element_by_css_selector('span.ProfileTweet-actionCountForPresentation').text)

            #date
            timestamp = int(content.find_element_by_css_selector('span.js-short-timestamp').get_attribute("data-time"))
            dateString = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            datetimeString = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')

            # jsonFileName = "sourceDir/%s/%s.json" % (keyword,dateString)
            #
            # jsonFile = open(jsonFileName, "a", encoding='utf-8')
            # jsonFile.write('{"text": "%s", "datetime": "%s ", "retweets": %s, "favorites": %s},' % (tweet_text.replace('"','\''),datetimeString,retweet,favorite))
            # jsonFile.close()

            sentimentScore = getSentimentScore(tweet_text)

            print(sentimentScore)

            output.write("%s\t%s\t%s\t%s\t%s" % (tweet_text,datetimeString,retweet,favorite,sentimentScore))
            output.write("\n")

    except Exception as e:
        print(e)

    finally:
        output.close()
        driver.quit()

if __name__ == '__main__':
    pages = input('pages (scroll pages number ? ')
    keyword = input('keyword ? ')
    since = input('since (yyyy-mm-dd) ? ')
    until = input('until (yyyy-mm-dd) ? ')

    crawling(pages,keyword,since,until)