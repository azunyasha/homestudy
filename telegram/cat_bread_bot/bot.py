import telebot
from PIL import Image
import os
bot = telebot.TeleBot("6091449502:AAGLBBff_mq-CrA96O5AUBuaHaFedXOrbWI")


# Handle the '/start' command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Дай картинку')


@bot.message_handler(content_types=['photo'])
def image_handler(message):
    file_id = message.photo[-1].file_id
    file = bot.get_file(file_id)
    downloaded_file = bot.download_file(file.file_path)
    input_file_name = "./input/" +str(message.message_id)
    with open(input_file_name+".jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    while True:
        try:
            ouput_file_name = "./output/" +str(message.message_id) + ".txt"
            with open(ouput_file_name, 'r') as output_file:
                output_str = output_file.read()
                bot.send_message(message.chat.id, output_str)
                output_file.close()
            try:
                os.remove(ouput_file_name)
            except Exception as e:
                pass
            break
        except:
            pass




# Run the bot
print("bot started. ctrl-C to quit")
bot.polling()
