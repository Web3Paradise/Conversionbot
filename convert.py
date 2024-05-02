import logging
from telegram.ext import Updater, CommandHandler
import requests

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the token for your bot
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Define the API key for the file conversion service
CONVERSION_API_KEY = 'YOUR_CONVERSION_API_KEY'

# Define the base URL for the file conversion service
CONVERSION_BASE_URL = 'https://api.cloudconvert.com/v2/convert'

# Define the supported file formats
SUPPORTED_FORMATS = ['pdf', 'docx', 'jpg', 'png']

# Define the start function
def start(update, context):
    update.message.reply_text('Welcome to the File Conversion Bot! Send me a file and I will convert it to the desired format.')

# Define the convert function
def convert(update, context):
    # Check if a file is sent
    if not update.message.document:
        update.message.reply_text('Please send a file to convert.')
        return

    # Get the file ID
    file_id = update.message.document.file_id
    
    # Get the file name
    file_name = update.message.document.file_name

    # Get the desired file format
    desired_format = context.args[0].lower()

    # Check if the desired format is supported
    if desired_format not in SUPPORTED_FORMATS:
        update.message.reply_text('Sorry, this file format is not supported.')
        return

    # Download the file
    file = context.bot.get_file(file_id)
    file.download(file_name)

    # Send a message indicating that the conversion is in progress
    update.message.reply_text('Converting file...')

    # Convert the file
    conversion_url = f'{CONVERSION_BASE_URL}?apikey={CONVERSION_API_KEY}&inputformat=auto&outputformat={desired_format}'
    files = {'file': open(file_name, 'rb')}
    response = requests.post(conversion_url, files=files)

    # Check if the conversion was successful
    if response.status_code == 200:
        # Send the converted file
        converted_file = response.content
        update.message.reply_document(converted_file, filename=f'{file_name.split(".")[0]}.{desired_format}')
    else:
        update.message.reply_text('Sorry, an error occurred during the conversion.')

# Define the main function
def main():
    # Create the Updater and pass it your bot's token
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("convert", convert))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
