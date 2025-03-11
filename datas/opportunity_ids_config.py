import os
import json

data_settings = None


class OpportunityID(object):
    """Simple singleton class for managing and accessing opportunity ID's"""

    def __init__(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'opportunity_ids.json')) as f:
            data_settings = json.load(f)

            self.SOLAR_SUNNOVA = data_settings["SOLAR_SUNNOVA"]
            self.RRR_SUNNOVA = data_settings["RRR_SUNNOVA"]
            self.SOLAR_CASH = data_settings["SOLAR_CASH"]
            self.ROOF_CASH = data_settings["ROOF_CASH"]
            self.RRR_CASH = data_settings["RRR_CASH"]
            self.RRR_SERVICE_FINANCE = data_settings["RRR_SERVICE_FINANCE"]
            self.ROOF_SERVICE_FINANCE = data_settings["ROOF_SERVICE_FINANCE"]
            self.SOLAR_SERVICE_FINANCE = data_settings["SOLAR_SERVICE_FINANCE"]
            self.SOLAR_SERVICE_FINANCE_RRR_SERVICE_FINANCE = data_settings[
                "SOLAR_SERVICE_FINANCE_RRR_SERVICE_FINANCE"]
            self.SOLAR_SERVICE_FINANCE_ROOF_SERVICE_FINANCE = data_settings[
                "SOLAR_SERVICE_FINANCE_ROOF_SERVICE_FINANCE"]
            self.SOLAR_CASH_RRR_SERVICE_FINANCE = data_settings[
                "SOLAR_CASH_RRR_SERVICE_FINANCE"]
            self.BATTERY_CASH = data_settings["BATTERY_CASH"]
            self.SOLAR_SUNNOVA_ROOF_CASH = data_settings["SOLAR_SUNNOVA_ROOF_CASH"]
            self.SOLAR_SUNNOVA_BATTERY_CASH = data_settings["SOLAR_SUNNOVA_BATTERY_CASH"]
            self.SOLAR_SUNNOVA_ROOF_SUNNOVA = data_settings["SOLAR_SUNNOVA_ROOF_SUNNOVA"]
            self.SOLAR_SUNNOVA_RRR_SUNNOVA = data_settings["SOLAR_SUNNOVA_RRR_SUNNOVA"]
            self.SOLAR_CASH_ROOF_CASH = data_settings["SOLAR_CASH_ROOF_CASH"]
            self.ROOF_CASH_BATTERY_CASH = data_settings["ROOF_CASH_BATTERY_CASH"]
            self.SOLAR_CASH_RRR_CASH = data_settings["SOLAR_CASH_RRR_CASH"]
            self.SOLAR_SUNNOVA_RRR_CASH = data_settings[
                "SOLAR_SUNNOVA_RRR_CASH"]
            self.SOLAR_CASH_ROOF_SUNNOVA = data_settings[
                "SOLAR_CASH_ROOF_SUNNOVA"]
            self.ROOF_SUNNOVA_BATTERY_CASH = data_settings["ROOF_SUNNOVA_BATTERY_CASH"]
            self.SOLAR_SUNNOVA_ROOF_SERVICE_FINANCE = data_settings[
                "SOLAR_SUNNOVA_ROOF_SERVICE_FINANCE"]
            self.SOLAR_CASH_ROOF_SERVICE_FINANCE = data_settings[
                "SOLAR_CASH_ROOF_SERVICE_FINANCE"]
            self.SOLAR_SERVICE_FINANCE_ROOF_SUNNOVA = data_settings[
                "SOLAR_SERVICE_FINANCE_ROOF_SUNNOVA"]
            self.ROOF_SERVICE_FINANCE_BATTERY_CASH = data_settings[
                "ROOF_SERVICE_FINANCE_BATTERY_CASH"]
            self.SOLAR_SERVICE_FINANCE_BATTERY_CASH = data_settings[
                "SOLAR_SERVICE_FINANCE_BATTERY_CASH"]
            self.SOLAR_SUNNOVA_RRR_SERVICE_FINANCE = data_settings[
                "SOLAR_SUNNOVA_RRR_SERVICE_FINANCE"]
            self.ROOF_SUNNOVA = data_settings["ROOF_SUNNOVA"]
            self.SOLAR_SUNNOVA_ROOF_CASH_BATTERY_CASH = data_settings[
                "SOLAR_SUNNOVA_ROOF_CASH_BATTERY_CASH"]
            self.SOLAR_SUNNOVA_ROOF_SUNNOVA_BATTERY_CASH = data_settings[
                "SOLAR_SUNNOVA_ROOF_SUNNOVA_BATTERY_CASH"]
            self.SOLAR_SUNNOVA_RRR_CASH_BATTERY_CASH = data_settings[
                "SOLAR_SUNNOVA_RRR_CASH_BATTERY_CASH"]
            self.SOLAR_CASH_ROOF_SUNNOVA_BATTERY_CASH = data_settings[
                "SOLAR_CASH_ROOF_SUNNOVA_BATTERY_CASH"]
            self.SOLAR_CASH_ROOF_CASH_BATTERY_CASH = data_settings[
                "SOLAR_CASH_ROOF_CASH_BATTERY_CASH"]
            self.SOLAR_CASH_RRR_CASH_BATTERY_CASH = data_settings[
                "SOLAR_CASH_RRR_CASH_BATTERY_CASH"]
            self.SOLAR_CASH_RRR_SERVICE_FINANCE_BATTERY_CASH = data_settings[
                "SOLAR_CASH_RRR_SERVICE_FINANCE_BATTERY_CASH"]
            self.SOLAR_SERVICE_FINANCE_RRR_CASH_BATTERY_CASH = data_settings[
                "SOLAR_SERVICE_FINANCE_RRR_CASH_BATTERY_CASH"]
            self.SOLAR_SERVICE_FINANCE_RRR_SERVICE_FINANCE_BATTERY_CASH = data_settings[
                "SOLAR_SERVICE_FINANCE_RRR_SERVICE_FINANCE_BATTERY_CASH"]
            self.SOLAR_SERVICE_FINANCE_RRR_SUNNOVA_BATTERY_CASH = data_settings[
                "SOLAR_SERVICE_FINANCE_RRR_SUNNOVA_BATTERY_CASH"]
            self.SOLAR_CASH_BATTERY_CASH = data_settings[
                "SOLAR_CASH_BATTERY_CASH"]
            self.SOLAR_CASH_RRR_SUNNOVA_BATTERY_CASH = data_settings[
                "SOLAR_CASH_RRR_SUNNOVA_BATTERY_CASH"]
            self.SOLAR_SERVICE_FINANCE_RRR_CASH = data_settings[
                "SOLAR_SERVICE_FINANCE_RRR_CASH"]
            self.SOLAR_SERVICE_FINANCE_ROOF_CASH = data_settings[
                "SOLAR_SERVICE_FINANCE_ROOF_CASH"]
            self.SOLAR_CASH_ROOF_SERVICE_FINANCE_BATTERY_CASH = data_settings[
                "SOLAR_CASH_ROOF_SERVICE_FINANCE_BATTERY_CASH"]
            self.SOLAR_SERVICE_FINANCE_ROOF_SERVICE_FINANCE_BATTERY_CASH = data_settings[
                "SOLAR_SERVICE_FINANCE_ROOF_SERVICE_FINANCE_BATTERY_CASH"]
            self.SOLAR_CASH_RRR_SUNNOVA = data_settings["SOLAR_CASH_RRR_SUNNOVA"]
            self.SOLAR_SERVICE_FINANCE_RRR_SUNNOVA = data_settings[
                "SOLAR_SERVICE_FINANCE_RRR_SUNNOVA"]
            self.SOLAR_SUNNOVA_ROOF_SERVICE_FINANCE_BATTERY_CASH = data_settings[
                "SOLAR_SUNNOVA_ROOF_SERVICE_FINANCE_BATTERY_CASH"]
            self.SOLAR_SERVICE_FINANCE_ROOF_SUNNOVA_BATTERY_CASH = data_settings[
                "SOLAR_SERVICE_FINANCE_ROOF_SUNNOVA_BATTERY_CASH"]
            self.SOLAR_SERVICE_FINANCE_ROOF_CASH_BATTERY_CASH = data_settings[
                "SOLAR_SERVICE_FINANCE_ROOF_CASH_BATTERY_CASH"]
            self.SOLAR_SUNNOVA_RRR_SUNNOVA_BATTERY_CASH = data_settings[
                "SOLAR_SUNNOVA_RRR_SUNNOVA_BATTERY_CASH"]
            self.SOLAR_SUNNOVA_RRR_SERVICE_FINANCE_BATTERY_CASH = data_settings[
                "SOLAR_SUNNOVA_RRR_SERVICE_FINANCE_BATTERY_CASH"]

            self.BATTERY_SUNNOVA = data_settings["BATTERY_SUNNOVA"]
            self.SOLAR_SUNNOVA_BATTERY_SUNNOVA = data_settings["SOLAR_SUNNOVA_BATTERY_SUNNOVA"]


opportunity_id = OpportunityID()
