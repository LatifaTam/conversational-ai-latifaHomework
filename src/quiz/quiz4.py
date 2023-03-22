# ========================================================================
# Copyright 2023 Emory University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========================================================================

__author__ = 'Latifa Tan'
# could add on more staff with global states but doesnt require to
import json
import pickle
import time
from typing import Dict, Any, List
import requests
from emora_stdm import DialogueFlow, Macro, Ngrams
# for load and save
import os.path
import re # regular expression for user name

# return corresponding greetings and ask for name in various way
class MacroGreet(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        # to check number of time visiting and offer various greeting
        vn = 'VISITS'
        if vn not in vars:
            vars[vn] = 1
            askName = 'What is your name?'
        else:
            count = vars[vn] + 1
            vars[vn] = count
            n = count%4
            match n:
                case 0:
                    askName = 'Please tell me your name.'
                case 1:
                    askName = 'May I have your name, please?'
                case 2:
                    askName = 'What should I call you?'
                case 3:
                    askName = 'What is your name?'
        # to assign current time with proper greeting
        current_time = str(time.strftime('%H:%M'))
        iTime=current_time.find(":")
        checkerTime = int(current_time[0:iTime])
        if checkerTime < 12:
            curTime = "Good morning."
        elif 12 <= checkerTime < 18:
            curTime = "Good afternoon."
        else:
            curTime = "Good evening."
        # to assign current weather to the greeting
        url = 'https://api.weather.gov/gridpoints/FFC/52,88/forecast'
        r = requests.get(url)
        d = json.loads(r.text)
        periods = d['properties']['periods']
        today = periods[0]
        index = today['detailedForecast'].find(".")
        curWeather = 'he weather today is '+ today['detailedForecast'][0:index+1]
        # combine everything
        respCom = curTime + 'T'+curWeather.lower() + askName
        return respCom

# save the user name for later check
class MacroUserName(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[str]):
        r = re.compile(r"(you could call me |you can call me |just call me |call me |my name is |i am |it is )?(mr. |mrs. |ms. |dr. )?([a-z]+)(.*)")
        m = r.search(ngrams.text())
        if m is None:
            return False
        if m.group(4):
            userName = m.group(4)
        else:
            userName = m.group(3)
        vars['CURNAME'] = userName
        return True

# return recommendation question based on users' status
class MacroRecomQues(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[str]):
        # check if preRec is empty
        name = vars['CURNAME']
        if str(name) in vars.keys():
            # if the name had save before
            previous = vars[name][1]
            if vars[name][0][0] != 0 or vars[name][0][1] != 0:
                return "Welcome back! Did you get to enjoy " + previous +"?"
            else:
                return "Welcome back! Do you want some recommendations on movies or songs this time?"
        else:
            # creat a dictionary, key = username, value = recommendations relevant info
            recDone = [0,0]# index for available recommendation for movie,song
            preRec = "default"# update everytime offer recommendation
            # recDone: already recommend/ curRecType: movie or song
            vars[name] = [recDone, preRec]
            return "Welcome! What recommendation are you looking for, song or movie?"

# return recommendation on song/ movie based on users' request
class MacroRecomAns(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[str]):
        data = json.load(open('resources/ontology_quiz4.json'))
        curUser = vars['CURNAME']
        # recommend a song
        if vars['CURTYPE'] in ["song","songs","music","musics","listen"]:
            potentialRecS = data["ontology"]["song"]
            potentialIndex = vars[curUser][0][1]
            rec = potentialRecS[potentialIndex]
            recT = "How about the song " + str(rec) + "? Have you heard it before?"
            vars[curUser][0][1] = potentialIndex+1
            vars[curUser][1] = rec
        # recommend a movie
        else:
            potentialRecM = data["ontology"]["movie"]
            potentialIndex = vars[curUser][0][0]
            rec = potentialRecM[potentialIndex]
            recT = "How about the movie "+ str(rec) + "? Have you watched it before?"
            vars[curUser][0][0] = potentialIndex +1
            vars[curUser][1] = rec
        return recT

#return more information about the recommendation
class MacroSpecial(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[str]):
        data = json.load(open('resources/ontology_quiz4.json'))
        curUser = vars['CURNAME']
        previous = vars[curUser][1]
        if vars['CURTYPE'] in ["song","songs","music","musics","listen"]:
            artist = data["ontology"][previous][0]
            return "This song is by one of my favorite artist " + str(artist) + "!"
        else:
            nomination = data["ontology"][previous]
            text=nomination[0]
            if len(nomination)>1:
                text= "s on " + text
                for i in nomination:
                    text = text + " and "+i
            else: text =" on " + text
            return "This movie got Oscars nomination"+text+"!"

def mainConversation() -> DialogueFlow:
    transitions = {
        'state': 'start',
        '`Hello!` #GREET': { # bot
            # if the wired user just dont wanna talk and say no/ nope/ dont want to: goodbye
            '[{no, nope, do not want,bye}]': { # user response
                '`Ok. Goodbye!`': 'end'
            },
            # if not no, save name
            # STILL WORKING HERE
            '#USERNAME': { #user response
                # see if preRec: previous recommendation is empty and ask questions accordingly
                '#RECOMQUES': { #bot
                    'state': 'recomReact',
                    '[$CURTYPE=#ONT(option)]':{ # response react
                        '#RECOMANS':{
                            'state': 'recomQuest',
                            '[{already, saw, seen,watched}]':{
                                '`Then` #RECOMANS': 'recomQuest'
                            },
                            '[{why, [what, {special, interesting, cool}]}]': {
                                '#SPECIAL': {
                                    '#UNX': {
                                        '`Hope you could enjoy this recommendation!`': 'end'
                                    },
                                    'error': {
                                        '`Sorry, I didn\'t understand you.`': 'end'
                                    }
                                }
                            },
                            '[{not yet, no, have not}]':{
                                '`Hope you got time enjoy it soon!`':'end'
                            },
                            'error': {
                                '`Sorry, I didn\'t understand you.`': 'end'
                            }
                        },
                        'error': {
                            '`Sorry, I didn\'t understand you.`': 'end'
                        }
                    },
                    # not enjoy the previous recommendation from last visit and need new recommend
                    '[{no, nope, nay, did not}]': {
                        '`Hmmmm... Let me recommend something else for you then! Movie or song?`':'recomReact'
                    },
                    '[{yes,already}]':{ # enjoy the previous recommendation and need new recommend
                        '`Woooo glad to know, then do you want some other recommendations in movies or songs?`':'recomReact'
                    },
                    'error': {
                        '`Sorry, I didn\'t understand you.`': 'end'
                    }
                },
                'error': {
                    '`Sorry, I didn\'t understand you.`': 'end'
               }
            },
            'error': {
                '`Sorry, I didn\'t understand you.`': 'end'
            }
        }
    }

    macros = {
        'GREET': MacroGreet(),
        'USERNAME': MacroUserName(),
        'RECOMQUES': MacroRecomQues(),
        'RECOMANS': MacroRecomAns(),
        'SPECIAL': MacroSpecial()
    }

    df = DialogueFlow('start', end_state='end')
    df.load_transitions(transitions)
    df.knowledge_base().load_json_file('resources/ontology_quiz4.json')
    df.add_macros(macros)
    return df


def save(df: DialogueFlow, varfile: str):
    df.run()
    d = {k: v for k, v in df.vars().items() if not k.startswith('_')}
    pickle.dump(d, open(varfile, 'wb'))

def load(df: DialogueFlow, varfile: str):
    d = pickle.load(open(varfile, 'rb'))
    df.vars().update(d)
    save(df, varfile)


if __name__ == '__main__':
    # to chcek if we already use the system and have some saved info from the past
    if os.path.isfile('resources/visits.pkl'):
        load(mainConversation(), 'resources/visits.pkl')
    else:
        # create the file
        save(mainConversation(), 'resources/visits.pkl')