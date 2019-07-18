#!/usr/bin/env python3

import speech_recognition as sr
import sys
import os
from os import path
import lib

# gui classess
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


class TRANSCRIBE:
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


class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title('FreePBX Transcription')
        self.root.geometry('480x120')
        # Control Full Frame
        full_frame = Frame(self.root)
        #
        #
        # Buttons Frame
        button_frame = Frame(full_frame)
        # Directory Button
        select_dir_button = Button(
            button_frame, text='Select Directory', command=self.getDIR).pack(side=LEFT, padx=5)
        # Recursive Button
        self.select_recursion = IntVar()
        select_recursion_check = Checkbutton(
            button_frame, text="Recursive", variable=self.select_recursion).pack(side=LEFT, padx=5)
        # File Buttons
        select_file_button = Button(
            button_frame, text='Select File', command=self.getFILE).pack(side=LEFT, padx=5)
        # FreePBX Check
        self.select_freepbx = IntVar()
        select_freepbx_check = Checkbutton(
            button_frame, text="FreePBX Dir/File", variable=self.select_freepbx).pack(side=LEFT, padx=5)
        # Add buttons frame to window
        button_frame.pack(pady=(20, 10), padx=10, side=TOP)
        #
        #
        #
        # Trascribe Frame
        transcribe_frame = Frame(full_frame)
        # Transcribe Types
        self.transcribe_type = StringVar()
        audio_recognition_types = ['sphinx', 'google', 'google_cloud', 'wit', 'azure', 'bing', 'houndify', 'ibm']
        audio_recognition_type_menu = Spinbox(
            transcribe_frame, values=audio_recognition_types, textvariable=audio_recognition_types, state='readonly').pack(side=LEFT)
        # Transcribe Button
        transcribe_button = Button(
            transcribe_frame, text='Transcribe', command=self.transcribe).pack(side=LEFT, padx=20)
        # Add transcribe frame to window
        transcribe_frame.pack(pady=(10, 20), padx=10, side=BOTTOM)
        #
        #
        # Add Full Frame
        full_frame.pack()

        # Run man GUI threads
        self.root.mainloop()

    def getDIR(self):
        self.directory = filedialog.askdirectory()
        self.transcribe_type = 'dir'

    def getFILE(self):
        self.filename = filedialog.askopenfilename()
        self.transcribe_type = 'file'

    def transcribe(self):
        trans_type = self.transcribe_type.get()
        if(self.transcribe_type == 'dir'):
            self.transcribeDirectory(self.directory, trans_type)
        elif(self.transcribe_type == 'file'):
            self.transcribeFile(self.filename, trans_type)
        else:
            messagebox.showinfo(
                "Error", "You must either select a directory or file to Transcribe")

    def transcribeFile(self, filename, trans_type):
        wav_file = filename
        AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), wav_file)
        # use the audio file as the audio source
        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)  # read the entire audio file
        last_index = wav_file.rfind('/')
        print(wav_file[last_index+1:-4])
        text_file = open("transcript_of_" +
                         wav_file[last_index+1:-4] + ".txt", "w")
        print("Transcribing: %s" % wav_file[2:])
        print(trans_type)
        sys.exit()
        text_file.write(TRANSCRIBE.trans_type(self, r, audio) + "\n\n")
        text_file.close()
        print('Finished file: %s' % wav_file[2:])

    def transcribeDirectory(self, directory_path, trans_type):
        # get all directories
        os.chdir(directory_path)
        if(self.select_recursion.get()):
            directories = next(os.walk('.'))[1]

            # loop through each direction
            for directory in directories:
                os.chdir(directory)
                print(os.getcwd())

                # create a new text file with the name of the current working directory
                cwd = str(os.getcwd())
                last_index = cwd.rfind('\\')
                text_file = open("transcript_of_" +
                                 cwd[last_index+1] + ".txt", "w")

                # count all wav files in working directory
                count = 1
                wav_count = 0
                for wav_file in os.listdir('./'):
                    if wav_file.endswith(".wav"):
                        wav_count += 1

                try:
                    # convert wav files to text
                    for wav_file in os.listdir('./'):
                        if wav_file.endswith(".wav"):
                            AUDIO_FILE = path.join(path.dirname(
                                path.realpath(__file__)), wav_file)
                            # use the audio file as the audio source
                            r = sr.Recognizer()
                            with sr.AudioFile(AUDIO_FILE) as source:
                                # read the entire audio file
                                audio = r.record(source)
                            message_text_file = open(
                                (wav_file[:-3] + 'txt'), "r")
                            skip = False

                            if(self.select_freepbx.get()):
                                # get text data from txt file acconting the wav file
                                for line_number, line in enumerate(message_text_file):
                                    if(line_number == 11):
                                        # .replace("<", "").replace(">", "")
                                        caller = line[line.index(
                                            '\"') + 1:-1].replace("\"", '')
                                    elif(line_number == 12):
                                        timestamp = line[line.index(
                                            '=') + 1:-1]
                                    elif(line_number == 17 and "duration=0" in line):
                                        skip = True
                                if(skip):
                                    text_file.write(
                                        caller + ' ' + timestamp + "\n" + "No Audio" + "\n\n")
                                else:
                                    text_file.write(
                                        caller + ' ' + timestamp + "\n" + self.functions[self.transcribe_type](self, r, audio) + "\n\n")
                                print("message " + str(count) + " of " +
                                      str(wav_count) + " finished")
                                count += 1

                    # close transcript.txt file
                    text_file.close()
                except Exception as e:
                    text_file.close()
                    os.remove(str(text_file.name))
                    print(e)

                os.chdir('../')


if __name__ == "__main__":
    main_thread = GUI()
