from pyrobud import mt4

_zmq = mt4.DWX_ZeroMQ_Connector(_host="192.168.88.148")

_my_trade = _zmq._generate_default_order_dict()

_my_trade['_lots'] = 0.05

_my_trade['_type'] = 1

_my_trade['_comment'] = 'test selling'

_zmq._DWX_MTX_NEW_TRADE_(_order=_my_trade)
print("order sent")