import requests
import time
import os
import whisper
from pydub import AudioSegment


TOKEN=""



# ==============================
# تنظیمات
# ==============================

BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}"

VOICE_FOLDER = "voices"


if not os.path.exists(VOICE_FOLDER):
    os.makedirs(VOICE_FOLDER)



# ==============================
# بارگذاری Whisper
# ==============================

print("Loading Whisper Medium Model...")

model = whisper.load_model("medium")

print("Model Loaded")



# ==============================
# دریافت پیام از بله
# ==============================

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



# ==============================
# دریافت اطلاعات فایل
# ==============================

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



# ==============================
# دانلود صوت
# ==============================

def download_voice(file_path):


    url = (
        f"https://tapi.bale.ai/file/bot"
        f"{TOKEN}/{file_path}"
    )


    response = requests.get(url)


    filename = (
        VOICE_FOLDER
        +
        "/voice.ogg"
    )


    with open(filename, "wb") as f:

        f.write(
            response.content
        )


    return filename



# ==============================
# تبدیل OGG به WAV استاندارد
# ==============================

def convert_audio(input_file):


    output_file = (
        input_file.replace(
            ".ogg",
            ".wav"
        )
    )


    audio = AudioSegment.from_file(
        input_file
    )


    # تبدیل به حالت مناسب Whisper

    audio = audio.set_channels(1)

    audio = audio.set_frame_rate(
        16000
    )


    audio.export(
        output_file,
        format="wav"
    )


    return output_file



# ==============================
# تبدیل صوت به متن
# ==============================

def speech_to_text(filename):


    print(
        "Transcribing..."
    )


    result = model.transcribe(

        filename,

        language="fa",

        fp16=False,

        temperature=0,

        beam_size=5

    )


    return result["text"]




# ==============================
# ارسال پیام
# ==============================

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



# ==============================
# اجرای ربات
# ==============================


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



            if "voice" in message:


                print(
                    "Voice Received"
                )


                file_id = (
                    message["voice"]["file_id"]
                )


                # گرفتن مسیر فایل

                info = get_file(
                    file_id
                )


                file_path = (
                    info["result"]["file_path"]
                )



                # دانلود

                ogg_file = download_voice(
                    file_path
                )



                # تبدیل استاندارد

                wav_file = convert_audio(
                    ogg_file
                )



                # تبدیل به متن

                text = speech_to_text(
                    wav_file
                )


                print(
                    text
                )


                send_message(

                    chat_id,

                    "متن صوت:\n\n"
                    +
                    text

                )



            else:


                send_message(

                    chat_id,

                    "لطفاً یک ویس ارسال کنید"

                )



        time.sleep(2)




if __name__ == "__main__":

    main()