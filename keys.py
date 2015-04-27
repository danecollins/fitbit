import os

# keys are set as environment variables.  On a Mac or Linux you would set these with
# export FITBIT_CONSUMER_KEY='5..............................f'
# export FITBIT_CONSUMER_SECRET='e..............................4'
# export DANE_USERID='2.....'
# export DANE_OAUTH_TOKEN='7...............................f'
# export DANE_OAUTH_SECRET='a...............................e'


def fitbit_key():

    # Returns the consumer key, consumer secret and a dict of user tokens

    # Client (Consumer) Key
    consumer_key = os.environ['FITBIT_CONSUMER_KEY']
    #
    # Client (Consumer) Secret
    consumer_secret = os.environ['FITBIT_CONSUMER_SECRET']
    #
    # Temporary Credentials (Request Token) URL
    # https://api.fitbit.com/oauth/request_token
    #
    # Token Credentials (Access Token) URL
    # https://api.fitbit.com/oauth/access_token
    #
    # Authorize URL
    # https://www.fitbit.com/oauth/authorize
    # You'll have to gather the user keys on your own,
    #     or try ./fitbit/gather_keys_cli.py <con_key> <con_sec> for development

    oakeys = {}
    oakeys['dane'] = {'encoded_user_id': os.environ['DANE_USERID'],
                      'oauth_token': os.environ['DANE_OAUTH_TOKEN'],
                      'oauth_token_secret': os.environ['DANE_OAUTH_SECRET']}
    oakeys['cindy'] = {'encoded_user_id': os.environ['CINDY_USERID'],
                       'oauth_token': os.environ['CINDY_OAUTH_TOKEN'],
                       'oauth_token_secret': os.environ['CINDY_OAUTH_SECRET']}

    return(consumer_key, consumer_secret, oakeys)


def twilio_key():
    ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
    AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
    return(ACCOUNT_SID, AUTH_TOKEN)
