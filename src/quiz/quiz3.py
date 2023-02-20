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

from emora_stdm import DialogueFlow
import re
from emora_stdm import Macro, Ngrams
from typing import Dict, Any, List

# save the user name from input
class MacroUserName(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[str]):
        r = re.compile(r"(call me |my name is |i am )?([a-z]+)(.*)")
        m = r.search(ngrams.text())
        if m is None:
            return False
        userName = m.group(2)
        vars['NAME'] = userName

        return True

# save favorite character from input
class MacroFavChar(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[str]):
        rchar = re.compile(r"(i love |he is | she is |it is |they are |it was )?(the )?([a-z]+)(.*)")
        mchar = rchar.search(ngrams.text())
        if mchar is None:
            return False
        charName = mchar.group(3)
        vars['character'] = charName

        return True


transitions = {
    'state': 'start',
    # ask and save name
    '`Hello, what should I call you?`':{
        # if say no/ nope/ dont want to: goodbye
        '[{no, nope, do not want}]':{
            '`Ok. Goodbye!`': 'end'
        },
        # if not no, save name
        '#USERNAME':{
            # ask latest movie
            '`Nice to meet you,` $NAME `. What was the latest movie you watched? `':{
                # Recognized movie type:
                '[$MOVIE=#ONT(family)]':{
                    '`Family movie is a good choice! Who is your favorite character?`': {
                        '#FAVCHAR': {
                            '`Yea the ` $character` is impressing. So I guess you love family movies like` $MOVIE `?`':{
                                '[{no, nope,not}]': {
                                    '`Interesting! What is your favorite genre?`':{
                                        '#UNX': {
                                            '`Thanks for sharing.`': 'end'
                                        },
                                        'error': {
                                            '`Sorry, I didn\'t understand you.`': 'end'
                                        }
                                    }
                                },
                                '[{yes, yea, definitely}]': {
                                    '`Interesting! Why do you like it?`':{
                                        '#UNX': {
                                            '`Thanks for sharing.`': 'end'
                                        },
                                        'error': {
                                            '`Sorry, I didn\'t understand you.`': 'end'
                                        }
                                    }
                                },
                                '#UNX': {
                                    '`Thanks for sharing.`': 'end'
                                },
                                'error': {
                                    '`Sorry, I didn\'t understand you.`': 'end'
                                }
                            }
                        },
                        'error': {
                            '`Sorry, I didn\'t understand you.`': 'end'
                        }
                    }
                },
                # Recognized movie type:
                '[$MOVIE=#ONT(horror)]':{
                    '`I love horror movies! Who is your favorite character?`': {
                        '#FAVCHAR': {
                            '`Yea the ` $character` is impressing. So I guess you love horror movies like` $MOVIE `?`':{
                                '[{no, nope,not}]': {
                                    '`Interesting! What is your favorite genre?`':{
                                        '#UNX': {
                                            '`Thanks for sharing.`': 'end'
                                        },
                                        'error': {
                                            '`Sorry, I didn\'t understand you.`': 'end'
                                        }
                                    }
                                },
                                '[{yes, yea, definitely}]': {
                                    '`Interesting! Why do you like it?`':{
                                        '#UNX': {
                                            '`Thanks for sharing.`': 'end'
                                        },
                                        'error': {
                                            '`Sorry, I didn\'t understand you.`': 'end'
                                        }
                                    }
                                },
                                '#UNX': {
                                    '`Thanks for sharing.`': 'end'
                                },
                                'error': {
                                    '`Sorry, I didn\'t understand you.`': 'end'
                                }
                            }
                        },
                        'error': {
                            '`Sorry, I didn\'t understand you.`': 'end'
                        }
                    }
                },
                '#UNX': {
                    '`Ah. Do you like it?`':{
                        '[{yes, yea, definitely}]': {
                            '`I will watch it this weekend. Thanks for sharing!`' : 'end'
                        },
                        'error':{
                            '`Good to know. Thanks for sharing!`' : 'end'
                        }
                    }
                },
                'error': {
                    '`Sorry, I didn\'t understand you.`': 'end'
                }
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

macros = {
    # save user name
    'USERNAME' : MacroUserName(),
    'FAVCHAR' : MacroFavChar()
}

df = DialogueFlow('start', end_state='end')
df.load_transitions(transitions)
df.knowledge_base().load_json_file('resources/ontology_quiz3.json')
df.add_macros(macros)

if __name__ == '__main__':
    df.run()