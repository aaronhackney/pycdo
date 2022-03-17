from pycdo import CDOClient
from pycdo.model.asa.access_rule import AccessRule


class TestASAPolicies:
    """Test ASA Policy Manipulation"""

    def test_get_access_groups(self, cdo_client: CDOClient):
        asa = cdo_client.get_asa("TatianeASA")
        workingset = cdo_client.get_workingset(asa.target_device.uid)
        access_policies = cdo_client.get_asa_access_groups(workingset.uid)
        assert access_policies

    def test_get_access_policy(self, cdo_client: CDOClient):
        asa = cdo_client.get_asa("TatianeASA")
        workingset = cdo_client.get_workingset(asa.target_device.uid)
        access_groups = cdo_client.get_asa_access_groups(workingset.uid)
        access_list = cdo_client.get_asa_access_policy(access_groups[0].uid)
        assert access_list

    def test_update_policy(self, cdo_client: CDOClient):
        asa = cdo_client.get_asa("TatianeASA")
        workingset = cdo_client.get_workingset(asa.target_device.uid)
        access_groups = cdo_client.get_asa_access_groups(workingset.uid)
        access_list = cdo_client.get_asa_access_policy(access_groups[0].uid)
        assert access_list.access_rules[0].protocol.name == "ip"
        access_list.access_rules[0].protocol.name = "tcp"
        modified_acl = cdo_client.update_access_policy(access_groups[0].uid, access_list.access_rules)
        assert modified_acl

    def test_add_access_policy(self, cdo_client: CDOClient):
        """Create a new ACE and add it to the end of the ACL/Access Group"""
        asa = cdo_client.get_asa("TatianeASA")
        workingset = cdo_client.get_workingset(asa.target_device.uid)
        access_groups = cdo_client.get_asa_access_groups(workingset.uid)
        access_list = cdo_client.get_asa_access_policy(access_groups[0].uid)
        acl_count = len(access_list.access_rules)  # Num of rules before our addition

        # Create our new rule to add to the end of the ACL list
        new_ace = AccessRule()
        new_ace.rule_action = {"name": "permit"}
        new_ace.protocol = {"name": "tcp"}
        new_ace.source_address = {"name": "192.168.2.0/24"}
        new_ace.source_port = {"name": "any"}
        new_ace.destination_address = {"name": "any4"}
        new_ace.destination_port = {"name": "any"}
        new_ace.enabled = True
        new_ace.line_num = access_list.access_control_entry_counts["TOTAL_ACCESS_CONTROL_ENTRIES"] + 1

        access_list.access_rules.append(new_ace)  # add our new rule to the list of rules
        modified_acl = cdo_client.update_access_policy(access_groups[0].uid, access_list.access_rules)  # commit rule
        assert len(modified_acl.access_rules) == acl_count + 1  # Verify the rule was added
