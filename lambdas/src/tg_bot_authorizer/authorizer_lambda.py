import os
import logging
logger = logging.getLogger(__name__)
logger.setLevel("INFO")

CHAT_ID = 'chatId'
TG_USER_ID = 'telegramUserId'
TG_SECRET_TOKEN_HEADER = 'x-telegram-bot-api-secret-token'
HEADERS = 'headers'
TG_SECRET_ENV = 'BOT_AUTHORIZATION_KEY'


response = {
    'isAuthorized': False,
    'context': {
        TG_USER_ID: 0,
        CHAT_ID: 0
    }
}

bot_auth_key = os.environ.get(TG_SECRET_ENV)

# test changes 4

def handler(event, context):
    if bot_auth_key is None:
        return response
    logger.info('Got the Bot auth key sent by Telegram from the environment')
    request_headers = event.get(HEADERS)
    if request_headers is None:
        return response
    request_secret_key = request_headers.get(TG_SECRET_TOKEN_HEADER)
    if request_secret_key is None:
        return response
    if request_secret_key == bot_auth_key:
        # TODO: populate the authorizer's context
        response['isAuthorized'] = True
        logger.info(f'Authorized access to the API GW: {response}')
    return response
    
    