"""Tools for unittests."""


def flask_response_data(resp):
    """Flask html response without whitespaces.

    :param resp: app_fixture response
    """
    return "".join(resp.data.decode().split())
