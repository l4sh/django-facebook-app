import json, base64, hmac, hashlib, time
from social_core.utils import parse_qs, constant_time_compare, handle_http_errors


def load_signed_request(self, signed_request):
    """social_core method for parsing a signed request"""
    # NOTE: this method is implemented in the current social_core master
    # TODO: Review and update social_core when this is available on pypi
    def base64_url_decode(data):
        data = data.encode('ascii')
        data += '='.encode('ascii') * (4 - (len(data) % 4))
        return base64.urlsafe_b64decode(data)
    key, secret = self.get_key_and_secret()
    try:
        sig, payload = signed_request.split('.', 1)
    except ValueError:
        pass  # ignore if can't split on dot
    else:
        sig = base64_url_decode(sig)
        payload_json_bytes = base64_url_decode(payload)
        data = json.loads(payload_json_bytes.decode('utf-8', 'replace'))
        expected_sig = hmac.new(secret.encode('ascii'),
                                msg=payload.encode('ascii'),
                                digestmod=hashlib.sha256).digest()
        # allow the signed_request to function for upto 1 day
        if constant_time_compare(sig, expected_sig) and \
           data['issued_at'] > (time.time() - 86400):
            return data