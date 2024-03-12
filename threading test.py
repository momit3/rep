from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatMember
import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import sqlite3
from PIL import Image
import threading
import datetime


api_id = 19605213
api_hash = "1705b2cc407b7612449ed8ef9978a127"
bot_token = "6702756056:AAFAIuNl0-zvHwMqpVeejub5iZyVDFaw4p8"
app = Client("AutoUC", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


activate_bool =False
add_code_bool =False
remove_code_bool =False
view_code_bool =False
statistics_bool =False
profile_bool =False
ID_bool = False
amount_bool = False

top_up_id = ""
amount_add = ""
amount_rem = ""
amount_top_up = ""
redeem_amount = ""
redeem_code = ""
x = ""
id_no = -1
id_list = ['midasbuy', 'midasbuy1', 'midasbuy2']
with open('approved_users.pkl', 'rb') as f:
    approved_users = pickle.load(f)
print(approved_users)
# approved_users = ['subnet_255', 'ragner82']
# with open('approved_users.pkl', 'wb') as f:
#     pickle.dump(approved_users, f)

def create_user_table(username):
    # Create a table for the user's lists
    conn = sqlite3.connect('ragner_codes.db')
    cursor = conn.cursor()
    cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {username} (
                list_id INTEGER PRIMARY KEY,
                UC10 TEXT DEFAULT NULL,
                UC60 TEXT DEFAULT NULL,
                UC325 TEXT DEFAULT NULL,
                UC660 TEXT DEFAULT NULL,
                UC1800 TEXT DEFAULT NULL,
                UC3850 TEXT DEFAULT NULL,
                UC8100 TEXT DEFAULT NULL,
                UC16200 TEXT DEFAULT NULL,
                UC24300 TEXT DEFAULT NULL
            )
        ''')
    conn.commit()


def insert_row_for_new_date(date, message):
    conn = sqlite3.connect('ragner_codes.db')
    cursor = conn.cursor()
    cursor.execute(f'''INSERT INTO {message.chat.username}_stats (date, UC10, UC60, UC325, UC660, UC1800, UC3850, UC8100, UC16200, UC24300)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (date, 0, 0, 0, 0, 0, 0, 0, 0, 0))
    conn.commit()


