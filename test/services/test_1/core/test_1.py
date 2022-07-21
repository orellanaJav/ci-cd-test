from settings.config import logger

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
        - 2022.07.21
    """
    logger.basic_loader(**event)
    logger.basic_loader(**event)
    logger.basic_loader(**event)
    logger.basic_loader(**event)
    logger.basic_loader(**event)
    logger.basic_loader(**event)
    logger.basic_loader(**event)
    logger.basic_loader(**event)
    logger.basic_loader(**event)
    logger.basic_loader(**event)
    logger.basic_loader(**event)
    logger.basic_loader(**event)
    return {'status': 'status'}
