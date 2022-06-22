from yaml import FullLoader
from yaml import load


if __name__ == '__main__':
    with open('serverless.yml') as file:
        resource_data = load(file, Loader=FullLoader)
        print(resource_data)
