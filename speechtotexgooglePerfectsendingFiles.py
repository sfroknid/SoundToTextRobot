import requests
import time
import os
import speech_recognition as sr
from pydub import AudioSegment

TOKEN = "498463304:FaVAvywbm_iyvzoOn7RVqEqWOOCl9kg5gv4"
BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}"
VOICE_FOLDER = "voices"

SUPPORTED_FORMATS = [
    ".mp3", ".wav", ".ogg", ".m4a",
    ".flac", ".aac", ".wma", ".opus"
]

if not os.path.exists(VOICE_FOLDER):
    os.makedirs(VOICE_FOLDER)

recognizer = sr.Recognizer()
print("Bot Ready...")


# ==============================
# دریافت آپدیت
# ==============================

def get_updates(offset=None):
    url = BASE_URL + "/getUpdates"
    params = {}
    if offset:
        params["offset"] = offset
    response = requests.get(url, params=params)
    return response.json()


# ==============================
# دریافت اطلاعات فایل
# ==============================

def get_file(file_id):
    url = BASE_URL + "/getFile"
    params = {"file_id": file_id}
    response = requests.get(url, params=params)
    return response.json()


# ==============================
# دانلود فایل
# ==============================

def download_file(file_path, extension=".ogg"):
    url = f"https://tapi.bale.ai/file/bot{TOKEN}/{file_path}"
    response = requests.get(url)
    filename = os.path.join(VOICE_FOLDER, f"audio{extension}")
    with open(filename, "wb") as f:
        f.write(response.content)
    return filename


# ==============================
# تبدیل هر فرمتی به WAV
# ==============================

def convert_to_wav(input_file):
    output_file = os.path.join(VOICE_FOLDER, "audio.wav")
    try:
        audio = AudioSegment.from_file(input_file)
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)
        audio.export(output_file, format="wav")
        return output_file
    except Exception as e:
        print(f"Convert Error: {e}")
        return None


# ==============================
# تبدیل صوت به متن
# ==============================

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


# ==============================
# ارسال پیام
# ==============================

def send_message(chat_id, text):
    url = BASE_URL + "/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, json=data)


# ==============================
# پردازش فایل صوتی
# ==============================

def process_audio(chat_id, file_id, extension=".ogg"):
    info = get_file(file_id)
    file_path = info["result"]["file_path"]

    send_message(chat_id, "⏳ در حال پردازش...")

    downloaded = download_file(file_path, extension)
    wav_file = convert_to_wav(downloaded)

    if not wav_file:
        send_message(chat_id, "❌ خطا در تبدیل فایل صوتی")
        return

    text = speech_to_text(wav_file)
    send_message(chat_id, f"📝 متن صوت:\n\n{text}")


# ==============================
# اجرای ربات
# ==============================

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

            # ویس مستقیم
            if "voice" in message:
                print("Voice received")
                file_id = message["voice"]["file_id"]
                process_audio(chat_id, file_id, ".ogg")

            # فایل صوتی (audio)
            elif "audio" in message:
                print("Audio file received")
                audio_info = message["audio"]
                file_id = audio_info["file_id"]
                file_name = audio_info.get("file_name", "audio.mp3")
                extension = os.path.splitext(file_name)[-1].lower()

                if extension not in SUPPORTED_FORMATS:
                    send_message(
                        chat_id,
                        f"❌ فرمت {extension} پشتیبانی نمیشه\n\n"
                        f"✅ فرمت‌های مجاز:\n"
                        + "\n".join(SUPPORTED_FORMATS)
                    )
                    continue

                process_audio(chat_id, file_id, extension)

            # فایل عمومی (document)
            elif "document" in message:
                print("Document received")
                doc_info = message["document"]
                file_id = doc_info["file_id"]
                file_name = doc_info.get("file_name", "")
                extension = os.path.splitext(file_name)[-1].lower()

                if extension not in SUPPORTED_FORMATS:
                    send_message(
                        chat_id,
                        f"❌ فرمت {extension} پشتیبانی نمیشه\n\n"
                        f"✅ فرمت‌های مجاز:\n"
                        + "\n".join(SUPPORTED_FORMATS)
                    )
                    continue

                process_audio(chat_id, file_id, extension)

            else:
                send_message(
                    chat_id,
                    "🎙 لطفاً یک ویس یا فایل صوتی ارسال کنید\n\n"
                    "✅ فرمت‌های پشتیبانی شده:\n"
                    + "\n".join(SUPPORTED_FORMATS)
                )

        time.sleep(2)


if __name__ == "__main__":
    main()