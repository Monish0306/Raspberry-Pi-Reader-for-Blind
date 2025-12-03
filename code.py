import sys
import sounddevice as sd
import queue
import json
import cv2
import pytesseract
import RPi.GPIO as GPIO
from vosk import Model, KaldiRecognizer
from datetime import datetime
from RPLCD.gpio import CharLCD
from gtts import gTTS
import subprocess
import time
# =============================
# GPIO Setup (LED Indicators)
# =============================
GREEN_PIN = 17  # Success
RED_PIN = 27    # Failure
GPIO.setmode(GPIO.BCM)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(RED_PIN, GPIO.OUT)

def led_status(success=None):
    """Control LEDs based on success or failure"""
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(RED_PIN, GPIO.LOW)

    if success is True:
        GPIO.output(GREEN_PIN, GPIO.HIGH)
    elif success is False:
        GPIO.output(RED_PIN, GPIO.HIGH)
# =============================
# LCD Setup
# =============================
try:
    lcd = CharLCD(
        numbering_mode=GPIO.BCM,
        pin_rs=26,
        pin_e=19,
        pins_data=[13, 6, 5, 11],
        cols=16,
        rows=2,
        dotsize=8,
        auto_linebreaks=False
    )
    lcd.clear()
    lcd.write_string("System Started")
except Exception as e:
    lcd = None
    print("LCD Error:", e)
def lcd_print(msg):
    """Print message on LCD and console"""
    if lcd:
        lcd.clear()
        lines = msg.split('\n')
        lcd.cursor_pos = (0, 0)
        lcd.write_string(lines[0][:16])
    print("[LCD]:", msg)
# =============================
# VOSK Speech Recognition Setup
# =============================
model_path = "/home/sairam/vosk-model/model"
model = Model(model_path)
rec = KaldiRecognizer(model, 16000)
q = queue.Queue()
# =============================
# gTTS Voice Output
# =============================
def speak(text, lang="en"):
    """Convert text to speech using gTTS"""
    filename = "/home/sairam/voice.mp3"
    tts = gTTS(text=text, lang=lang, tld="co.in")
    tts.save(filename)
    subprocess.run(["mpg321", "-q", filename])
# =============================
# Microphone Callback
# =============================
def callback(indata, frames, time_data, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))
# =============================
# Capture & OCR Function
# =============================
def capture_and_read():
    """Capture image, preprocess, perform OCR, and speak text"""
    cap = cv2.VideoCapture(0)
    time.sleep(1)

    if not cap.isOpened():
        lcd_print("No Camera")
        speak("Camera not detected")
        led_status(success=False)
        return

    ret, frame = cap.read()
    cap.release()

    if not ret:
        lcd_print("Not Captured")
        speak("Failed to capture image")
        led_status(success=False)
        return
    lcd_print("Processing...")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    processed = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        17, 3
    )

    timestamp = datetime.now().strftime('%H%M%S')
    orig_file = f"/home/sairam/captured_{timestamp}.jpg"
    proc_file = f"/home/sairam/processed_{timestamp}.jpg"
    cv2.imwrite(orig_file, frame)
    cv2.imwrite(proc_file, processed)
    lcd_print("Images Saved")
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
    custom_config = r'--oem 3 --psm 3'

    text = pytesseract.image_to_string(processed, lang="eng", config=custom_config)
    cleaned_text = text.strip().replace('\n', ' ')

    if cleaned_text:
        led_status(success=True)
        lcd_print(f"Text Found:\n{cleaned_text[:16]}")
        print("OCR Output:", cleaned_text)
        speak("The text is " + cleaned_text)
    else:
        led_status(success=False)
        lcd_print("No Text Found")
        speak("No readable text found")
# =============================
# Main Loop
# =============================
try:
    with sd.RawInputStream(samplerate=16000, blocksize=8000,
                           dtype='int16', channels=1, callback=callback):
        lcd_print("Say 'Hi' to start")
        speak("Say hi to start the process")

        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if result["text"]:
                    spoken = result["text"].lower().strip()
                    print("You said:", spoken)

                    if "hi" in spoken:
                        lcd_print("Hi! Capturing...")
                        speak("Hello, capturing image now")
                        capture_and_read()

                    elif "exit" in spoken:
                        lcd_print("Exiting...")
                        speak("Exiting now")
                        break
except KeyboardInterrupt:
    pass
finally:
    if lcd:
        lcd_print("System Off")
    GPIO.cleanup()
    print("\nSystem Off. GPIO cleaned up.")
