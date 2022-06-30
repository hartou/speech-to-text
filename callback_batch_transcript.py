#Dependencies 
import time
import wave
import azure.cognitiveservices.speech as speechsdk
from testcase import TESTCASES
from utils import AZURE_SERVICE_REGION,AZURE_SPEECH_KEY

#Functions 
def read_wav_file(filename):
    with wave.open(filename, 'rb') as w:
        rate = w.getframerate()
        frames = w.getnframes()
        buffer = w.readframes(frames)
    return buffer, rate

def simulate_stream(buffer: bytes, batch_size: int = 4096):
    buffer_len = len(buffer)
    offset = 0
    while offset < buffer_len:
        end_offset = offset + batch_size
        buf = buffer[offset:end_offset]
        yield buf
        offset = end_offset

def azure_streaming_stt(filename: str, lang: str, encoding: str) -> str:
    speech_config = speechsdk.SpeechConfig(
        subscription=AZURE_SPEECH_KEY,
        region=AZURE_SERVICE_REGION
    )
    stream = speechsdk.audio.PushAudioInputStream()
    audio_config = speechsdk.audio.AudioConfig(stream=stream)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(
        lambda evt: print('interim text: "{}"'.format(
            evt.result.text
        ))
    )
    speech_recognizer.recognized.connect(
        lambda evt:  print('azure-streaming-stt: "{}"'.format(
            evt.result.text
        ))
    )

    # start continuous speech recognition
    speech_recognizer.start_continuous_recognition()

    # push buffer chunks to stream
    buffer, rate = read_wav_file(filename)
    audio_generator = simulate_stream(buffer)
    for chunk in audio_generator:
      stream.write(chunk)
      time.sleep(0.1)  # to give callback a chance against fast loop

    # stop continuous speech recognition
    stream.close()
    time.sleep(0.5)  # give chance to VAD to kick in
    speech_recognizer.stop_continuous_recognition()
    time.sleep(0.5)  # Let all callback run


# Run tests
for t in TESTCASES:
    print('\naudio file="{0}"    expected text="{1}"'.format(
        t['filename'], t['text']
    ))
    azure_streaming_stt(t['filename'], t['lang'], t['encoding'])
    
# Run Batch Transcript
#azure_streaming_stt(filename='audio/GRF19740809.wav',lang='en-US',encoding='LINEAR16')