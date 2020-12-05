# bamBOOK

### Simplified Text-to-Speech
At a small cost of fluency, much less crazy to install:

`python3 simplified_tts.py`

### Archived
To install the necessary packages, enter the following in the terminal:   
`pip install -r requirements.txt`

In your terminal, use `pwd` to help you determine the path to the file `serv_acc_key.json`.  For me, the filepath was `/Users/georgehong/Documents/bamBOOK/serv_acc_key.json`.

Now type:

`export GOOGLE_APPLICATION_CREDENTIALS={your path}`

Example:

`export GOOGLE_APPLICATION_CREDENTIALS=/Users/georgehong/Documents/bamBOOK/serv_acc_key.json`


The output of `python3 first_tts.py` will be an MP3 file.
x