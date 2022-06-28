from datetime import datetime
from fileinput import filename
import time
from utils import AZURE_SERVICE_REGION,AZURE_SPEECH_KEY
import azure.cognitiveservices.speech as speechsdk

# Add your subscription key and endpoint
subscription_key= AZURE_SPEECH_KEY

# This is required if using a Cognitive Services resource.
location = AZURE_SERVICE_REGION
# Create the file that while receive the transcriptions
def create_file():
    x = datetime.now()
    file_name = x.strftime('%d-%m-%Y-%H-%M-%S.txt')
    # create a empty text file
    fp = open(file_name, 'w')
    fp.write(f"New transcription file started {x.strftime('%d-%m-%Y-%H-%M-%S')}")
    fp.close()
    return file_name
    

class BinaryFileReaderCallback(speechsdk.audio.PullAudioInputStreamCallback):
    def __init__(self, filename: str):
        super().__init__()
        self._file_h = open(filename, "rb")

    def read(self, buffer: memoryview) -> int:
        print('trying to read {} frames'.format(buffer.nbytes))
        try:
            size = buffer.nbytes
            frames = self._file_h.read(size)

            buffer[:len(frames)] = frames
            print('read {} frames'.format(len(frames)))

            return len(frames)
        except Exception as ex:
            print('Exception in `read`: {}'.format(ex))
            raise

    def close(self) -> None:
        print('closing file')
        try:
            self._file_h.close()
        except Exception as ex:
            print('Exception in `close`: {}'.format(ex))
            raise

def compressed_stream_helper(compressed_format,
        mp3_file_path):
    callback = BinaryFileReaderCallback(mp3_file_path)
    stream = speechsdk.audio.PullAudioInputStream(stream_format=compressed_format, pull_stream_callback=callback)
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=location)

    # speech_config = speechsdk.SpeechConfig(**default_speech_auth)
    audio_config = speechsdk.audio.AudioConfig(stream=stream)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(evt):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    def print_to_file(evt,filename):
        print('RECOGNIZED: {}'.format(evt))
        with open(filename, "a+") as file:  
            file.seek(0)   
            content = file.read(30)
            if len(content) > 0 :
                file.write("\n")
                file.write(evt)
            file.close()
        
        
    filename=create_file()
    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    # speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print_to_file(evt=evt.result.text,filename=filename))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(5)

    speech_recognizer.stop_continuous_recognition()

def pull_audio_input_stream_compressed_mp3(mp3_file_path: str):
    # Create a compressed format
    compressed_format = speechsdk.audio.AudioStreamFormat(compressed_stream_format=speechsdk.AudioStreamContainerFormat.MP3)
    compressed_stream_helper(compressed_format, mp3_file_path)

#=====
mp3_file_path="audio/GRF19740809_64kb.mp3"
pull_audio_input_stream_compressed_mp3(mp3_file_path)