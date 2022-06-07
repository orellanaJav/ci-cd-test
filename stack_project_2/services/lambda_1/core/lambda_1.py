import json
from controllers.formatted_name import get_formatted_name
from settings.config import ANOTHER_KEY


def hello(event, lambda_context):
<<<<<<< HEAD
    print('hola')
=======
>>>>>>> f2fb6456151b6adaff39d16fda20388727c859e6
    first_name = event.get('first_name', '')
    middle_name = event.get('middle_name', '')
    last_name = event.get('last_name', '')
    full_name = get_formatted_name(first_name, middle_name, last_name)
    response = {
        'statusCode': 200,
        'body': full_name
    }

    return response
