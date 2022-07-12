from os import environ
from bifrost.logger import Logger


# ==============================================================================
# SISTEMA MULTITARGET
# ==============================================================================
MULTI_REGION = {
    'LOCALHOST': 'sa-east-1',
    'PANDORA': 'sa-east-1',
    'ARES': environ.get('AWS_REGION'),
    'PRODUCTION': environ.get('AWS_REGION')
}
# ==============================================================================

# ==============================================================================
# CONFIGURACIÓN STATICA - LOGGER
# ==============================================================================
NAME_IDX = 'nombre_campo_idx'
logger = Logger(NAME_IDX)
# ==============================================================================