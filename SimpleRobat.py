import requests
import time
import os
import whisper





# ------------------------------
# تنظیمات اولیه
# ------------------------------
TOKEN="498463304:FaVAvywbm_iyvzoOn7RVqEqWOOCl9kg5gv4"


BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}"


VOICE_FOLDER = "voices"



if not os.path.exists(VOICE_FOLDER):
    os.makedirs(VOICE_FOLDER)



# ------------------------------
# بارگذاری مدل هوش مصنوعی
# ------------------------------

print("Loading Whisper Model...")

model = whisper.load_model("medium")


print("Model Loaded")



# ------------------------------
# گرفتن پیام‌های جدید
# ------------------------------

def get_updates(offset=None):

    url = BASE_URL + "/getUpdates"


    params = {}


    if offset:
        params["offset"] = offset



    response = requests.get(
        url,
        params=params
    )


    return response.json()





# ------------------------------
# گرفتن اطلاعات فایل صوتی
# ------------------------------

def get_file(file_id):


    url = BASE_URL + "/getFile"


    params = {

        "file_id": file_id

    }



    response = requests.get(
        url,
        params=params
    )



    return response.json()






# ------------------------------
# دانلود فایل صوتی
# ------------------------------

def download_voice(file_path):


    url = (
        f"https://tapi.bale.ai/file/bot"
        f"{TOKEN}/{file_path}"
    )



    response = requests.get(url)



    filename = (
        VOICE_FOLDER 
        + "/voice.ogg"
    )



    with open(filename,"wb") as file:

        file.write(
            response.content
        )



    return filename






# ------------------------------
# ارسال پیام
# ------------------------------

def send_message(chat_id,text):


    url = BASE_URL + "/sendMessage"



    data = {

        "chat_id": chat_id,

        "text": text

    }



    requests.post(

        url,

        json=data

    )





# ------------------------------
# تبدیل صوت به متن
# ------------------------------

def speech_to_text(filename):


    print(
        "Converting voice..."
    )


    result = model.transcribe(
        filename,
        language="fa",
        fp16=False,
        temperature=0,
        beam_size=5
    )


    text = result["text"]


    return text







# ------------------------------
# برنامه اصلی
# ------------------------------


def main():


    offset = None


    print(
        "Bot Started..."
    )



    while True:



        updates = get_updates(offset)



        for item in updates.get(
            "result",
            []
        ):



            offset = (
                item["update_id"]
                +
                1
            )



            message = item.get(
                "message"
            )



            if not message:

                continue



            chat_id = (
                message["chat"]["id"]
            )




            # اگر صوت بود

            if "voice" in message:



                print(
                    "Voice received"
                )



                file_id = (
                    message["voice"]["file_id"]
                )



                # دریافت آدرس فایل

                info = get_file(
                    file_id
                )



                file_path = (
                    info["result"]["file_path"]
                )



                # دانلود

                voice_file = download_voice(
                    file_path
                )



                # تبدیل

                text = speech_to_text(
                    voice_file
                )



                print(
                    text
                )



                send_message(

                    chat_id,

                    "متن صوت شما:\n\n"
                    +
                    text

                )



            else:



                text = message.get(
                    "text",
                    ""
                )



                send_message(

                    chat_id,

                    "لطفاً یک پیام صوتی ارسال کنید"

                )



        time.sleep(2)






if __name__ == "__main__":

    main()

# import torch

# print("Torch OK")
# print(torch.__version__)

# x = torch.rand(5,5)

# print(x)