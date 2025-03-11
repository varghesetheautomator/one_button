import os
import json

data_settings = None


class SalesRepDataSettings(object):
    """Simple singleton class for managing and accessing datas"""

    def __init__(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sales_rep_data.json')) as f:
            data_settings = json.load(f)
            self.name = data_settings['name']
            self.id = data_settings['id']
            self.direct_lead = data_settings['direct_lead']
            self.address = data_settings['address']
            self.contact = data_settings['contact']
            self.stage = data_settings['stage']
            self.sales_person = data_settings['sales_person']

sales_rep_data_settings = SalesRepDataSettings()