def create_stats_table(username):
    conn = sqlite3.connect('ragner_codes.db')
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {username}_stats (
                        date TEXT PRIMARY KEY,
                        UC10 INTEGER,
                        UC60 INTEGER,
                        UC325 INTEGER,
                        UC660 INTEGER,
                        UC1800 INTEGER,
                        UC3850 INTEGER,
                        UC8100 INTEGER,
                        UC16200 INTEGER,
                        UC24300 INTEGER
                    )''')
    conn.commit()

def get_values(username,column, limit):
    conn = sqlite3.connect('ragner_codes.db')
    cursor = conn.cursor()

    # Execute the SELECT query to retrieve the first 3 values from UC10
    cursor.execute(f'''
        SELECT {column} FROM {username} LIMIT {limit}
    ''')

    # Fetch all the rows and extract the values from UC10 column
    rows = cursor.fetchall()
    uc10_values = [row[0] for row in rows]

    conn.close()  # Close the connection
    return uc10_values


@app.on_message(filters.command("start") & filters.private & filters.user(users=approved_users))
def get_text(client, message):
    create_user_table(message.chat.username)
    create_stats_table(message.chat.username)
    print(message.text)


@app.on_message(filters.command("new_subscriber") & filters.private & filters.user(['subnet_255', 'ragner82']))
def get_text(client, message):
    user = str(message.text).split(" ")
    approved_users.append(message.text[1])
    with open('approved_users.pkl', 'wb') as f:
        pickle.dump(approved_users, f)
    message.reply(f"New subscriber approved. Username{message.text[1]}")
    app.send_message("subnet_255", f"New subscriber approved. Username{message.text[1]}")


@app.on_message(filters.command("activate") & filters.private & filters.user(users=approved_users))
def get_text(client, message):
    global activate_bool
    global add_code_bool
    global remove_code_bool
    global view_code_bool
    global statistics_bool
    global profile_bool
    global ID_bool
    global amount_bool
    activate_bool = False
    add_code_bool = False
    remove_code_bool = False
    view_code_bool = False
    statistics_bool = False
    profile_bool = False
    ID_bool = False
    amount_bool = False
    conn = sqlite3.connect('ragner_codes.db')
    cursor = conn.cursor()
    print(message.text)
    global x
    available_list = []
    for column in ['UC10', 'UC60', 'UC325', 'UC660', 'UC1800',
                   'UC3850', 'UC8100', 'UC16200', 'UC24300']:
        cursor.execute(f'''
                SELECT COUNT({column}) FROM {message.chat.username}
            ''')
        count = cursor.fetchone()[0]
        available_list.append(count)
    activate_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(f"10 UC - {available_list[0]}", callback_data="UC10"),
                InlineKeyboardButton(f"60 UC - {available_list[1]}", callback_data="UC60"),
                InlineKeyboardButton(f"325 UC - {available_list[2]}", callback_data="UC325"),
            ],
            [
                InlineKeyboardButton(f"660 UC - {available_list[3]}", callback_data="UC660"),
                InlineKeyboardButton(f"1800 UC - {available_list[4]}", callback_data="UC1800"),
                InlineKeyboardButton(f"3850 UC - {available_list[5]}", callback_data="UC3850"),
            ],
            [
                InlineKeyboardButton(f"8100 UC - {available_list[6]}", callback_data="UC8100"),
                InlineKeyboardButton(f"16200 UC - {available_list[7]}", callback_data="UC16200"),
                InlineKeyboardButton(f"24300 UC - {available_list[8]}", callback_data="UC24300"),
            ]
        ]

    )
    x = message.reply("Select amount of UC to purchase:", reply_markup=activate_markup)


@app.on_message(filters.command("add_code") & filters.private & filters.user(users=approved_users))
def get_text(client, message):
    global activate_bool
    global add_code_bool
    global remove_code_bool
    global view_code_bool
    global statistics_bool
    global profile_bool
    global ID_bool
    global amount_bool
    activate_bool = False
    add_code_bool = False
    remove_code_bool = False
    view_code_bool = False
    statistics_bool = False
    profile_bool = False
    ID_bool = False
    amount_bool = False
    conn = sqlite3.connect('ragner_codes.db')
    cursor = conn.cursor()
    global x
    print(message.text)
    available_list = []
    for column in ['UC10', 'UC60', 'UC325', 'UC660', 'UC1800',
                   'UC3850', 'UC8100', 'UC16200', 'UC24300']:
        cursor.execute(f'''
            SELECT COUNT({column}) FROM {message.chat.username}
        ''')
        count = cursor.fetchone()[0]
        available_list.append(count)
    add_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(f"10 UC - {available_list[0]}", callback_data="UC10_add"),
                InlineKeyboardButton(f"60 UC - {available_list[1]}", callback_data="UC60_add"),
                InlineKeyboardButton(f"325 UC - {available_list[2]}", callback_data="UC325_add"),
            ],
            [
                InlineKeyboardButton(f"660 UC - {available_list[3]}", callback_data="UC660_add"),
                InlineKeyboardButton(f"1800 UC - {available_list[4]}", callback_data="UC1800_add"),
                InlineKeyboardButton(f"3850 UC - {available_list[5]}", callback_data="UC3850_add"),
            ],
            [
                InlineKeyboardButton(f"8100 UC - {available_list[6]}", callback_data="UC8100_add"),
                InlineKeyboardButton(f"16200 UC - {available_list[7]}", callback_data="UC16200_add"),
                InlineKeyboardButton(f"24300 UC - {available_list[8]}", callback_data="UC24300_add"),
            ]
        ]

    )
    x = message.reply("Select amount of UC to be added:", reply_markup=add_markup)


@app.on_message(filters.command("remove_code") & filters.private & filters.user(users=approved_users))
def get_text(client, message):
    global activate_bool
    global add_code_bool
    global remove_code_bool
    global view_code_bool
    global statistics_bool
    global profile_bool
    global ID_bool
    global amount_bool
    activate_bool = False
    add_code_bool = False
    remove_code_bool = False
    view_code_bool = False
    statistics_bool = False
    profile_bool = False
    ID_bool = False
    amount_bool = False
    conn = sqlite3.connect('ragner_codes.db')
    cursor = conn.cursor()
    global x
    print(message.text)
    available_list = []
    for column in ['UC10', 'UC60', 'UC325', 'UC660', 'UC1800',
                   'UC3850', 'UC8100', 'UC16200', 'UC24300']:
        cursor.execute(f'''
            SELECT COUNT({column}) FROM {message.chat.username}
        ''')
        count = cursor.fetchone()[0]
        available_list.append(count)
    remove_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(f"10 UC - {available_list[0]}", callback_data="UC10_rem"),
                InlineKeyboardButton(f"60 UC - {available_list[1]}", callback_data="UC60_rem"),
                InlineKeyboardButton(f"325 UC - {available_list[2]}", callback_data="UC325_rem"),
            ],
            [
                InlineKeyboardButton(f"660 UC - {available_list[3]}", callback_data="UC660_rem"),
                InlineKeyboardButton(f"1800 UC - {available_list[4]}", callback_data="UC1800_rem"),
                InlineKeyboardButton(f"3850 UC - {available_list[5]}", callback_data="UC3850_rem"),
            ],
            [
                InlineKeyboardButton(f"8100 UC - {available_list[6]}", callback_data="UC8100_rem"),
                InlineKeyboardButton(f"16200 UC - {available_list[7]}", callback_data="UC16200_rem"),
                InlineKeyboardButton(f"24300 UC - {available_list[8]}", callback_data="UC24300_rem"),
            ]
        ]

    )
    x = message.reply("Select amount of UC to be removed:", reply_markup=remove_markup)

    print(message.text)


@app.on_message(filters.command("view_code") & filters.private & filters.user(users=approved_users))
def get_text(client, message):
    slt = str(message.text).split(" ")
    xz= get_values(username=message.chat.username, limit=slt[2], column=slt[1])
    print(xz)


@app.on_message(filters.command("statistics") & filters.private & filters.user(users=approved_users))
def get_text(client, message):
    conn = sqlite3.connect('ragner_codes.db')
    cursor = conn.cursor()
    isodate = str(datetime.date.today().isoformat())
    stats = []
    for column in ['UC10', 'UC60', 'UC325', 'UC660', 'UC1800',
                   'UC3850', 'UC8100', 'UC16200', 'UC24300']:
        cursor.execute(f'''SELECT {column} FROM {message.chat.username}_stats WHERE date = ?''', (isodate,))
        result = cursor.fetchone()[0]
        stats.append(result)
    message.reply(f"Statistics for today ({isodate})\n\n10 UC - **{stats[0]}x**\n60 UC - **{stats[1]}x**\n325 UC - **{stats[2]}x**\n660 UC - **{stats[3]}x**\n1800 UC - **{stats[4]}x**\n3850 UC - **{stats[5]}x**\n8100 UC - **{stats[6]}x**\n16200 UC - **{stats[7]}x**\n24300 UC - **{stats[8]}x**")
    print(message.text)


@app.on_message(filters.command("profile") & filters.private & filters.user(users=approved_users))
def get_text(client, message):

    print(message.text)


@app.on_callback_query()
def callback_query(client, query):
    global ID_bool
    global amount_add
    global amount_bool
    global remove_code_bool
    global amount_rem
    global redeem_code
    global redeem_amount
    global x

    # activate
    if query.data == "UC10":
        app.delete_messages(query.message.chat.id, x.id)
        redeem_amount = "10"
        x = query.message.reply(f"**{redeem_amount}UC** to be sent.\nEnter Player ID:")
        ID_bool = True

    if query.data == "UC60":
        app.delete_messages(query.message.chat.id, x.id)
        redeem_amount = "60"
        x = query.message.reply(f"**{redeem_amount}UC** to be sent.\nEnter Player ID:")
        ID_bool = True

    if query.data == "UC325":
        app.delete_messages(query.message.chat.id, x.id)
        redeem_amount = "325"
        x = query.message.reply(f"**{redeem_amount}UC** to be sent.\nEnter Player ID:")
        ID_bool = True

    if query.data == "UC660":
        app.delete_messages(query.message.chat.id, x.id)
        redeem_amount = "660"
        x = query.message.reply(f"**{redeem_amount}UC** to be sent.\nEnter Player ID:")
        ID_bool = True

    if query.data == "UC1800":
        app.delete_messages(query.message.chat.id, x.id)
        redeem_amount = "1800"
        x = query.message.reply(f"**{redeem_amount}UC** to be sent.\nEnter Player ID:")
        ID_bool = True

    if query.data == "UC3850":
        app.delete_messages(query.message.chat.id, x.id)
        redeem_amount = "3850"
        x = query.message.reply(f"**{redeem_amount}UC** to be sent.\nEnter Player ID:")
        ID_bool = True

    if query.data == "UC8100":
        app.delete_messages(query.message.chat.id, x.id)
        redeem_amount = "8100"
        x = query.message.reply(f"**{redeem_amount}UC** to be sent.\nEnter Player ID:")
        ID_bool = True

    if query.data == "UC16200":
        app.delete_messages(query.message.chat.id, x.id)
        redeem_amount = "16200"
        x = query.message.reply(f"**{redeem_amount}UC** to be sent.\nEnter Player ID:")
        ID_bool = True

    if query.data == "UC24300":
        app.delete_messages(query.message.chat.id, x.id)
        redeem_amount = "24300"
        x = query.message.reply(f"**{redeem_amount}UC** to be sent.\nEnter Player ID:")
        ID_bool = True

    # add
    if query.data == "UC10_add":
        app.delete_messages(query.message.chat.id, x.id)
        amount_add = "10"
        x = query.message.reply(f"Enter **{amount_add}UC** codes: \n\n<i>(Must be separated by new line)</i>")
        amount_bool = True

    if query.data == "UC60_add":
        app.delete_messages(query.message.chat.id, x.id)
        amount_add = "60"
        x = query.message.reply(f"Enter **{amount_add}UC** codes: \n\n<i>(Must be separated by new line)</i>")
        amount_bool = True

    if query.data == "UC325_add":
        app.delete_messages(query.message.chat.id, x.id)
        amount_add = "325"
        x = query.message.reply(f"Enter **{amount_add}UC** codes: \n\n<i>(Must be separated by new line)</i>")
        amount_bool = True

    if query.data == "UC660_add":
        app.delete_messages(query.message.chat.id, x.id)
        amount_add = "660"
        x = query.message.reply(f"Enter **{amount_add}UC** codes: \n\n<i>(Must be separated by new line)</i>")
        amount_bool = True

    if query.data == "UC1800_add":
        app.delete_messages(query.message.chat.id, x.id)
        amount_add = "1800"
        x = query.message.reply(f"Enter **{amount_add}UC** codes: \n\n<i>(Must be separated by new line)</i>")
        amount_bool = True

    if query.data == "UC3850_add":
        app.delete_messages(query.message.chat.id, x.id)
        amount_add = "3850"
        x = query.message.reply(f"Enter **{amount_add}UC** codes: \n\n<i>(Must be separated by new line)</i>")
        amount_bool = True

    if query.data == "UC8100_add":
        app.delete_messages(query.message.chat.id, x.id)
        amount_add = "8100"
        x = query.message.reply(f"Enter **{amount_add}UC** codes: \n\n<i>(Must be separated by new line)</i>")
        amount_bool = True

    if query.data == "UC16200_add":
        app.delete_messages(query.message.chat.id, x.id)
        amount_add = "16200"
        x = query.message.reply(f"Enter **{amount_add}UC** codes: \n\n<i>(Must be separated by new line)</i>")
        amount_bool = True

    if query.data == "UC24300_add":
        app.delete_messages(query.message.chat.id, x.id)
        amount_add = "24300"
        x = query.message.reply(f"Enter **{amount_add}UC** codes: \n\n<i>(Must be separated by new line)</i>")
        amount_bool = True

    #remove
    if query.data == "UC10_rem":
        app.delete_messages(query.message.chat.id, x.id)
        amount_rem = "10"
        x = query.message.reply(f"Enter number of codes to be removed from **{amount_rem}UC** list:")
        remove_code_bool = True

    if query.data == "UC60_rem":
        app.delete_messages(query.message.chat.id, x.id)
        amount_rem = "60"
        x = query.message.reply(f"Enter number of codes to be removed from **{amount_rem}UC** list:")
        remove_code_bool = True

    if query.data == "UC325_rem":
        app.delete_messages(query.message.chat.id, x.id)
        amount_rem = "325"
        x = query.message.reply(f"Enter number of codes to be removed from **{amount_rem}UC** list:")
        remove_code_bool = True

    if query.data == "UC660_rem":
        app.delete_messages(query.message.chat.id, x.id)
        amount_rem = "660"
        x = query.message.reply(f"Enter number of codes to be removed from **{amount_rem}UC** list:")
        remove_code_bool = True

    if query.data == "UC1800_rem":
        app.delete_messages(query.message.chat.id, x.id)
        amount_rem = "1800"
        x = query.message.reply(f"Enter number of codes to be removed from **{amount_rem}UC** list:")
        remove_code_bool = True

    if query.data == "UC3850_rem":
        app.delete_messages(query.message.chat.id, x.id)
        amount_rem = "3850"
        x = query.message.reply(f"Enter number of codes to be removed from **{amount_rem}UC** list:")
        remove_code_bool = True

    if query.data == "UC8100_rem":
        app.delete_messages(query.message.chat.id, x.id)
        amount_rem = "8100"
        x = query.message.reply(f"Enter number of codes to be removed from **{amount_rem}UC** list:")
        remove_code_bool = True

    if query.data == "UC16200_rem":
        app.delete_messages(query.message.chat.id, x.id)
        amount_rem = "16200"
        x = query.message.reply(f"Enter number of codes to be removed from **{amount_rem}UC** list:")
        remove_code_bool = True

    if query.data == "UC24300_rem":
        app.delete_messages(query.message.chat.id, x.id)
        amount_rem = "24300"
        x = query.message.reply(f"Enter number of codes to be removed from **{amount_rem}UC** list:")
        remove_code_bool = True


@app.on_message(filters.private & filters.user(users=approved_users))
def get_text(client, message):
    global amount_bool
    global ID_bool
    global top_up_id
    global remove_code_bool
    global redeem_amount
    global x
    global id_no

    if ID_bool:
        ID_bool = False
        id_no += 1
        print(id_no)
        activation_thread(midas_id=f"midasbuy{id_no}", amount_top_up=redeem_amount, message=message, app=app)
        if id_no >= 3:
            id_no = -1

    if remove_code_bool:
        remove_code_bool = False
        conn = sqlite3.connect('ragner_codes.db')
        cursor = conn.cursor()
        to_be_removed = int(message.text)
        cursor.execute(f'''SELECT COUNT(UC{amount_rem}) FROM {message.chat.username}''')
        count = cursor.fetchone()[0]
        if count >= to_be_removed:
            zz = count-to_be_removed
            list_txt = []
            for i in range(to_be_removed):
                cursor.execute(f'''SELECT UC{amount_rem} FROM {message.chat.username} WHERE list_id = {zz+i}''')
                code = cursor.fetchone()[0]
                list_txt.append(code)
                cursor.execute(f'''UPDATE {message.chat.username} SET UC{amount_rem} = NULL WHERE list_id = {zz+i}''')
            conn.commit()
            file_path = f"UC{amount_rem} [{to_be_removed}x].txt"
            with open(file_path, "w") as file:
                for item in list_txt:
                    file.write(item + "\n")
            app.send_document(message.chat.username, f"UC{amount_rem} [{to_be_removed}x].txt", caption= f"**• Pack: {amount_rem}UC\n• Quantity:{to_be_removed}x**")
        else:
            message.reply("You don't have enough codes.")


    if amount_bool:
        conn = sqlite3.connect('ragner_codes.db')
        cursor = conn.cursor()
        to_be_added_bs = str(message.text).split("\n")
        to_be_added = [item.strip() for item in to_be_added_bs if item.strip()]
        already_code = []
        cursor.execute(f'''
                    SELECT COUNT(UC{amount_add}) FROM {message.chat.username}
                ''')
        count = cursor.fetchone()[0]
        for i in range(count):
            cursor.execute(f'''SELECT UC{amount_add} FROM {message.chat.username} WHERE list_id = {i}''')
            code = cursor.fetchone()[0]
            already_code.append(code)
        total_code = to_be_added + already_code
        unique_list = []
        print(f"unique {unique_list}")
        duplicate_list = []
        for item in total_code:
            if item not in unique_list:
                unique_list.append(item)
            else:
                duplicate_list.append(item)
        finally_add = []
        for item in unique_list:
            if item not in already_code:
                finally_add.append(item)

        print(f"unique 2 {finally_add}")
        amount_bool = False
        cursor.execute(f'''SELECT COUNT(UC{amount_add}) FROM {message.chat.username}''')
        count = cursor.fetchone()[0]

        for i, value in enumerate(finally_add, start=count):
            try:
                cursor.execute(f'''
                                            INSERT INTO {message.chat.username} (list_id, UC{amount_add}) VALUES (?, ?)
                                        ''', (i, value))
            except:
                cursor.execute(f'''
                                        UPDATE {message.chat.username} SET UC{amount_add} = ? WHERE list_id = ?
                                    ''', (value, i))

        conn.commit()
        dupli_str = "\n".join(f"{item}" for item in duplicate_list)
        if len(duplicate_list) == 0:
            message.reply(f"{len(finally_add)} Codes added to {amount_add}UC list.")
        else:
            message.reply(f"{len(finally_add)} Codes added to {amount_add}UC list. \n\nDuplicate Count = **{len(duplicate_list)}**\nDuplicate codes:\n{dupli_str}")


def activate(midas_id, amount_top_up, message,app):
    top_up_id = str(message.text).split("\n")
    conn = sqlite3.connect('ragner_codes.db')
    cursor = conn.cursor()
    cursor.execute(f'''SELECT COUNT(UC{redeem_amount}) FROM {message.chat.username}''')
    last = cursor.fetchone()[0]
    print(last)

    if last >= len(top_up_id):
        for i, pubg_id in enumerate(top_up_id, start=1):
            cursor.execute(f'''SELECT UC{redeem_amount} FROM {message.chat.username} WHERE list_id = {last - i}''')
            redeem_code = cursor.fetchone()[0]
            cursor.execute(f'''UPDATE {message.chat.username} SET UC{redeem_amount} = NULL WHERE list_id = {last - i}''')
            conn.commit()
            print(f"{pubg_id} - {redeem_code}")
            topup = random.randint(100000000,999999999)
            y = message.reply(f"**• TopUP request processing...** </b>✅\n\n**• TOPUP ID:** {topup}\n**• Player ID:** {pubg_id}\n**• UC AMOUNT:** {amount_top_up} UC\n**• CODE USED:** {redeem_code}")
            options = webdriver.ChromeOptions()
            # options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080") #1024,768
            options.add_argument(f'--user-data-dir=ChromeProfiles\\{midas_id}')
            driver = webdriver.Chrome(options=options)
            used_code = False
            invalid_code = False
            try:
                driver.get("https://www.midasbuy.com/midasbuy/my/redeem/pubgm")
                time.sleep(2)
                # try:
                #     driver.find_element(By.XPATH,
                #                         '/html/body/div[3]/div/div[1]').click()   //*[@id="root"]/div/div[5]/div[2]/div[1]/div/div[4]/div/div
                # except:
                #     pass
                try:
                    driver.implicitly_wait(2)
                    driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[1]/span').click()
                    driver.implicitly_wait(2)
                    driver.find_element(By.XPATH,
                                        '//*[@id="root"]/div/div[5]/div[2]/div[1]/div/div[2]/div/div/div[1]/input').clear()
                    # input pubg id
                    driver.implicitly_wait(2)
                    driver.find_element(By.XPATH,
                                        '//*[@id="root"]/div/div[5]/div[2]/div[1]/div/div[2]/div/div/div[1]/input').send_keys(
                        f"{pubg_id}")
                    time.sleep(1)

                    # okay after inputting pubg id
                    driver.implicitly_wait(2)
                    driver.find_element(By.XPATH,
                                        '//*[@id="root"]/div/div[5]/div[2]/div[1]/div/div[3]/div/div/div/div').click()
                except:
                    ## New Account
                    driver.implicitly_wait(2)
                    driver.find_element(By.XPATH,
                                        '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[2]/div/div').click()
                    driver.implicitly_wait(2)
                    time.sleep(1)
                    driver.find_element(By.XPATH,
                                        '//*[@id="root"]/div/div[5]/div[2]/div[1]/div/div[3]/div/div/div[1]/input').send_keys(f"{pubg_id}")
                    driver.find_element(By.XPATH,
                                        '//*[@id="root"]/div/div[5]/div[2]/div[1]/div/div[4]/div/div').click()
                    time.sleep(1)




                time.sleep(1)
                driver.implicitly_wait(20)
                nick_name = driver.find_element(By.XPATH,
                                          '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[1]/div/span[1]').text
                time.sleep(1)
                driver.implicitly_wait(20)
                driver.find_element(By.XPATH,
                                    '//*[@id="root"]/div/div[5]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/input').send_keys(
                    f"{redeem_code}")

                driver.find_element(By.XPATH, '//*[@id="root"]/div/div[5]/div[2]/div/div/div[2]/div[2]/div/div').click()
                time.sleep(1)
                uc_amount = driver.find_element(By.CLASS_NAME, 'PopConfirmRedeem_item_mess__CKh92').text

                print(uc_amount)

                print("here 1")
                try:
                    driver.implicitly_wait(20)
                    driver.find_element(By.XPATH, '//*[@id="root"]/div/div[5]/div[4]/div[2]/div[2]/div[4]/div/div').click()



                    try:
                        time.sleep(2)
                        submit_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[5]/div[4]/div[2]/div[2]/div[5]/div/div/div/div').text
                        print(submit_btn)
                        if submit_btn == "Submit":
                            used_code = True
                            app.edit_message_text(chat_id=message.chat.id, message_id=y.id,
                                                  text=f"**• TopUP Unsuccessful ❌**\n\n**• TOPUP ID:** {topup}\n**• Player ID:** {pubg_id}\n**• UC AMOUNT:** {amount_top_up} UC\n**• CODE USED:** {redeem_code}")
                            message.reply("**Redemption code is redeemed by someone else. Contact Seller🫨** \n\n<i>• Note: The code has been removed from the database.</i>")
                            return True
                        else:
                            return False
                    except:
                        print("Element does not exist.")
                        pass
                    driver.implicitly_wait(1)
                except:
                    invalid_code = True
                    app.edit_message_text(chat_id=message.chat.id, message_id=y.id,
                                          text=f"**• TopUP Unsuccessful ❌**\n\n**• TOPUP ID:** {topup}\n**• Player ID:** {pubg_id}\n**• UC AMOUNT:** {amount_top_up} UC\n**• CODE USED:** {redeem_code}")
                    message.reply(
                        "**Code format invalid. Contact Seller🫨** \n\n<i>• Note: The code has been removed from the database.</i>")

                    return True
            except Exception as e:
                print(e)
                cursor.execute(f'''SELECT COUNT(UC{redeem_amount}) FROM {message.chat.username}''')
                last = cursor.fetchone()[0]
                cursor.execute(
                    f'''UPDATE {message.chat.username} SET UC{amount_add} = ? WHERE list_id = ?''', (redeem_code, last))
                conn.commit()
                app.edit_message_text(chat_id=message.chat.id, message_id=y.id,
                                     text=f"TopUP Unsuccessful ❌")
            finally:
                print("here 2")
                if not used_code and not invalid_code:

                    print("also here")
                    confirmation = ""
                    time.sleep(2)
                    #//*[@id="root"]/div/div[5]/div[3]/div[3]/div/div[2]/p
                    try:
                        driver.implicitly_wait(10)
                        confirmation = driver.find_element(By.CLASS_NAME, 'PopPurchaseSuccess_title__4XikX').text
                        print(confirmation)
                        if confirmation == "Redeem Successful":
                            app.edit_message_text(chat_id=message.chat.id, message_id=y.id, text=f"**• TopUP Successful ✅\n\n• TOPUP ID:** {topup}\n**• Player ID:** {pubg_id}\n**• Nickname: **{nick_name}\n**• UC AMOUNT: **{uc_amount}\n**• CODE USED:** {redeem_code}\n\n<i>• Note: The code has been removed from the database.</i>")
                            conn = sqlite3.connect('ragner_codes.db')
                            cursor = conn.cursor()
                            isodate = str(datetime.date.today().isoformat())
                            cursor.execute(f'''SELECT * FROM {message.chat.username}_stats WHERE date = ?''', (isodate,))
                            existing_row = cursor.fetchone()
                            if existing_row is None:
                                insert_row_for_new_date(isodate, message)
                            cursor.execute(f'''SELECT UC{redeem_amount} FROM {message.chat.username}_stats WHERE date = ?''', (isodate,))
                            result = cursor.fetchone()[0]
                            print(result)
                            cursor.execute(f'''UPDATE {message.chat.username}_stats 
                                                 SET UC{redeem_amount} = ?
                                                 WHERE date = ?''', (int(result)+1, isodate))
                            conn.commit()

                            driver.get("https://www.midasbuy.com/midasbuy/my/usercenter#transactionPage")
                            driver.implicitly_wait(60)
                            driver.find_element(By.XPATH,
                                                '//*[@id="app"]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div[1]').click()
                            time.sleep(1)
                            driver.save_screenshot("ss.png")
                            image = Image.open("ss.png")
                            # Crop the image
                            cropped_image = image.crop((500, 150, 1200, 600))

                            # Save the cropped image
                            cropped_image.save("trx.png")
                            app.send_photo(chat_id=message.chat.id, photo="trx.png")
                            return True
                        else:
                            cursor.execute(f'''SELECT COUNT(UC{redeem_amount}) FROM {message.chat.username}''')
                            last = cursor.fetchone()[0]
                            cursor.execute(
                                f'''UPDATE {message.chat.username} SET UC{redeem_amount} = {redeem_code} WHERE list_id = {last}''')
                            conn.commit()
                            app.edit_message_text(chat_id=message.chat.id, message_id=y.id,
                                                  text=f"**• TopUP Unsuccessful ❌**\n\n**• TOPUP ID:** {topup}\n**• Player ID:** {pubg_id}\n**• UC AMOUNT:** {amount_top_up} UC\n**• CODE USED:** {redeem_code}")
                            driver.quit()
                            return False
                    except Exception as ex:
                        cursor.execute(f'''SELECT COUNT(UC{redeem_amount}) FROM {message.chat.username}''')
                        last = cursor.fetchone()[0]
                        cursor.execute(
                            f'''UPDATE {message.chat.username} SET UC{amount_add} = ? WHERE list_id = ?''', (redeem_code, last))

                        conn.commit()
                        app.edit_message_text(chat_id=message.chat.id, message_id=y.id,
                                              text=f"**• TopUP Unsuccessful ❌**\n\n**• TOPUP ID:** {topup}\n**• Player ID:** {pubg_id}\n**• UC AMOUNT:** {amount_top_up} UC\n**• CODE USED:** {redeem_code}")
                        print(ex)
                    finally:
                        driver.quit()
                driver.quit()
    else:
        message.reply("**Insufficient codes!**")

def activation_thread(midas_id, amount_top_up, message,app):
    thread = threading.Thread(target=activate, args=(midas_id, amount_top_up, message, app))
    thread.start()
    thread.join()  # Wait for the thread to complete


def wait_and_print(zzz):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(f'--user-data-dir=ChromeProfiles\\{id_list[zzz]}')
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.midasbuy.com/midasbuy/my/redeem/pubgm")
    time.sleep(10)
    driver.quit()


def run_function_in_thread(id):
    """
    Runs the wait_and_print function in a separate thread.
    """

    thread = threading.Thread(target=wait_and_print, args=(id,))
    thread.start()
    thread.join()  # Wait for the thread to complete

app.run()
