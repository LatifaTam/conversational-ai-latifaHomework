# ========================================================================
# Copyright 2022 Emory University
#
# Licensed under the Apache License, Version 2.0 (the `License`);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an `AS IS` BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========================================================================
__author__ = 'Latifa Tan'

from emora_stdm import DialogueFlow, Macro, Ngrams
from typing import Dict, Any, List

import openai

PATH_API_KEY = 'resources/openai_api.txt'
openai.api_key_path = PATH_API_KEY

global serviceType
global avTime
global timeChecker
serviceType = 3 # 0: haircut/ 1: coloring/ 2: perm
avTime=['Monday: 10 AM, 1 PM, 2 PM; Tuesday: 2 PM',# time[0]: haircut
      'Wednesday: 10 AM, 11 AM, 1 PM; Thursday: 10 AM, 11 AM', # time[1]: coloring
      'Friday: 10 AM, 11 AM, 1 PM, 2 PM; Saturday: 10 AM, 2 PM']  # time[2]: perm
timeChecker = 0 # 1: yes/ 0: no

class MacroService(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[str]):
        global serviceType
        model = 'gpt-3.5-turbo'
        c1 = 'Detect if the user wants to do a haircut, hair coloring, or perm from the following sentence and return only the service name lowercase in the format of  "[haircut]", "[hair coloring]", "[perm]", or "[other]":'
        c2 = ngrams.text().strip()
        content = c1 +c2
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{'role': 'user', 'content': content}]
        )
        output = response['choices'][0]['message']['content'].strip().lower()
    # [haircut], [hair coloring], [perm], [other]
        if "haircut" in output:
            serviceType = 0
        elif 'hair coloring'in output:
            serviceType = 1
        elif 'perm' in output:
            serviceType = 2
        else:
            vars['SERVICEYES'] = '1'
        return True

class MacroTime(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[str]):
        # [haircut], [hair coloring], [perm], [other]
        global serviceType
        if serviceType <=2:
            return 'Sure, here is our open time slot for this service:\n' + avTime[serviceType]+'\nWhat date and time are you looking for?'
        else:
            return 'ohno'

class MacroCheckav(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[str]):
        global serviceType
        global timeChecker
        model = 'gpt-3.5-turbo'
        c1 = 'Here is a list of available time slots: ' + avTime[serviceType]+'. Detect if the requested time from the following sentence in the list of available time slots and return only [yes] or [no]: '
        c2 = ngrams.text().strip()
        content = c1 +c2
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{'role': 'user', 'content': content}]
        )
        output = response['choices'][0]['message']['content'].strip().lower()
        if "yes" in output:
            timeChecker =1
        return True

class MacroFinalcall(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[str]):
        global timeChecker
        if timeChecker == 1:
            return "Sure! I had reserved this time slot for you."
        else:
            return "Sorry that time slot is not available."

transitions = {
    'state': 'start',
    '`Hello, how can I help you?`': { # bot
        '#SET($SERVICEYES=0) #SERVICE':{ # user response
            '#IF($SERVICEYES=1)`Sorry we do not have this service`':{ #bot
                '#UNX': {
                    '`Hope you enjoy using this bot!`': 'end'
                }
            },
            '#IF($SERVICEYES=0) #TIME':{ # bot
                '#CHECKAV':{ # user response
                    '#FINALCALL':{ #bot
                        '#UNX': {
                            '`Hope you enjoy using this bot!`': 'end'
                        },
                        'error': {
                            'score': 0.0000001,
                            '`Sorry, I didn\'t understand you.`': 'end'
                        }
                    },
                    'error': {
                        'score': 0.0000001,
                        '`Sorry, I didn\'t understand you.`': 'end'
                    }
                },
                'error': {
                    'score': 0.0000001,
                    '`Sorry, I didn\'t understand you.`': 'end'
                }
            },
            'error': {
                'score': 0.0000001,
                '`Sorry, I didn\'t understand you.`': 'end'
            }
        },
        'error': {
            'score': 0.0000001,
            '`Sorry, I didn\'t understand you.`': 'end'
        }
    }
}

macros = {
    # save user name
    'SERVICE' : MacroService(),
    'TIME' : MacroTime(),
    'CHECKAV' : MacroCheckav(),
    'FINALCALL' : MacroFinalcall()
}

df = DialogueFlow('start', end_state='end')
df.load_transitions(transitions)
df.add_macros(macros)

if __name__ == '__main__':
    df.run()