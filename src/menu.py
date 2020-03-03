from PyInquirer import style_from_dict, Token
from  .tools.validators import *

style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})

questions = [
    {
        'type': 'confirm',
        'name': 'toBeDelivered',
        'message': 'Is this for delivery?',
        'default': False
    },
    {
        'type': 'input',
        'name': 'phone',
        'message': 'What\'s your phone number?',
        'validate': PhoneNumberValidator
    },
    {
        'type': 'list',
        'name': 'size',
        'message': 'What size do you need?',
        'choices': ['Large', 'Medium', 'Small'],
        'filter': lambda val: val.lower()
    },
    {
        'type': 'input',
        'name': 'quantity',
        'message': 'How many do you need?',
        'validate': NumberValidator,
        'filter': lambda val: int(val)
    },
    {
        'type': 'expand',
        'name': 'toppings',
        'message': 'What about the toppings?',
        'choices': [
            {
                'key': 'p',
                'name': 'Pepperoni and cheese',
                'value': 'PepperoniCheese'
            },
            {
                'key': 'a',
                'name': 'All dressed',
                'value': 'alldressed'
            },
            {
                'key': 'w',
                'name': 'Hawaiian',
                'value': 'hawaiian'
            }
        ]
    },
    {
        'type': 'rawlist',
        'name': 'beverage',
        'message': 'You also get a free 2L beverage',
        'choices': ['Pepsi', '7up', 'Coke']
    },
    {
        'type': 'input',
        'name': 'comments',
        'message': 'Any comments on your purchase experience?',
        'default': 'Nope, all good!'
    },
    {
        'type': 'list',
        'name': 'prize',
        'message': 'For leaving a comment, you get a freebie',
        'choices': ['cake', 'fries'],
        'when': lambda answers: answers['comments'] != 'Nope, all good!'
    }
]

model_name_q = [ 
    {
        'type': 'input',
        'name': 'model_name',
        'message': 'Define a model name',
        'default' : 'myb',
        'validate': DummyValidator
    }
]

in_path_q = [ 
    {
        'type': 'input',
        'name': 'in_path',
        'message': 'What\'s the model root folder?',
        "default" : "src",
        'validate': ModelPathValidator
    }
]

out_path_q = [ 
    {
        'type': 'input',
        'name': 'out_path',
        'message': 'What\'s the deployement target folder?',
        "default" : "..",
        'validate': DeployPathValidator
    }
]

tag_q = [ 
    {
        'type': 'input',
        'name': 'tag',
        'message': 'Assign tag for this image (dev, qa, prod, ..)',
        "default" : "dev",
        'validate': TagValidator
    }
]

pay_path_q = [ 
    {
        'type': 'input',
        'name': 'payload_path',
        'message': 'Path to payload for testing inference',
        "default" : f"{os.getcwd()}",
        'validate': DeployPathValidator
    }
]

# MENU
main_menu = [
    {   
        'type': 'list',
        'name': 'usage',
        'message': 'What do you need to do?',
        'choices': ['Build', 'Docker Manager', 'Test', 'Deploy', 'Mantain', 'Exit'],
        'filter': lambda val: val.lower()
    }
]

test_menu = [ 
    {   
        'type': 'list',
        'name': 'test',
        'message': 'What do you need to test?',
        'choices': ['Train', 'Serve', 'Inference', '<- back'],
        'filter': lambda val: val.lower()
    }
]

dm_menu = [ 
    {   
        'type': 'list',
        'name': 'dm',
        'message': 'Docker Manager Menu',
        'choices': ['Launch image', 'Clear all images', 'Prune system', 'Stop Containers', '<- back'],
        'filter': lambda val: val.lower()
    }
]

deploy_menu = [ 
    {   
        'type': 'list',
        'name': 'deploy_usage',
        'message': 'Docker Manager Menu',
        'choices': ['Push to ECR', 'Training Job', 'Endpoint Deployement', '<- back'],
        'filter': lambda val: val.lower()
    }
]