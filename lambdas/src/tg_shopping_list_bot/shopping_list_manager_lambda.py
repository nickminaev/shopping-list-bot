import boto3
import json
import os
import logging
from argparse import ArgumentParser, Namespace
from shlex import split
import requests

logger = logging.getLogger(__name__)
logger.setLevel("INFO") # the default level is WARNING
logger.info('Initializing lambda')
BODY_KEY = 'body'
UPDATE_ID_KEY = 'update_id'
CHAT_ID_KEY = 'chat_id'
MESSAGE_KEY = 'message'
CHAT_KEY = 'chat'
DYNAMODB_TABLE_KEY = 'DYNAMODB_TABLE'
TELEGRAM_BASE_URL = 'TELEGRAM_BASE_URL'
TELEGRAM_BOT_TOKEN = 'TELEGRAM_BOT_TOKEN'
ID_KEY = 'id'
TEXT_KEY = 'text'

table_name = os.environ.get(DYNAMODB_TABLE_KEY)
dynamodb_client = boto3.client('dynamodb')
telegram_url = os.environ.get(TELEGRAM_BASE_URL)
telegram_bot_token = os.environ.get(TELEGRAM_BOT_TOKEN)

telegram_session = requests.Session()

# We'll always return OK to the Telegram bot, so the messages are not pending in the queue
response = {
            'statusCode': 200,
            'body': 'OK'
           }

# test the changes 109999

parser = ArgumentParser()
parser.add_argument("command")
parser.add_argument("--item")
parser.add_argument("--unit")
parser.add_argument("--amount")
 
def add_item(item: Namespace, chat_id: int):
    pass

def remove_item(item: Namespace, chat_id: int):
    pass

def update_item(item: Namespace, chat_id: int):
    pass

def reset_shopping_list(item: Namespace, chat_id: int): # no need to pass an item as an argument
     pass

command_handler = {
     'add': add_item,
     'update': update_item,
     'remove': remove_item,
     'clear': reset_shopping_list
}


def verify_telegram_message_structure(tg_update:dict):
    if tg_update.get(UPDATE_ID_KEY) is None:
        return False
    telegram_message = tg_update.get(MESSAGE_KEY)
    if telegram_message is None:
        return False
    chat_properties = telegram_message.get(CHAT_KEY)
    if chat_properties is None:
         return False
    chat_id = chat_properties.get(ID_KEY)
    if chat_id is None:
         return False
    return True

def validate_telegram_text_message(telegram_message:dict):
     message_text = telegram_message.get(TEXT_KEY)
     if message_text is None:
        return False, """
                      Sorry, I support only commands. These are the commands that I support:
                      /add - add a new item to the shopping list.
                      /update - update an item in the shopping list.
                      /clear - clen up the shopping list.
                      /remove - remove an item from the shopiing list.
                      """
     return True, None

def send_response_to_user(chat_id, response_contents):
     response_chat_template = {
               'chat_id': chat_id,
               'text': response_contents
          }
     with telegram_session as session:
          session.post(f'{telegram_url}{telegram_bot_token}/sendMessage', json=response_chat_template)
     

def handler(event, context):
    logger.info('Executing handler')
    logger.info(f'Got the following event: {event}')
    telegram_update =  json.loads(event.get(BODY_KEY))
    if not verify_telegram_message_structure(telegram_update):
         logger.warning("Could not verify the Telegram bot update structure. Missing essential params.")
    telegram_message = telegram_update.get(MESSAGE_KEY)
    chat_properties = telegram_message.get(CHAT_KEY)
    chat_id = chat_properties.get(ID_KEY)
    is_text_message, validation_message = validate_telegram_text_message(telegram_message)
    if not is_text_message:
         send_response_to_user(chat_id, validation_message)
         return response
    message_text = telegram_message.get(TEXT_KEY)
    if len(message_text<=4):
         logger.warning('The message text is empty or does not seem to contain any command')
         return response
    if message_text[0]!='/':
         logger.warning(f'The following message is not a command: {message_text}')
         return response
    try:
        message_args = parser.parse_args(split(message_text[1:]))
        method_to_execute = command_handler.get(message_args.command)
        if method_to_execute is None:
             logger.warning(f'Command {message_args.command} is not supported. One of the available commands should be used')
             return response
        result = method_to_execute(message_args, chat_id)
            # response = dynamodb_client.put_item(
            #     Item = {
            #         'message_id': {'N': str(update_id)},
            #         'message_contents': {'S': json.dumps(message_contents)}
            #     },
            #     TableName = table_name
            # )
    except SystemExit as exc:
            logger.warning(f'Was not able to parse the shopping list arguments from the following message: {message_text}')
            return response
    return response