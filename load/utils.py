def calculate_carrier_price(shipper_price):
    return round(shipper_price - (shipper_price * 5.0 / 100.0), 2)