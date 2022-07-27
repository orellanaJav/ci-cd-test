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
        - 2022.07.27
    """
    result_1 = test_layer_1({})
    result_2 = hola('Lunita')
    print(result_1)
    print(result_2)
    return {'status': 'status'}
