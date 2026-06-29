

# Project Versions

## 1. Simple Speech-to-Text Version

**File: `SimpleRobot.py`**

This is the basic version of the project, designed for simple voice-to-text conversion tasks.

Features:

* Receiving voice messages from users
* Converting speech into text
* Simple and lightweight implementation
* Suitable for basic applications and testing the speech recognition workflow

This version provides the foundation of the project and can be extended with more advanced speech recognition models.

---

## 2. Offline Whisper Speech Recognition Version

**File: `voiceToTextWhispermedquality.py`**

This version uses **OpenAI Whisper** as an offline speech recognition engine.

The main advantage of this implementation is that it does not require a continuous internet connection. It can process audio locally and convert speech into text even when online speech recognition services are unavailable.

Features:

* Fully offline speech recognition
* No dependency on Google cloud services
* Suitable for environments with limited or unstable internet access
* Improved privacy because audio processing can be performed locally
* Good performance for Persian speech recognition

This version can be used as a reliable backup solution when cloud-based services have limitations or connectivity problems.

---

## 3. Advanced Whisper Model Version

**File: `VoiceToTextRobotLowQuality.py`**

This version is another implementation based on **OpenAI Whisper**, using different model configurations to achieve a balance between processing speed and recognition quality.

Features:

* Optimized Whisper model usage
* Faster processing compared with higher-quality models
* Lower hardware requirements
* Suitable for systems where execution speed is more important than maximum accuracy

This version provides flexibility by allowing developers to select different Whisper models depending on available hardware resources and application requirements.

---

## 4. High Accuracy Google Speech-to-Text Version

**File: `speechtotextgooglePerfect.py`**

This version integrates **Google Speech-to-Text API** to achieve high-quality speech recognition.

It provides excellent accuracy, especially for the Persian language, and performs very well in converting voice messages into text.

Features:

* High speech recognition accuracy
* Excellent Persian language support
* Cloud-based AI speech processing
* Suitable for professional and commercial applications
* Better performance in complex speech scenarios

However, this version depends on Google services and has limitations such as API usage restrictions, internet dependency, and service availability.

---

## 5. Audio File Processing Version

**File: `speechtotextgooglePerfectsendingFiles.py`**

This version extends the Google Speech-to-Text implementation by adding support for audio file processing.

In addition to receiving voice messages, users can send audio files directly to the robot, and the system processes them automatically.

Features:

* Support for voice messages and uploaded audio files
* Automatic audio processing workflow
* High-quality conversion using Google Speech-to-Text
* Suitable for applications that require processing recorded audio files

---

# Language Customization

The project supports language customization, especially for the Persian language. Developers can modify language parameters, recognition settings, and processing configurations to improve performance for different Persian speech patterns, accents, and specialized vocabulary.

---

# Future Development

Possible future improvements include:

* Adding automatic selection between offline Whisper and online Google recognition
* Creating a hybrid system that switches models based on internet availability
* Supporting more messaging platforms
* Adding database management for users and converted texts
* Improving Persian speech recognition accuracy using customized models

---

**SoundToTextRobot** provides a complete speech-to-text framework, from simple voice conversion to advanced AI-powered recognition, offering both offline reliability and cloud-based high accuracy.
