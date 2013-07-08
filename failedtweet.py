import twitter, os

api = twitter.Api(consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
      consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
      access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
      access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

def failed_message(inspection):
    return ("%s failed a food inspection on %s. Visit http://www.eatsafe.co for more information. #FoodInspections" % (inspection.facilities.facility_name, str(inspection.inspection_date).replace('00:00:00', '')))

def tweet_if(inspection):
    return inspection.results == 'Fail'

def tweet_maybe(data_object, api_instance, conditional_f, message_f):
    """
    Tweets to a twitter account if the conditional function returns True. The tweet will have the message function return value as content.
    """ 
    if conditional_f(data_object) == True:
        message = message_f(data_object)
        print message
        api_instance.PostUpdate(message)

def tweet_failed(inspection):
    try:
        tweet_maybe(inspection, api, tweet_if, failed_message)
    except: pass
