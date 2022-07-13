from settings.config import logger
import numpy as np
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
        - 2022.07.13
    """
    logger.basic_loader(**event)
    a = np.arange(6)
    logger.info(a)
    return {'status': 'status'}
