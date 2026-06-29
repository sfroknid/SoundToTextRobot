import requests
import time
import sqlite3
import json


# =====================
# TOKEN ربات بله
# =====================

TOKEN="498463304:FaVAvywbm_iyvzoOn7RVqEqWOOCl9kg5gv4"

API = f"https://tapi.bale.ai/bot{TOKEN}"


# =====================
# DATABASE
# =====================

conn = sqlite3.connect("bot.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id TEXT UNIQUE
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id TEXT,
    order_text TEXT
)
""")


conn.commit()



# ذخیره کاربر

def save_user(chat_id):

    try:
        cursor.execute(
            "INSERT INTO users(chat_id) VALUES(?)",
            (chat_id,)
        )

        conn.commit()

    except:
        pass



# ذخیره سفارش

def save_order(chat_id,text):

    cursor.execute(
        "INSERT INTO orders(chat_id,order_text) VALUES(?,?)",
        (chat_id,text)
    )

    conn.commit()



# =====================
# ارسال پیام
# =====================


def send_message(chat_id,text):

    url = API + "/sendMessage"


    data = {
        "chat_id": chat_id,
        "text": text
    }


    r=requests.post(url,data=data)

    print(r.text)



# =====================
# منوی اصلی
# =====================


def send_menu(chat_id):

    url = API + "/sendMessage"

    keyboard = {
        "keyboard": [
            [
                {
                    "text": "📦 ثبت سفارش"
                },
                {
                    "text": "📋 سفارش من"
                }
            ],
            [
                {
                    "text": "☎️ تماس با ما"
                },
                {
                    "text": "🤖 پشتیبانی"
                }
            ]
        ],
        "resize_keyboard": True
    }


    data = {
        "chat_id": chat_id,
        "text": "سلام 👋\nیک گزینه انتخاب کنید:",
        "reply_markup": json.dumps(keyboard, ensure_ascii=False)
    }


    response = requests.post(url, data=data)

    print("MENU:", response.text)


    requests.post(url,data=data)




# =====================
# دریافت پیام ها
# =====================


def get_updates(offset=None):


    url=API+"/getUpdates"


    params={}


    if offset:
        params["offset"]=offset


    r=requests.get(
        url,
        params=params
    )


    return r.json()



# =====================
# وضعیت کاربران
# =====================

user_state={}



print("ربات فعال شد")


offset=None



while True:


    data=get_updates(offset)


    if "result" in data:


        for item in data["result"]:


            offset=item["update_id"]+1


            message=item.get("message")


            if message:


                chat_id=message["chat"]["id"]

                text=message.get("text","")


                print(
                    "پیام:",
                    chat_id,
                    text
                )


                save_user(chat_id)



                # شروع


                if text=="/start":


                    send_menu(chat_id)



                # ثبت سفارش


                elif text=="📦 ثبت سفارش":


                    user_state[chat_id]="order"


                    send_message(
                        chat_id,
                        "لطفاً توضیح دهید چه سفارشی دارید؟"
                    )



                # دریافت سفارش


                elif user_state.get(chat_id)=="order":


                    save_order(
                        chat_id,
                        text
                    )


                    user_state[chat_id]=None


                    send_message(
                        chat_id,
                        "✅ سفارش شما ثبت شد.\n"
                        "به زودی با شما تماس می‌گیریم."
                    )



                # سفارش من


                elif text=="📋 سفارش من":


                    cursor.execute(
                        "SELECT order_text FROM orders WHERE chat_id=?",
                        (str(chat_id),)
                    )


                    result=cursor.fetchall()


                    if result:


                        msg="سفارش‌های شما:\n\n"


                        for r in result:

                            msg += "📌 "+r[0]+"\n"


                    else:

                        msg="هنوز سفارشی ثبت نکرده‌اید."


                    send_message(
                        chat_id,
                        msg
                    )



                # تماس


                elif text=="☎️ تماس با ما":


                    send_message(
                        chat_id,
                        "☎️ شماره تماس:\n09120000000"
                    )



                # پشتیبانی


                elif text=="🤖 پشتیبانی":


                    send_message(
                        chat_id,
                        "سؤال خود را ارسال کنید.\n"
                        "کارشناس پاسخ خواهد داد."
                    )



                else:


                    send_message(
                        chat_id,
                        "پیام شما دریافت شد."
                    )



    time.sleep(2)