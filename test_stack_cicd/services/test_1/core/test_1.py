from settings.config import logger
from os import environ
from destacame_models.receiver import Receiver
from destacame_models.receiver_tag import ReceiverTag
from destacame_models.voluntary_payment_rule import VoluntaryPaymentRule
from destacame_models.voluntary_payment_rule_tags import VoluntaryPaymentRuleTags


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

    logger.info(environ.get('HOLA'))
    logger.info(environ.get('HOLA'))
    receivers_data = []
    try:
        query_receivers_close_to_expire = (
            VoluntaryPaymentRule.select(
                VoluntaryPaymentRule.id.alias('id_rule'),
                VoluntaryPaymentRule.expiration_date,
                ReceiverTag.id,
                Receiver.name,
            )
            .where(
                (VoluntaryPaymentRule.status == 'active') &
                (VoluntaryPaymentRule.type_rules == 'reported')
            )
            .join(
                VoluntaryPaymentRuleTags,
                on=(
                    VoluntaryPaymentRule.id == VoluntaryPaymentRuleTags.voluntarypaymentrule
                ),
            )
            .join(ReceiverTag)
            .join(Receiver)
            .dicts()
        )
        if query_receivers_close_to_expire.exists():
            receivers_data = [
                receiver for receiver in query_receivers_close_to_expire
            ]
        print(receivers_data)

    except VoluntaryPaymentRule.DoesNotExist as e:
        logger.error('error_get_rules', extra=str(e))
        receivers_data = []
    return {'status': 'status'}
