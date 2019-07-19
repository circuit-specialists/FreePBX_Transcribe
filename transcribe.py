import speech_recognition as sr

class TRANSCRIBE(type, r, audio):
    def sphinx(self, r, audio):
        try:
            return r.recognize_sphinx(audio)
        except sr.UnknownValueError:
            return "Sphinx could not understand audio"
        except sr.RequestError as e:
            return "Sphinx error; {0}".format(e)

    def google(self, r, audio):
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            return "Could not request results from Google Speech Recognition service; {0}".format(e)

    def google_cloud(self, r, audio):
        GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""INSERT THE CONTENTS OF THE GOOGLE CLOUD SPEECH JSON CREDENTIALS FILE HERE"""
        try:
            return r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
        except sr.UnknownValueError:
            return "Google Cloud Speech could not understand the audio"
        except sr.RequestError as e:
            return "Could not request results from Google Cloud Speech service; {0}".format(e)

    def wit(self, r, audio):
        # Wit.ai keys are 32-character uppercase alphanumeric strings
        WIT_AI_KEY = "INSERT WIT.AI API KEY HERE"
        try:
            return r.recognize_wit(audio, key=WIT_AI_KEY)
        except sr.UnknownValueError:
            return "Wit.ai could not understand audio"
        except sr.RequestError as e:
            return "Could not request results from Wit.ai service; {0}".format(e)

    def azure(self, r, audio):
        # Microsoft Speech API keys 32-character lowercase hexadecimal strings
        AZURE_SPEECH_KEY = "INSERT AZURE SPEECH API KEY HERE"
        try:
            return r.recognize_azure(audio, key=AZURE_SPEECH_KEY)
        except sr.UnknownValueError:
            return "Microsoft Azure Speech could not understand audio"
        except sr.RequestError as e:
            return "Could not request results from Microsoft Azure Speech service; {0}".format(e)

    def bing(self, r, audio):
        # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
        BING_KEY = "INSERT BING API KEY HERE"
        try:
            return r.recognize_bing(audio, key=BING_KEY)
        except sr.UnknownValueError:
            return "Microsoft Bing Voice Recognition could not understand audio"
        except sr.RequestError as e:
            return "Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e)

    def houndify(self, r, audio):
        # Houndify client IDs are Base64-encoded strings
        HOUNDIFY_CLIENT_ID = "INSERT HOUNDIFY CLIENT ID HERE"
        # Houndify client keys are Base64-encoded strings
        HOUNDIFY_CLIENT_KEY = "INSERT HOUNDIFY CLIENT KEY HERE"
        try:
            return r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY)
        except sr.UnknownValueError:
            return "Houndify could not understand audio"
        except sr.RequestError as e:
            return "Could not request results from Houndify service; {0}".format(e)

    def ibm(self, r, audio):
        # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
        IBM_USERNAME = "INSERT IBM SPEECH TO TEXT USERNAME HERE"
        # IBM Speech to Text passwords are mixed-case alphanumeric strings
        IBM_PASSWORD = "INSERT IBM SPEECH TO TEXT PASSWORD HERE"
        try:
            return r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD)
        except sr.UnknownValueError:
            return "IBM Speech to Text could not understand audio"
        except sr.RequestError as e:
            return "Could not request results from IBM Speech to Text service; {0}".format(e)