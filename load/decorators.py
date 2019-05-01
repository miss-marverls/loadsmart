from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def shipper_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='app:index'):
    """
    Decorator for views that check that the user is logged in and is a shipper,
    redirects to the login page if necessary. / todo verificar pra onde vai isso

    :param function:
    :param redirect_field_name:
    :param login_url:
    :return:
    :rtype:
    """

    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_shipper,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def carrier_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='app:index'):
    """
    Decorator for views that check that the user is logged in and is a carrier,
    redirects to the login page if necessary.

    :param function:
    :param redirect_field_name:
    :param login_url:
    :return:
    :rtype:
    """

    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_carrier,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='users:login'):
    """
    Decorator for views that check that the user is logged,
    redirects to the login page if necessary.

    :param function:
    :param redirect_field_name:
    :param login_url:
    :return:
    :rtype:
    """

    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

# TODO: update params in Docstrings
