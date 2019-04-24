# ligeia
*Python3 Package for voice synthesis using eSpeak and PicoTTS.*

## Installation
### Install with pip
```
pip3 install -U ligeia
```

## Usage
```
In [1]: from ligeia import eSpeak, PicoTTS, VoiceController

In [2]: voice_controller = VoiceController()

In [3]: voice_controller.load_voice(PicoTTS)

In [4]: voice_controller.say("Hello world.")

Say (Silent: False) > Hello world.

In [5]: voice_controller.load_voice(PicoTTS)

In [6]: voice_controller.generate_file(destiny_path="picotts_hello.wav", text="Hello world")
Out[6]: CompletedProcess(
    args='pico2wave   --lang en-US --wave hello.wav "hello world"', returncode=0
    )

In [7]: voice_controller.load_voice(eSpeak)

In [8]: voice_controller.say("Hello world.")

Say (Silent: False) > Hello world.
/bin/sh: 1: Syntax error: Unterminated quoted string

In [9]: voice_controller.generate_file(destiny_path="espeak_hello.wav", text="Hello world")
Out[9]: CompletedProcess(
    args='espeak -v en  -p 30 -a 200 -w hello.wav "Hello world"',
    returncode=0
    )
```
