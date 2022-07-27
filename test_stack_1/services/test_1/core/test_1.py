from test_layer_1 import test_layer_1
from test_layer_2.test_layer_2 import hola
__version__ = '0.1.0'


def lambda_handler(event: dict, context: dict) -> dict:
    """
    Main

    Parameters
    ----------
    event : dict
        - idx: Identificador de tracking
    context : dict

    Returns
    -------
    dict
        - status : str
            Estado de la consulta

    :Authors:
        -

    :Created:
        - 2022.07.26
    """
    result = test_layer_1({})
    saludo = hola('javier')
    print(saludo)
    print(result)
    return {'status': 'status'}
