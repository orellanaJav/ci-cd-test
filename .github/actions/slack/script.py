import json
import sys
import requests
if __name__ == '__main__':
    slack_message_data = sys.argv[-1]
    slack_message_data = slack_message_data.replace('\'', '"')
    slack_message_data = json.loads(slack_message_data)
    url = 'https://hooks.slack.com/services/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'
    message = slack_message_data.get('message', 'mensaje por defecto')
    title = slack_message_data.get('title', 'titulo por defecto')
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