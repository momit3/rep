from pyrogram import Client, filters


api_id = 19605213
api_hash = "1705b2cc407b7612449ed8ef9978a127"
bot_token = "6162233123:AAFpljoqFThieAJV0a0q34eTVG_iGkF6FeI"
app = Client("numberadderBot2", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

chat_id = []
result = [None] * 100


@app.on_message()
def join_link(client, message):
    print(message.chat.id)

    if len(str(message.text).split("+")) == 2:
        number = str(message.text).split("+")
        if message.chat.id not in chat_id:
            chat_id.append(message.chat.id)
            id_index = chat_id.index(message.chat.id)
            result[id_index] = float(eval(number[1]))
            print(result[id_index])
            message.reply_text(result[id_index])
        else:
            id_index = chat_id.index(message.chat.id)
            result[id_index] += float(eval(number[1]))
            print(result[id_index])
            message.reply_text(result[id_index])
    if len(str(message.text).split("-")) ==2:
        number = str(message.text).split("-")
        if message.chat.id not in chat_id:
            chat_id.append(message.chat.id)
            id_index = chat_id.index(message.chat.id)
            result[id_index] = float(eval(number[1]))
            print(result[id_index])
            message.reply_text(result[id_index])
        else:
            id_index = chat_id.index(message.chat.id)
            result[id_index] -= float(eval(number[1]))
            print(result[id_index])
            message.reply_text(result[id_index])


# Start the bot
app.run()
