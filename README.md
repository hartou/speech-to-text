# Speech-to-text

Speech-To-Text using Azure Cognitive Service

# How to run this example?

## Step 1 : Create the "utils.py" file 

Create the "utils.py" file add the AZURE_SPEECH_KEY, AZURE_SERVICE_REGION

## Step 2: Create your virtual environment 
 I
 For my virtual environment, I use pipenv. Use the following link to set up environment : Here [https://pypi.org/project/pipenv/]
 # Step 3: Transcribe .WAV files 

# Step 4 : Transcribe mp3 to file 

```sh
    python transcribe-mp3-to-file.py 
```
# Step 5 : Running Batch transcript  (.wav)

```sh
python callback_batch_transcript.py
```