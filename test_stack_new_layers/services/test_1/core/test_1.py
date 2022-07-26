
from bifrost.connection_aws import invoker_dispatch

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
    # response = invoker_dispatch(function_name=connection, data=payload)
    return {'status': 'status'}
