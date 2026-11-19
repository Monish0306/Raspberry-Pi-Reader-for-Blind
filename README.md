# Raspberry Pi-Based Voice-Controlled Assistive Reader

### Printed Text Recognition and Text-to-Speech System for Visually Impaired Users

[![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi-red)]()
[![Language](https://img.shields.io/badge/Language-Python-blue)]()
[![Computer
Vision](https://img.shields.io/badge/Computer%20Vision-OpenCV-green)]()
[![OCR](https://img.shields.io/badge/OCR-Tesseract-orange)]()
[![License](https://img.shields.io/badge/License-To%20Be%20Specified-lightgrey)]()


## 1. Project Overview

The **Raspberry Pi-Based Voice-Controlled Assistive Reader** is an
embedded assistive-technology system designed to help visually impaired
users access printed information independently. It captures an image of
printed text through a webcam, improves the image using computer-vision
preprocessing, extracts text with Tesseract Optical Character
Recognition (OCR), and converts the recognized content into spoken audio
using a Text-to-Speech (TTS) engine.

The system is controlled through voice input received by a microphone. A
16×2 LCD provides live status messages, while three GPIO-connected LEDs
communicate the system state: blue for processing, green when readable
text is detected, and red when text cannot be recognized. A speaker or
earphones deliver the spoken output.

The Raspberry Pi runs the application on **Raspberry Pi OS**. A laptop
is used for development and remote operation: **PuTTY** provides SSH
terminal access, while **WinSCP** transfers project files and
captured/processed images between the laptop and Raspberry Pi for
inspection.

## 2. Problem Statement

Printed material is not directly accessible to many people with visual
impairments. Conventional reading often requires assistance from another
person or specialized equipment. This project addresses that
accessibility challenge by combining low-cost embedded hardware with
computer vision, OCR, voice interaction, and speech synthesis.

## 3. Project Objectives

-   Capture printed text using a webcam after a voice command is
    recognized.
-   Improve captured image quality before recognition.
-   Apply grayscale conversion, noise reduction, contrast improvement,
    and thresholding to prepare images for OCR.
-   Extract machine-readable text using Tesseract OCR.
-   Convert recognized text into speech through a TTS engine.
-   Provide clear system feedback through an LCD and status LEDs.
-   Support remote development, execution, file transfer, and image
    inspection using a laptop.

## 4. Key Features

-   **Voice-activated operation:** microphone input is used to trigger
    the reading workflow.
-   **Camera-based text acquisition:** captures printed documents or
    text for processing.
-   **OpenCV preprocessing:** applies grayscale conversion, denoising,
    and thresholding; additional enhancement can be used where required.
-   **Tesseract OCR:** converts text present in the processed image into
    digital text.
-   **Text-to-Speech output:** reads the extracted text aloud through a
    speaker or earphones.
-   **LCD status monitoring:** displays short messages such as system
    ready, capturing, processing, text found, and no readable text.
-   **Three-colour LED feedback:** blue indicates processing, green
    indicates successful text detection, and red indicates an
    unsuccessful or unreadable result.
-   **Remote development workflow:** PuTTY is used to access the Pi
    terminal and run the program; WinSCP is used to transfer and inspect
    files.

## 5. System Workflow

``` text
                 ┌──────────────────────┐
                 │ Raspberry Pi OS     │
                 │ Application starts  │
                 └──────────┬───────────┘
                            │
                 ┌──────────▼───────────┐
                 │ Microphone           │
                 │ Voice command input  │
                 └──────────┬───────────┘
                            │ Command recognized
                 ┌──────────▼───────────┐
                 │ Webcam               │
                 │ Capture text image   │
                 └──────────┬───────────┘
                            │
                 ┌──────────▼───────────┐
                 │ OpenCV preprocessing │
                 │ Grayscale conversion │
                 │ Noise reduction      │
                 │ Thresholding         │
                 └──────────┬───────────┘
                            │ Enhanced image
                 ┌──────────▼───────────┐
                 │ Tesseract OCR        │
                 │ Text recognition     │
                 └──────────┬───────────┘
                            │
                   ┌────────▼────────┐
                   │ Readable text?  │
                   └────┬────────┬───┘
                     Yes│        │No
                        │        │
             ┌──────────▼───┐  ┌─▼────────────────┐
             │ Extracted    │  │ LCD: No readable │
             │ text         │  │ text; Red LED ON │
             └──────┬───────┘  └──────────────────┘
                    │
             ┌──────▼────────┐
             │ TTS engine    │
             │ Text to speech│
             └──────┬────────┘
                    │
             ┌──────▼────────┐
             │ Speaker /     │
             │ earphones     │
             └───────────────┘

       LCD and LEDs provide status feedback throughout.
```

## 6. Detailed Working Process

### Step 1 --- System initialization

When the Raspberry Pi is powered on, Raspberry Pi OS loads and the
Python application is started. The program initializes the camera,
microphone/audio input, speaker/audio output, LCD interface, and GPIO
pins used by the LEDs.

-   **LCD:** `System Started` or `System Ready`
-   **LEDs:** all LEDs remain off or briefly indicate initialization,
    depending on the implementation.

### Step 2 --- Voice command input

The microphone receives the user's voice. The voice-input component
listens for the configured trigger command (for example, "Hi" or
"Start"). When the command is recognized, the application begins the
reading sequence.

-   **LCD:** `Waiting for Command`, followed by `Command Detected`
-   **Blue LED:** turns on to indicate that the operation is active.

> The exact speech-recognition library and trigger phrase depend on the
> implementation. They are intentionally not specified here because they
> have not been confirmed.

### Step 3 --- Image capture using the webcam

After the trigger command is accepted, the webcam captures an image
containing the printed text. The image is made available to the
image-processing pipeline, either in memory or as a saved image file.

A clear image is important: adequate lighting, correct focus, a steady
camera, and a view that is reasonably parallel to the page improve OCR
performance.

-   **LCD:** `Capturing Image`
-   **Blue LED:** remains on.
-   **Capture error:** the LCD can display `Capture Failed`, and the red
    LED can indicate the error.

### Step 4 --- Image preprocessing with OpenCV

The captured image may contain colour information, uneven lighting,
shadows, or small visual disturbances. OpenCV is used to prepare the
image for OCR.

1.  **Grayscale conversion:** converts the colour image into shades of
    gray. This reduces image complexity and makes later processing
    easier.
2.  **Noise reduction:** applies a suitable filtering method to reduce
    unwanted speckles or image noise while retaining character edges as
    much as possible.
3.  **Contrast enhancement (if required):** improves the distinction
    between text and its background, especially when lighting is uneven.
4.  **Thresholding / binarization:** converts the grayscale image into a
    high-contrast representation, usually dark text against a light
    background. Adaptive or Otsu thresholding may be selected depending
    on the image.
5.  **Optional geometric or morphological correction:** deskewing,
    resizing, or morphological operations can be applied when the
    captured page is tilted, text is too small, or character strokes are
    broken.

The output is a processed image intended to make the printed characters
easier for Tesseract to recognize. The exact preprocessing sequence and
parameters should be matched to the code actually used.

-   **LCD:** `Processing Image`, with brief messages such as
    `Grayscale`, `Noise Reduction`, or `Thresholding` if implemented.
-   **Blue LED:** on during preprocessing.

### Step 5 --- Text recognition using Tesseract OCR

The preprocessed image is passed to **Tesseract OCR**. Tesseract
analyses the image and recognizes visible character patterns, converting
them into a digital text string.

The application checks the OCR result to determine whether usable text
was extracted. A practical implementation can check whether the returned
string is empty and, optionally, use word-confidence values to reject
very poor results.

-   **LCD during OCR:** `Reading Image` or `OCR Processing`
-   **Blue LED:** on while recognition is in progress.

### Step 6 --- Text validation and result handling

After OCR, the program checks the extracted text.

**If readable text is found:** - The extracted text is retained for
speech conversion. - The LCD displays `Text Found` or `Text Detected`. -
The green LED turns on, while red and blue are turned off or changed
according to the program's state logic.

**If no readable text is found:** - The LCD displays `No Readable Text`
or `No Text Found`. - The red LED turns on. - The application can return
to listening mode or request another capture.

A non-empty OCR result does not guarantee perfect recognition. Image
quality and OCR confidence should be considered when deciding whether
the result is sufficiently readable.

### Step 7 --- Text-to-Speech conversion

When usable text is available, it is passed to the configured
**Text-to-Speech (TTS)** engine. The TTS engine converts the text string
into synthesized speech.

The project description and resume draft identify **pyttsx3** as the
intended TTS library. It can provide offline speech synthesis when a
compatible local speech engine is installed and configured on Raspberry
Pi OS.

-   **LCD:** `Reading Text`
-   **Green LED:** indicates successful text detection / reading state,
    depending on the program's LED logic.
-   **Speaker or earphones:** play the synthesized speech.

### Step 8 --- Completion and standby

After speech playback finishes, the application can display
`Reading Complete` or `System Ready`, switch off the active status LEDs,
and return to voice-command listening mode. This allows the user to
start another reading cycle without restarting the Raspberry Pi.

### Step 9 --- File inspection and remote operation

The laptop supports development and monitoring but does not replace the
Raspberry Pi as the device running the project.

-   **Raspberry Pi OS:** operating system on which the Python
    application and required libraries execute.
-   **PuTTY:** establishes an SSH terminal session to the Raspberry Pi.
    It is used to log in, execute commands, start the Python program,
    and inspect terminal output.
-   **WinSCP:** transfers files between the laptop and Raspberry Pi
    using a supported file-transfer connection. It can be used to
    retrieve captured images, processed images, text output, and logs
    for inspection on the laptop.

WinSCP is a file-transfer and file-management tool; it does not itself
perform image processing or OCR.

## 7. Hardware Components

  -------------------------------------------------------------------------
                   No. Component                   Quantity Purpose
  -------------------- --------------- -------------------- ---------------
                     1 Raspberry Pi                       1 Main embedded
                       board                                computer; runs
                                                            Raspberry Pi OS
                                                            and the Python
                                                            application.

                     2 microSD card                       1 Stores
                                                            Raspberry Pi
                                                            OS, application
                                                            code,
                                                            libraries, and
                                                            project files.

                     3 Laptop / PC                        1 Used for
                                                            development,
                                                            remote access,
                                                            file transfer,
                                                            and result
                                                            inspection.

                     4 USB webcam                         1 Captures images
                                                            of printed
                                                            text.

                     5 Microphone                         1 Receives voice
                                                            commands to
                                                            trigger the
                                                            reading
                                                            process.

                     6 Speaker /                          1 Plays the
                       earphones                            synthesized
                                                            speech output.

                     7 16×2 character                     1 Displays system
                       LCD                                  messages and
                                                            processing
                                                            status.

                     8 Green LED                          1 Indicates
                                                            successful text
                                                            detection.

                     9 Red LED                            1 Indicates
                                                            unreadable text
                                                            or an error
                                                            state.

                    10 Blue LED                           1 Indicates
                                                            active
                                                            processing.

                    11 10 kΩ                              1 Adjusts LCD
                       potentiometer                        character
                                                            contrast.

                    12 220--330 Ω                At least 3 Limit current
                       resistors                            through the
                                                            three status
                                                            LEDs.

                    13 Breadboard                         1 Enables
                                                            temporary
                                                            circuit
                                                            prototyping
                                                            without
                                                            soldering.

                    14 Jumper wires             As required Connect GPIO,
                                                            LCD, LEDs,
                                                            power, and
                                                            ground.

                    15 Power adapter                      1 Supplies the
                                                            Raspberry Pi
                                                            with the
                                                            required stable
                                                            power.
  -------------------------------------------------------------------------

**Note:** The exact Raspberry Pi board model, webcam model, microphone
type, speaker type, and adapter rating were not specified. Select a
power adapter rated for the particular Raspberry Pi model and its
connected peripherals.

## 8. GPIO Pin Connections

### 8.1 LED connections

Each LED must be connected in series with its own 220--330 Ω
current-limiting resistor.

  -----------------------------------------------------------------------
  LED               Purpose           Anode (+), long   Cathode (−),
                                      leg               short leg
  ----------------- ----------------- ----------------- -----------------
  Green             Text detected /   GPIO 17 ---       Through a
                    success           physical pin 11   220--330 Ω
                                                        resistor to GND

  Red               No readable text  GPIO 27 ---       Through a
                    / failure         physical pin 13   220--330 Ω
                                                        resistor to GND

  Blue              Processing /      GPIO 22 ---       Through a
                    active state      physical pin 15   220--330 Ω
                                                        resistor to GND
  -----------------------------------------------------------------------

The resistor can be placed on either side of the LED as long as it is in
series. Use Raspberry Pi GPIO pins only within their electrical limits.

### 8.2 16×2 LCD connections --- 4-bit mode

The LCD uses four data lines (D4--D7), together with RS and E. The RW
pin is grounded to configure write-only operation.

  ------------------------------------------------------------------------
                LCD pin LCD signal       Raspberry Pi     Purpose
                                         connection       
  --------------------- ---------------- ---------------- ----------------
                      1 VSS              GND              Ground

                      2 VDD              5V               LCD power

                      3 V0               Middle terminal  Contrast
                                         of 10 kΩ         adjustment
                                         potentiometer    

                      4 RS               GPIO 26 ---      Register Select
                                         physical pin 37  

                      5 RW               GND              Write-only mode

                      6 E                GPIO 19 ---      Enable
                                         physical pin 35  

                      7 D0               Not connected    Unused in 4-bit
                                                          mode

                      8 D1               Not connected    Unused in 4-bit
                                                          mode

                      9 D2               Not connected    Unused in 4-bit
                                                          mode

                     10 D3               Not connected    Unused in 4-bit
                                                          mode

                     11 D4               GPIO 13 ---      Data bit 4
                                         physical pin 33  

                     12 D5               GPIO 6 ---       Data bit 5
                                         physical pin 31  

                     13 D6               GPIO 5 ---       Data bit 6
                                         physical pin 29  

                     14 D7               GPIO 11 ---      Data bit 7
                                         physical pin 23  

                     15 A / LED+         5V, through a    Backlight
                                         suitable         positive
                                         resistor if      
                                         required by the  
                                         LCD module       

                     16 K / LED−         GND              Backlight
                                                          negative
  ------------------------------------------------------------------------

**Potentiometer wiring:** connect one outer terminal to 5V, the other
outer terminal to GND, and the middle (wiper) terminal to LCD pin 3
(V0).

**Electrical caution:** Raspberry Pi GPIO uses 3.3V logic and is not 5V
tolerant. Check the LCD module's input-level requirements before
connecting its signals. Use suitable level shifting if the module can
drive a signal above 3.3V toward the Pi. Some LCD modules include a
backlight resistor; check the module before adding another. Never
connect 5V to a Raspberry Pi GPIO pin.

## 9. LCD and LED Status Reference

The messages below are suggested status labels. Use the exact text
supported by the available LCD width and the program implementation.

  System stage                 Example LCD message   LED indication
  ---------------------------- --------------------- ------------------------------------
  Startup                      `System Started`      Brief blue indication or all off
  Idle                         `Waiting Command`     All off
  Voice command accepted       `Command Detected`    Blue ON
  Image acquisition            `Capturing Image`     Blue ON
  Image preprocessing          `Processing Image`    Blue ON
  OCR execution                `OCR Processing`      Blue ON
  Text successfully detected   `Text Found`          Green ON
  Speech playback              `Reading Text`        Green ON (if configured)
  No usable text               `No Readable Text`    Red ON
  Camera or processing error   `Operation Failed`    Red ON
  Completed                    `Reading Complete`    LEDs off or brief green indication

## 10. Software and Technology Stack

  -----------------------------------------------------------------------
  Category                Technology / Tool       Role
  ----------------------- ----------------------- -----------------------
  Operating system        Raspberry Pi OS         Runs the application
                                                  and provides
                                                  hardware/software
                                                  support.

  Programming language    Python                  Implements the workflow
                                                  and connects the
                                                  software modules.

  Computer vision         OpenCV (`cv2`)          Image capture support
                                                  and preprocessing
                                                  operations.

  Image preprocessing     OpenCV functions        Grayscale conversion,
                                                  noise reduction,
                                                  contrast enhancement,
                                                  and thresholding.

  OCR engine              Tesseract OCR           Recognizes characters
                                                  and extracts text from
                                                  images.

  Python OCR interface    `pytesseract`           Allows Python code to
                                                  call Tesseract and
                                                  retrieve OCR text.

  Speech synthesis        TTS engine; `pyttsx3`   Converts extracted text
                          identified in the       into spoken output.
                          project description     

  GPIO control            `RPi.GPIO` or           Controls LED states and
                          compatible GPIO library LCD signal pins.

  Remote terminal         PuTTY (SSH)             Accesses the Raspberry
                                                  Pi command line and
                                                  runs the application.

  File transfer           WinSCP                  Transfers and inspects
                                                  project files between
                                                  the laptop and Pi.
  -----------------------------------------------------------------------

**Implementation accuracy note:** `pytesseract` is a Python wrapper; the
Tesseract OCR engine must also be installed on Raspberry Pi OS. The
specific speech-recognition library used for voice-command detection and
the exact LCD/GPIO Python package were not confirmed in the project
details available for this README. Add their actual package names after
checking the source code and installed environment.

## 11. OCR and Image-Processing Concepts

-   **OpenCV:** an open-source computer-vision library used to
    manipulate and enhance the captured image.
-   **Grayscale conversion:** transforms a colour image into intensity
    values, simplifying later processing.
-   **Noise reduction:** reduces unwanted pixel variations that may
    interfere with character recognition.
-   **Thresholding:** separates foreground text from the background by
    assigning pixels to contrasting values.
-   **Tesseract OCR:** an OCR engine that recognizes text in images.
    Modern Tesseract versions include an LSTM-based recognition engine.
-   **Text extraction:** converts recognized characters and words into a
    text string that can be stored or passed to TTS.
-   **Text-to-Speech:** synthesizes speech from the extracted text so
    the information can be heard.

This project uses a conventional OCR pipeline; it does not require a
separately trained machine-learning model. Tesseract provides the
text-recognition engine. Do not describe the project as using a
custom-trained AI model unless one is added separately.

## 12. Development and Experimental Setup

1.  Install Raspberry Pi OS on the microSD card and boot the Raspberry
    Pi.
2.  Connect the Raspberry Pi and laptop to a network that allows SSH and
    file transfer.
3.  Use PuTTY to connect to the Pi through SSH and access its terminal.
4.  Install Python dependencies and the Tesseract OCR system package.
5.  Connect the webcam, microphone, speaker, LCD, LEDs, and other
    circuit components.
6.  Wire the LEDs and LCD according to the GPIO tables in this README,
    with a common ground.
7.  Run basic hardware tests for camera capture, microphone input, audio
    playback, LCD output, and LED switching.
8.  Transfer the Python project files to the Pi using WinSCP or edit
    them on the Pi.
9.  Run the application through the PuTTY terminal.
10. Test with printed pages under different lighting, distances, camera
    angles, and text sizes.
11. Inspect captured and processed images, OCR text, and logs by
    transferring them to the laptop with WinSCP.

## 13. Testing and Evaluation

The system should be tested at each stage rather than only checking the
final speech output.

  -----------------------------------------------------------------------
  Test area               What to verify          Expected result
  ----------------------- ----------------------- -----------------------
  Voice input             Speak the configured    Command is recognized
                          trigger command         and capture begins

  Camera                  Capture a page with     Image is captured and
                          printed text            saved or passed to
                                                  processing

  Grayscale               Inspect the grayscale   Image is represented in
                          output                  gray intensity values

  Noise reduction         Compare before/after    Unwanted noise is
                          images                  reduced without losing
                                                  important text edges

  Thresholding            Inspect the binary      Text and background are
                          output                  clearly separated

  OCR                     Test clear printed text Tesseract returns
                                                  recognizable text

  No-text handling        Capture a blank or      System reports that no
                          unsuitable image        readable text was found

  TTS                     Send recognized text to Speech is played
                          the TTS engine          through the audio
                                                  output

  LCD                     Observe each workflow   Relevant status
                          stage                   messages appear

  LEDs                    Trigger success,        Correct LED illuminates
                          failure, and processing for each state
                          states                  

  File transfer           Retrieve images and     Files can be inspected
                          result files through    on the laptop
                          WinSCP                  
  -----------------------------------------------------------------------

For a formal evaluation, record OCR accuracy against manually verified
text, successful recognition rate, processing time, and performance
under different lighting and capture conditions. Do not claim a
numerical accuracy or real-time performance figure unless it has been
measured.

## 14. Error Handling and Limitations

-   **Voice command not recognized:** remain in listening mode and allow
    the user to repeat the command.
-   **Camera unavailable:** display a capture error and indicate failure
    with the red LED.
-   **Poor image quality:** request a new capture with better focus,
    lighting, or positioning.
-   **No readable text:** display an appropriate LCD message and do not
    send empty content to TTS.
-   **OCR mistakes:** recognition can be affected by blur, shadows,
    skew, small fonts, handwriting, complex layouts, and low contrast.
-   **Audio failure:** verify the selected audio output device and TTS
    engine configuration.
-   **Hardware power issues:** use a suitable power adapter and avoid
    drawing excessive current from GPIO pins.

The system's recognition quality depends on the captured image and the
OCR configuration. Tesseract is generally more suitable for clear
printed text than unconstrained handwriting.

## 15. Repository Structure

A suggested organization for the project is shown below. Adjust
filenames to match the actual repository.

``` text
raspberry-pi-assistive-reader/
├── README.md
├── main.py                  # Main application workflow
├── camera.py                # Webcam capture functions
├── preprocessing.py         # OpenCV image preprocessing
├── ocr.py                   # Tesseract OCR integration
├── speech.py                # Text-to-Speech functions
├── voice_input.py           # Voice-command handling
├── lcd_display.py           # LCD status display
├── led_control.py           # GPIO LED control
├── captured_images/         # Captured input images
├── processed_images/        # Preprocessed images for OCR
├── output/                  # Extracted text and output files
└── logs/                    # Application/debug logs
```

This is a recommended layout, not a claim about the current source-code
filenames.

## 16. Installation and Execution

The following is a general setup outline. Confirm the Raspberry Pi
model, Python version, and library compatibility before installing
packages.

### Update Raspberry Pi OS

``` bash
sudo apt update
sudo apt upgrade -y
```

### Install Tesseract OCR and common system dependencies

``` bash
sudo apt install -y tesseract-ocr python3-pip python3-venv
```

### Create and activate a Python virtual environment

``` bash
python3 -m venv .venv --system-site-packages
source .venv/bin/activate
```

### Install Python packages

``` bash
pip install opencv-python pytesseract pyttsx3
```

Install the GPIO, LCD, and speech-recognition packages required by the
actual source code. Their exact choices are not specified here. On
Raspberry Pi OS, camera and GPIO access may require additional system
configuration or permissions.

### Verify Tesseract

``` bash
tesseract --version
```

### Run the application

``` bash
python3 main.py
```

The command assumes the main entry-point file is named `main.py`.
Replace it with the actual filename if different.

## 17. Safety and Hardware Notes

-   Raspberry Pi GPIO pins operate at 3.3V logic and must not receive
    5V.
-   Use one 220--330 Ω resistor in series with each LED.
-   Connect all circuit grounds to a common GND reference.
-   Verify the LCD module's logic-level requirements before connecting
    it to the Pi.
-   Check whether the LCD backlight already has a current-limiting
    resistor.
-   Use a power adapter suitable for the exact Raspberry Pi model and
    peripheral load.
-   Disconnect power before changing breadboard wiring.

## 18. Future Enhancements

Possible extensions include:

-   Support for additional OCR languages.
-   Improved page-boundary detection and perspective correction.
-   Automatic image-quality checks before OCR.
-   Better handling of multi-column documents and complex layouts.
-   Text navigation through voice commands (repeat, pause, resume, next
    section).
-   Adjustable speech speed and voice selection.
-   Saving and organizing recognized text for later access.
-   A compact enclosure and improved camera mounting for portability.

These are proposed enhancements and should not be presented as completed
features unless they are implemented.

## 19. Conclusion

The Raspberry Pi-Based Voice-Controlled Assistive Reader demonstrates
how embedded computing, computer vision, OCR, and speech synthesis can
be integrated into an accessible reading aid. A microphone-triggered
workflow initiates webcam capture; OpenCV prepares the image; Tesseract
extracts printed text; and a TTS engine delivers the result through a
speaker. The LCD and GPIO-controlled LEDs provide clear status feedback,
while Raspberry Pi OS, PuTTY, and WinSCP support execution, remote
operation, and file inspection. The system offers a practical foundation
for making printed information more accessible to visually impaired
users.

## 20. Keywords

Raspberry Pi, Assistive Technology, OpenCV, Image Preprocessing,
Grayscale Conversion, Noise Reduction, Thresholding, Tesseract OCR,
Text-to-Speech, Python, GPIO, Embedded Systems.

------------------------------------------------------------------------

## Project Details to Confirm Before Publishing

To make this README exactly match the implemented build, verify and
update these details:

1.  Exact Raspberry Pi model (for example, Raspberry Pi 3 Model B or
    Raspberry Pi 4 Model B).
2.  Exact voice-command recognition library and the trigger phrase used.
3.  Exact TTS engine and whether speech works offline.
4.  Exact LCD and GPIO Python libraries.
5.  Whether the webcam image is captured directly by the Pi or sent from
    another device.
6.  Whether the application actually saves captured images, processed
    images, OCR text, and logs.
7.  Exact repository filename and folder structure.

The README deliberately distinguishes confirmed project features from
optional implementation details so it does not claim hardware,
libraries, or functionality that may not be present in the final code.
