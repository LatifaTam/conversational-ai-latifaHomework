from emora_stdm import DialogueFlow

transitions = {
    'state': 'start',
    '`Hello, how can I help you?`': {
        '[{haircut, <cut, hair>,<hair,long>}]':{
            '`Sure. What date and time are you looking for?`':{
                '{<{monday,mon},{10 am,1 pm,2 pm}>,<{tuesday,tue},{2 pm}>}':{
                    '`Your appointment is set. See you!`':'end'
                },
                'error':{
                    '`Sorry, that slot is not available for a haircut.`':'end'
                }
            }
        },
        '[{hair coloring, hair colouring,<{color,colour}, hair>, <{dye,dyeing}, hair>, bleach}]':{
            '`Sure. What date and time are you looking for?`':{
                '{<{wednesday,wed},{10 am,11 am,1 pm}>,<{thursday,thu},{10 am, 11 am}>}': {
                    '`Your appointment is set. See you!`': 'end'
                },
                'error': {
                    '`Sorry, that slot is not available for a hair coloring.`': 'end'
                }
            }

        },
        '[{perm,perms,curl,curls,curling,frizz,frizzes,wave,waves,curly, frizzy}]': {
            '`Sure. What date and time are you looking for?`': {
                '{<{friday,fri},{10 am,11 am,1 pm,2 pm}>,<{saturday,sat},{10 am, 2 pm}>}': {
                    '`Your appointment is set. See you!`': 'end'
                },
                'error': {
                    '`Sorry, that slot is not available for a perm.`': 'end'
                }
            }
        },
        'error': {
            '`Sorry, we do not provide that service.`': 'end'
        }
    }
}

df = DialogueFlow('start', end_state='end')
df.load_transitions(transitions)

if __name__ == '__main__':
    df.run()