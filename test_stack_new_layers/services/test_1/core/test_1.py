
from bifrost.connection_aws import invoker_dispatch
from settings.config import logger
from test_layer_bifrost import test_layer_bifrost


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
    invoke = test_layer_bifrost({})
    response = invoker_dispatch(function_name='test-stack-new-layers-test_2', region='sa-east-1', data={})
    logger.info('resposne es ---> ', invoke)
    return {'status': 'status'}
