import os
import requests

from lib.cache import Pickled, RateLimitException


class ZipCode(Pickled):

    def __init__(self, zip_code):
        super(ZipCode, self).__init__()

        self.zip_code = zip_code.split('-')[0]
        self.metadata = self.fetch_metadata() if len(self.zip_code) == 5 else None

    def __repr__(self):
        if self.metadata:
            return self.metadata.get('formatted_address').encode('utf-8')
        else:
            return self.zip_code

    def fetch_metadata(self):
        def compute():
            response = requests.get(ZipCode.maps_resource(self.zip_code)).json()
            status = response.get('status')
            if status == 'OK':
                return response.get('results')[0]
            elif status == 'ZERO_RESULTS':
                return None
            elif status == 'OVER_QUERY_LIMIT':
                raise RateLimitException()

        pickle_fn = os.path.join(self.cwd, 'zip_codes', self.zip_code)
        return Pickled.load_or_compute(pickle_fn, compute, retry=1)

    @staticmethod
    def maps_resource(zip_code, key=None):
        resource = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s' % zip_code
        if key:
            resource += '&key=%s' % key
        return resource
