import json
import struct

def parse_mq_payload(payload):
    try:
        data = json.loads(payload)
    except Exception as e:
        print str(e)
        raise

    try:
        data['gw_timestamp'] = str(data['gw_timestamp'])
        data['payload'] = str(data['payload'])
        data['gw_serial'] = int(data['gw_serial'])
        pl = data['payload'].decode('hex')
    except Exception as e:
        print str(e)
        raise

    try:
        data['parsed'] = {}
        data['parsed']['serial'] = struct.unpack('H', pl[1:3])[0]
        data['parsed']['key']    = struct.unpack('H', pl[3:5])[0]
        data['parsed']['value']  = struct.unpack('f', pl[5:9])[0]
    except Exception as e:
        print str(e)
        raise

    return data
