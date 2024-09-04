import json
import unittest
from unittest.mock import patch, MagicMock
import custom_soarca
import logging
logger = logging.getLogger(__name__)
logger.setLevel = logging.DEBUG


class TestSoarcaWazuhIntegration(unittest.TestCase):
    def test_variable(self):
        var_type = "string"
        var_description = "A nice description"
        var_value = "variable 1 value"
        expected_result = {
            "type": "string",
            "description": "A nice description",
            "value": "variable 1 value",
            "constant": True,
            "external": True
        }
        result = custom_soarca.build_cacao_variable(
            var_type, var_description, var_value)
        self.assertEqual(result, expected_result)

    @patch("custom_soarca.requests.post")
    def test_main(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_requests.post.return_value = mock_response

        file = "alert.json"
        webhook = "localhost:8080"
        api_key = ""

        custom_soarca.execute(alert_file_location=file,
                              webhook=webhook, api_key=api_key)
        self.maxDiff = None
        data = '''{"__rule_id__": {"type": "integer", "description": "File added to the system.", "value": "554", "constant": true, "external": true}, "__rule_level__": {"type": "integer", "description": "rule severity level 1 - 15", "value": 5, "constant": true, "external": true}, "__times_fired__": {"type": "integer", "description": "number of times the rile fired", "value": 14, "constant": true, "external": true}, "__affected_agent_name__": {"type": "string", "description": "agent name that is affected", "value": "deployment", "constant": true, "external": true}, "__affected_agent_ip__": {"type": "ipv4-addr", "description": "agent ip that is affected", "value": "192.168.130.29", "constant": true, "external": true}, "__user__": {"type": "string", "description": "the effected user", "value": "root", "constant": true, "external": true}, "__full_log_message__": {"type": "string", "description": "the full log message from wazuh", "value": "File '/home/ansible/file16' added Mode: realtime", "constant": true, "external": true}}'''

        self.assertEqual(json.dumps(
            mock_requests.call_args[1]["data"]), data)
        self.assertEqual(str(json.dumps(
            mock_requests.call_args[1]["url"])).replace("\"", ""), webhook)

        mock_requests.assert_called()
