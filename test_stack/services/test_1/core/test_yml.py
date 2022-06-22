from yaml import dump
from yaml import load
from yaml import FullLoader


if __name__ == '__main__':
    with open('serverless.yml') as file:
        resource_data = load(file, Loader=FullLoader)
        file.close()
    print(resource_data)
    with open('serverless.yml', 'w') as file:
        resource_data['plugins'].remove('serverless-python-requirements')
        serverless = dump(resource_data, file)        
        file.close()
    print(resource_data)
