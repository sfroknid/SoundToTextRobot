import requests
import time
import os
import speech_recognition as sr
from pydub import AudioSegment

TOKEN = "498463304:FaVAvywbm_iyvzoOn7RVqEqWOOCl9kg5gv4"

BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}"
VOICE_FOLDER = "voices"

if not os.path.exists(VOICE_FOLDER):
    os.makedirs(VOICE_FOLDER)

recognizer = sr.Recognizer()

print("Bot Ready...")


def get_updates(offset=None):
    url = BASE_URL + "/getUpdates"
    params = {}
    if offset:
        params["offset"] = offset
    response = requests.get(url, params=params)
    return response.json()


def get_file(file_id):
    url = BASE_URL + "/getFile"
    params = {"file_id": file_id}
    response = requests.get(url, params=params)
    return response.json()


def download_voice(file_path):
    url = f"https://tapi.bale.ai/file/bot{TOKEN}/{file_path}"
    response = requests.get(url)
    filename = VOICE_FOLDER + "/voice.ogg"
    with open(filename, "wb") as f:
        f.write(response.content)
    return filename


def convert_audio(input_file):
    output_file = input_file.replace(".ogg", ".wav")
    audio = AudioSegment.from_file(input_file)
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)
    audio.export(output_file, format="wav")
    return output_file


def speech_to_text(filename):
    print("Transcribing...")
    with sr.AudioFile(filename) as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="fa-IR")
        return text
    except sr.UnknownValueError:
        return "صدا قابل تشخیص نبود"
    except sr.RequestError as e:
        return f"خطا در اتصال به سرویس گوگل: {e}"


def send_message(chat_id, text):
    url = BASE_URL + "/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, json=data)


def main():
    offset = None
    print("Bot Started...")

    while True:
        updates = get_updates(offset)

        for item in updates.get("result", []):
            offset = item["update_id"] + 1
            message = item.get("message")

            if not message:
                continue

            chat_id = message["chat"]["id"]

            if "voice" in message:
                print("Voice Received")

                file_id = message["voice"]["file_id"]
                info = get_file(file_id)
                file_path = info["result"]["file_path"]

                ogg_file = download_voice(file_path)
                wav_file = convert_audio(ogg_file)
                text = speech_to_text(wav_file)

                print(text)
                send_message(chat_id, "متن صوت:\n\n" + text)

            else:
                send_message(chat_id, "لطفاً یک ویس ارسال کنید")

        time.sleep(2)


if __name__ == "__main__":
    main()