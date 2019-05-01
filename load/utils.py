def calculate_carrier_price(shipper_price):
    """Calculates the carrier price based on the shipper price

    The carrier price is the amount of money a carrier will receive if
    they accept the load. It is the shipper price minus 5%.

    :param float shipper_price: The price defined by the Shipper.
    :return: The price presented to the Carrier.
    :rtype: float
    """
    return round(shipper_price - (shipper_price * 5.0 / 100.0), 2)