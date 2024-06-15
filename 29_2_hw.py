import logging

import requests

logging.basicConfig(level=logging.INFO)

LATEST_URL = 'https://downloads.thebiogrid.org/Download/BioGRID/Latest-Release/BIOGRID-ALL-LATEST.tab3.zip'

def load_biogrid():
    biogrid_url = LATEST_URL
    local_file_name = 'biogrid_v_latest.tab3.zip'

    logging.info('Loading biogrid file...')
    response = requests.get(
        biogrid_url,
        params={'downloadformat': 'zip'}
    )

    if response.status_code == 200:
        with open(local_file_name, 'wb') as f:
            f.write(response.content)
    else:
        logging.error('No connection')
        raise Exception()

    logging.info('Biogrid file has loaded')

if __name__ == '__main__':
    load_biogrid()
