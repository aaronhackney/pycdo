from .base import CDOBaseClient
import logging

logger = logging.getLogger(__name__)


class CDOASAServices(CDOBaseClient):
    """Class for performing CDO ASA operations"""

    # TODO: Full CRUD operations where available
    # TODO: packettracer method(s)

    def get_asa_config_summary_list(self):
        return self.get_operation(f"{self.PREFIX_LIST['SERVICES']}/asa/configs")

    def get_asa_config_summary(self, device_uid):
        return self.get_operation(f"{self.PREFIX_LIST['SERVICES']}/asa/configs/{device_uid}")

    def get_asa_nats_list(self):
        return self.get_operation(f"{self.PREFIX_LIST['SERVICES']}/asa/nats")

    def get_asa_nat(self, nat_uid):
        return self.get_operation(f"{self.PREFIX_LIST['SERVICES']}/asa/nats/{nat_uid}")

    def get_asa_twice_nat_events_list(self):
        return self.get_operation(f"{self.PREFIX_LIST['SERVICES']}/asa/twicenatevents")

    def get_asa_twice_nat_events(self, twice_nat_uid):
        return self.get_operation(f"{self.PREFIX_LIST['SERVICES']}/asa/twicenatevents/{twice_nat_uid}")

    def get_asa_exports_list(self):
        return self.get_operation(f"{self.PREFIX_LIST['SERVICES']}/asa/exports")

    def get_asa_exports(self, export_uid):
        return self.get_operation(f"{self.PREFIX_LIST['SERVICES']}/asa/exports/{export_uid}")

    def get_asa_templates_list(self):
        return self.get_operation(f"{self.PREFIX_LIST['SERVICES']}/asa/templates")

    def get_asa_templates(self, template_uid):
        return self.get_operation(f"{self.PREFIX_LIST['SERVICES']}/asa/templates/{template_uid}")

    def get_asa_debug_events_list(self):
        return self.get_operation(f"{self.PREFIX_LIST['SERVICES']}/asa/debugevents")

    def get_asa_debug_events(self, events_uid):
        return self.get_operation(f"{self.PREFIX_LIST['SERVICES']}/asa/debugevents/{events_uid}")

    def get_asa_ordered_nats_list(self, params):
        return self.get_operation(f"{self.PREFIX_LIST['SERVICES']}/asa/orderednats", params=params)

    def get_asa_ordered_nats(self, ordered_nats_uid, params):
        return self.get_operation(f"{self.PREFIX_LIST['SERVICES']}/asa/orderednats/{ordered_nats_uid}", params=params)

    def get_asa_configs_exports_list(self):
        return self.get_operation(f"{self.PREFIX_LIST['SERVICES']}/asa/configs-exports")

    def get_asa_configs_exports(self, configs_exports_uid):
        return self.get_operation(f"{self.PREFIX_LIST['SERVICES']}/asa/configs-exports/{configs_exports_uid}")

    def get_asa_nat_events_list(self):
        return self.get_operation(f"{self.PREFIX_LIST['SERVICES']}/asa/natevents")

    def get_asa_nat_events(self, nat_events_uid):
        return self.get_operation(f"{self.PREFIX_LIST['SERVICES']}/asa/natevents/{nat_events_uid}")
