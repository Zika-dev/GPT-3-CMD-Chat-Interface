print('Loading ...')
import playsound
import os
from time import sleep

import openai
import colorama
from colorama import Fore, Back, Style
from gtts import gTTS
import threading
from configparser import ConfigParser

config = ConfigParser()
colorama.init(autoreset=True)

try:
    f = open('key.ini', "r")
except:
    print(Fore.RED +'Key not found!')
    key = input('Enter your OpenAi api key: ')
    config['KEY'] = {
    'apiKey': key
    }
    with open('key.ini', 'w') as f:
        config.write(f)
    config.set('KEY', 'apikey', key)
    sleep(1)

config.read('key.ini')
key = config.get('KEY', 'apikey')
openai.api_key = key

try:
    response = openai.Completion.create(engine="text-ada-001", prompt='', max_tokens=1, temperature=0)
except:
    print(Fore.RED + '\nInvalid api-key / usage exceeded\nRestart program to reset settings')
    os.remove('key.ini')
    quit()

print(Fore.GREEN + 'Correct key!')
sleep(0.2)
conversation = ''

os.system('cls')
ttsChoice = ''
while ttsChoice != 'n' and ttsChoice != 'y':
    print('Input y/n')
    ttsChoice = input('Enable TTS? ')
os.system('cls')

while True:
    prompt = input(Fore.WHITE + "")
    if prompt == 'n':
        conversation=''
        print(Fore.YELLOW + 'New conversation in 1 second...')
        sleep(1)
        os.system('cls')
        continue
    elif prompt == ('s'):
        name = input(Fore.YELLOW + 'Name your conversation: ')
        if os.path.exists(f'{name}.txt'):
            overwriteChoose = ''
            while overwriteChoose != 'n' and overwriteChoose != 'y':
                print(Fore.WHITE + '\nInput y/n')
                overwriteChoose = input(Fore.RED+'Warning! This file already exists... Do you want to overwrite it?')
            if overwriteChoose == 'n':
                os.system('cls')
                continue
            elif overwriteChoose == 'y':
                os.remove(f'{name}.txt')
        f = open(f'{name}.txt', "x")
        f.write(conversation)
        f.close()
        print(Fore.GREEN + f'Successfully saved {name}')
        continue
    elif prompt == ('l'):
        load = input(Fore.YELLOW + 'Name of conversation: ')
        with open(load + '.txt', 'r') as file:
            data = file.read().replace('\n', ' ')
        conversation = data
        print(Fore.GREEN + f'Successfully loaded conversation: {load}\n' + Fore.YELLOW + 'Press enter to continue...')
        input()
        os.system('cls')
        print(conversation.replace('  ', '\n'))
        continue
    elif prompt == ('x'):
        print('Exiting')
        if os.path.exists("temp.mp3"):
            os.remove("temp.mp3")
        quit()

    conversation = conversation + (f'{prompt}\n')

    response = openai.Completion.create(engine="text-davinci-003", prompt=conversation, max_tokens=1000, temperature=0.7)

    conversation = conversation + (response["choices"][0]["text"]+ '\n')
    def tts(response):
        if ttsChoice == 'y':
            if os.path.exists('temp.mp3'):
                os.remove('temp.mp3')
                sleep(0.5)
            try:
                tts = gTTS(response)
            except:
                print('Error speaking, is the response empty?')
            tts.save('temp.mp3')
            playsound.playsound('temp.mp3')

    def print_response(response):
        print('\n')
        splitted = response.split()
        for word in splitted:
            print(Fore.GREEN + word, end=' ', flush=True)
            sleep(0.05)
        print('\n')

    t1 = threading.Thread(target=print_response, args=(response["choices"][0]["text"],))
    t1.start()
    if ttsChoice == 'y':
        t2 = threading.Thread(target=tts, args=(response["choices"][0]["text"],))
        t2.start()