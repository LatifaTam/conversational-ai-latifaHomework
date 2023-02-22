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

global MOVIE
# save the user name from input
class MacroUserName(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[str]):
        r = re.compile(r"(you could call me |you can call me |just call me |call me |my name is |i am )?(mr. |mrs. |ms. |dr. )?([a-z]+)(.*)")
        m = r.search(ngrams.text())
        if m is None:
            return False
        if m.group(4):
            userName = m.group(4)
        else:
            userName = m.group(3)
        vars['NAME'] = userName
        return True

transitions = {
    'state': 'start',
    # ask and save name
    '`Hello here is the oscar nomination movies LLC (Limited Liability Chatbot), what should I call you?`':{
        # if the wired user just dont wanna talk and say no/ nope/ dont want to: goodbye
        '[{no, nope, do not want}]':{
            '`Ok. Goodbye!`': 'end'
        },
        # if not no, save name
        '#USERNAME':{
            # ask latest movie
            '`Nice to meet you,` $NAME `. What was the latest movie you watched? `':{
                # Recognized movie type1: action
                '[$MOVIE=#ONT(action)]':{
                    '`I love all the chasing, beautiful heroines, big explosions, impossible wins in action movies! \n   Take a guess on what `$MOVIE` get nominated on!`': {
                        '[$NOMI=#ONT($MOVIE)]': {
                            '`Yea` $NOMI`! Isn\'t that amazing? So I guess you love action movies like` $MOVIE `?`':{
                                'state': 'genre',
                                '[{no, nope, nay, do not}]': {
                                    '`Interesting! What is your favorite genre?`':{
                                        '#UNX': {
                                            '`That\'s a good choice. Thanks for sharing that,`$NAME`!`': 'end'
                                        },
                                        'error': {
                                            '`Sorry, I didn\'t understand you.`': 'end'
                                        }
                                    }
                                },
                                #'[{yes, yea, yep, amazing, awesome, great, {[!-not, good]}, {[not, bad]}}]': {
                                '[{yes, yea, yep, amazing, awesome, great, good}]':{
                                    '`Interesting! Why do you like it?`':{
                                        '#UNX': {
                                            '`Make sense...! Thanks for sharing that,`$NAME`!`': 'end'
                                        },
                                        'error': {
                                            '`Sorry, I didn\'t understand you.`': 'end'
                                        }
                                    }
                                },
                                '#UNX': {
                                    '`Interesting...!Thanks for sharing that,`$NAME`!`': 'end'
                                },
                                'error': {
                                    '`Sorry, I didn\'t understand you.`': 'end'
                                }
                            }
                        },
                        'error': {
                            '`Sorry, I didn\'t understand you.`': 'end'
                        },
                        '#UNX': {
                            '`DING!! Wrong answer. Seems like you are not a real fan for this movie nor the Oscars:( \n DO you you love action movies like` $MOVIE `though?`': 'genre'
                        },
                    }
                },
                # Recognized movie type2: horror
                '[$MOVIE=#ONT(horror)]': {
                    '`I love all the jump scare and haunting in horror movies! \n   Take a guess on what `$MOVIE` get nominated on!`': {
                        '[$NOMI=#ONT($MOVIE)]': {
                            '`Yea` $NOMI`! Isn\'t that amazing? So I guess you love horror movies like` $MOVIE `?`': {
                                '[{no, nope, nay, do not}]': {
                                    '`Interesting! What is your favorite genre?`': {
                                        '#UNX': {
                                            '`That\'s a good choice. Thanks for sharing that,`$NAME`!`': 'end'
                                        },
                                        'error': {
                                            '`Sorry, I didn\'t understand you.`': 'end'
                                        }
                                    }
                                },
                                # '[{yes, yea, yep, amazing, awesome, great, {[!-not, good]}, {[not, bad]}}]': {
                                '[{yes, yea, yep, amazing, awesome, great, good}]': {
                                    '`Interesting! Why do you like it?`': {
                                        '#UNX': {
                                            '`Make sense...! Thanks for sharing that,`$NAME`!`': 'end'
                                        },
                                        'error': {
                                            '`Sorry, I didn\'t understand you.`': 'end'
                                        }
                                    }
                                },
                                '#UNX': {
                                    '`Interesting...!Thanks for sharing that,`$NAME`!`': 'end'
                                },
                                'error': {
                                    '`Sorry, I didn\'t understand you.`': 'end'
                                }
                            }
                        },
                        'error': {
                            '`Sorry, I didn\'t understand you.`': 'end'
                        },
                        '#UNX': {
                            '`DING!! Wrong answer. Seems like you are not a real fan for this movie nor the Oscars:(\n DO you you love horror movies like` $MOVIE `though?`': 'genre'
                        },
                    }
                },
                # Recognized movie type3: science fiction
                '[$MOVIE=#ONT(science fiction)]': {
                    '`I love exploring the world of aliens or spaceships or the post-apocalyptic future in science fiction movies! \n   Take a guess on what `$MOVIE` get nominated on!`': {
                        '[$NOMI=#ONT($MOVIE)]': {
                            '`Yea` $NOMI`! Isn\'t that amazing? So I guess you love science fiction movies like` $MOVIE `?`': {
                                '[{no, nope, nay, do not}]': {
                                    '`Interesting! What is your favorite genre?`': {
                                        '#UNX': {
                                            '`That\'s a good choice. Thanks for sharing that,`$NAME`!`': 'end'
                                        },
                                        'error': {
                                            '`Sorry, I didn\'t understand you.`': 'end'
                                        }
                                    }
                                },
                                # '[{yes, yea, yep, amazing, awesome, great, {[!-not, good]}, {[not, bad]}}]': {
                                '[{yes, yea, yep, amazing, awesome, great, good}]': {
                                    '`Interesting! Why do you like it?`': {
                                        '#UNX': {
                                            '`Make sense...! Thanks for sharing that,`$NAME`!`': 'end'
                                        },
                                        'error': {
                                            '`Sorry, I didn\'t understand you.`': 'end'
                                        }
                                    }
                                },
                                '#UNX': {
                                    '`Interesting...!Thanks for sharing that,`$NAME`!`': 'end'
                                },
                                'error': {
                                    '`Sorry, I didn\'t understand you.`': 'end'
                                }
                            }
                        },
                        'error': {
                            '`Sorry, I didn\'t understand you.`': 'end'
                        },
                        '#UNX': {
                            '`DING!! Wrong answer. Seems like you are not a real fan for this movie nor the Oscars:(\n DO you you love science fiction movies like` $MOVIE `though?`': 'genre'
                        },
                    }
                },
                # Recognized movie type4: comedy
                '[$MOVIE=#ONT(comedy)]': {
                    '`I love all the humor and laugh in comedy movies! \n   Take a guess on what `$MOVIE` get nominated on!`': {
                        '[$NOMI=#ONT($MOVIE)]': {
                            '`Yea` $NOMI`! Isn\'t that amazing? So I guess you love comedy movies like` $MOVIE `?`': {
                                '[{no, nope, nay, do not}]': {
                                    '`Interesting! What is your favorite genre?`': {
                                        '#UNX': {
                                            '`That\'s a good choice. Thanks for sharing that,`$NAME`!`': 'end'
                                        },
                                        'error': {
                                            '`Sorry, I didn\'t understand you.`': 'end'
                                        }
                                    }
                                },
                                # '[{yes, yea, yep, amazing, awesome, great, {[!-not, good]}, {[not, bad]}}]': {
                                '[{yes, yea, yep, amazing, awesome, great, good}]': {
                                    '`Interesting! Why do you like it?`': {
                                        '#UNX': {
                                            '`Make sense...! Thanks for sharing that,`$NAME`!`': 'end'
                                        },
                                        'error': {
                                            '`Sorry, I didn\'t understand you.`': 'end'
                                        }
                                    }
                                },
                                '#UNX': {
                                    '`Interesting...!Thanks for sharing that,`$NAME`!`': 'end'
                                },
                                'error': {
                                    '`Sorry, I didn\'t understand you.`': 'end'
                                }
                            }
                        },
                        'error': {
                            '`Sorry, I didn\'t understand you.`': 'end'
                        },
                        '#UNX': {
                            '`DING!! Wrong answer. Seems like you are not a real fan for this movie nor the Oscars:(\n DO you you love comedy movies like` $MOVIE `though?`': 'genre'
                        },
                    }
                },
                # Recognized movie type5: animation
                '[$MOVIE=#ONT(animation)]': {
                    '`I love all visual effects and music in animation movies! \n   Take a guess on what `$MOVIE` get nominated on!`': {
                        '[$NOMI=#ONT($MOVIE)]': {
                            '`Yea` $NOMI`! Isn\'t that amazing? So I guess you love animation movies like` $MOVIE `?`': {
                                '[{no, nope, nay, do not}]': {
                                    '`Interesting! What is your favorite genre?`': {
                                        '#UNX': {
                                            '`That\'s a good choice. Thanks for sharing that,`$NAME`!`': 'end'
                                        },
                                        'error': {
                                            '`Sorry, I didn\'t understand you.`': 'end'
                                        }
                                    }
                                },
                                # '[{yes, yea, yep, amazing, awesome, great, {[!-not, good]}, {[not, bad]}}]': {
                                '[{yes, yea, yep, amazing, awesome, great, good}]': {
                                    '`Interesting! Why do you like it?`': {
                                        '#UNX': {
                                            '`Make sense...! Thanks for sharing that,`$NAME`!`': 'end'
                                        },
                                        'error': {
                                            '`Sorry, I didn\'t understand you.`': 'end'
                                        }
                                    }
                                },
                                '#UNX': {
                                    '`Interesting...!Thanks for sharing that,`$NAME`!`': 'end'
                                },
                                'error': {
                                    '`Sorry, I didn\'t understand you.`': 'end'
                                }
                            }
                        },
                        'error': {
                            '`Sorry, I didn\'t understand you.`': 'end'
                        },
                        '#UNX': {
                            '`DING!! Wrong answer. Seems like you are not a real fan for this movie nor the Oscars:(\n DO you you love animation movies like` $MOVIE `though?`': 'genre'
                        },
                    }
                },
                # when the movie not in our ontology
                '#UNX': {
                    '`Ah... I guess this is not an Oscars nominated movie in my expertise. Do you like it?`':{
                        '[{yes, yea, yep}]': {
                            '`I will watch it this weekend. Thanks for sharing!`' : 'end'
                        },
                        'error':{
                            '`Hmmmm. . .Good to know. Thanks for sharing anyway!`' : 'end'
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
    'USERNAME' : MacroUserName()
}

df = DialogueFlow('start', end_state='end')
df.load_transitions(transitions)
df.knowledge_base().load_json_file('resources/ontology_quiz3.json')
df.add_macros(macros)

if __name__ == '__main__':
    df.run()