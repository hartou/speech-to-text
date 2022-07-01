# Speech-to-text

Speech-To-Text using Azure Cognitive Service

# How to run this example?

## Step 1 : Create the "utils.py" file

- Create the "utils.py" file and add the AZURE_SPEECH_KEY, AZURE_SERVICE_REGION values from retrieved from the Azure portal.
- Keep the file at the folder root level. 
   
   ```bash
    /.
    /_utils.py
    ```


![](img/utils.py.png)

## Step 2: Create your virtual environment 
 
 For my virtual environment, I use pipenv. Visit the following link to set up the pipenv environment : [https://pypi.org/project/pipenv/]

# Step 3 : Transcribe mp3 to file 

```sh
    python transcribe-mp3-to-file.py 
```
# Step 4 : Running Batch transcript  (.wav)

```sh
python callback_batch_transcript.py
```