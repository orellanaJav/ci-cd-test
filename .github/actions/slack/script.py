import json
import sys
import requests
if __name__ == '__main__':
    print('-----> ', sys.argv[-1])
    print('-----> ', sys.argv[-2])
    url = str(sys.argv[-2])
    message = str(sys.argv[-1])
    title = 'Test Título'
    slack_data = {
        'username': 'NotificationBot',
        'icon_emoji': ':satellite:',
        'attachments': [
            {
                'color': '#9733EE',
                'fields': [
                    {
                        'title': title,
                        'value': message,
                        'short': 'false',
                    }
                ]
            }
        ]
    }
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': 'application/json', 'Content-Length': byte_length}
    response = requests.post(url, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)