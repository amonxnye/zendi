# noinspection PyUnresolvedReferences
import logging
import functools
import operator

from iota import STANDARD_UNITS

from wallet.iota_ import NotEnoughBalanceException
from wallet.iota_.iota_api import IotaApi
from wallet.models import IotaAddress
from wallet.user_utils import get_user_safe

logger = logging.getLogger(__name__)


def api_resolver(func):
    @functools.wraps(func)
    def wrapper(user, **kwargs):
        api = IotaApi(seed=user.iotaseed.seed)
        return func(user=user, api=api, **kwargs)

    return wrapper


@api_resolver
def get_new_address(user, api=None):
    """
    Creates a new IOTA address, which is not attached to the tangle.
    :param user: user object containing seed
    :param api: IOTA api object (should be resolved by decorator)
    :return: new address in the IOTA network (not attached to the Tangle)
    """
    # create and store new address
    new_address = api.get_new_address()
    IotaAddress.objects.get_or_create(user=user, address=new_address)

    logger.info('Generated address %s for user %s', new_address, user)

    return new_address


# noinspection PyUnusedLocal
@api_resolver
def get_balance(user, api=None):
    return api.get_account_balance()


def send_tokens(sender, receiver, amount, msg=None):
    # get proper users
    _, sending_user = get_user_safe(email=sender)
    is_new, receiving_user = get_user_safe(email=receiver)

    # ToDo: inform user about new wallet

    # check balance
    api = IotaApi(seed=sending_user.iotaseed.seed)
    balance = api.get_account_balance()
    if balance < amount:
        raise NotEnoughBalanceException(user=str(sending_user), proposed_amount=amount, balance=balance)

    change_address = get_new_address(sending_user)
    receiving_address = get_new_address(receiving_user)

    logger.info('Sending %i IOTA from %s to %s (address: %s, new:%s)',
                amount, sending_user, receiving_user, receiving_address, is_new)

    # noinspection PyBroadException
    try:
        # send transaction
        api.transfer(receiver_address=receiving_address,
                     change_address=change_address,
                     value=amount,
                     message=msg)

        # ToDo: inform users via mail
    except:
        logger.exception('Error while transferring %i IOTA from %s to %s (address %s, new:%s)',
                         amount, sending_user, receiving_user, receiving_address, is_new)

    return


def iota_display_format(amount):
    previous_unit = 'i'
    for unit, decimal in sorted(STANDARD_UNITS.items(), key=operator.itemgetter(1)):
        if decimal >= amount / 10:
            break
        previous_unit = unit
    return amount / STANDARD_UNITS[previous_unit], previous_unit
