from test_layer_02.test import test

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
        - 2022.08.04
    """
    result = test()
    print('value', result)
    print('value', result)
    print('value', result)
    return {'status': 'status'}
