from yaml import dump
from yaml import load
from yaml import FullLoader


if __name__ == '__main__':
    with open('serverless.yml') as file:
        resource_data = load(file, Loader=FullLoader)
        print(resource_data)
        resource_data['plugins'].remove('serverless-python-requirements')
        dump(resource_data, 'serverless.yml')
        print(resource_data)
