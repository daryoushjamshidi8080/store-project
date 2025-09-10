from kavenegar import *


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI(
            '4B665846706266617741574D6643746C3078556D675473636B436C6667776B425266764E765A66365532413D')
        params = {
            'sender': '',  # optional
            'receptor': phone_number,  # multiple mobile number, split by comma
            'message': f'Your activation code is : {code} from daryoush app',
        }
        response = api.sms_send(params)
        print('response  otp code :', response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
