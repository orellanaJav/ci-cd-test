from settings.config import logger
from test_layer import test_layer

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
    layer_return = test_layer()
    logger.info('hola ---> ', layer_return)
    return {'status': 'status'}

