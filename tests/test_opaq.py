import os
import unittest

from opaq import OPAQ_BASE_URL, Opaq, claude_code_env, estimate_cost, list_models


class TestOpaq(unittest.TestCase):
    def test_client_points_at_opaq(self):
        client = Opaq(api_key="opaq_sk_test")
        self.assertEqual(str(client.base_url).rstrip("/"), OPAQ_BASE_URL)

    def test_refuses_to_start_without_a_key(self):
        saved = os.environ.pop("OPAQ_API_KEY", None)
        try:
            with self.assertRaises(ValueError):
                Opaq()
        finally:
            if saved:
                os.environ["OPAQ_API_KEY"] = saved

    def test_estimate_cost_reads_both_formats(self):
        model = {"pricing": {"prompt_per_mtok": 3, "completion_per_mtok": 15}}
        self.assertEqual(estimate_cost(model, {"prompt_tokens": 1_000_000, "completion_tokens": 0}), 3)
        self.assertEqual(estimate_cost(model, {"input_tokens": 0, "output_tokens": 1_000_000}), 15)

    def test_claude_code_env(self):
        self.assertEqual(claude_code_env("opaq_sk_x"), {"ANTHROPIC_BASE_URL": "https://opaq.computer", "ANTHROPIC_API_KEY": "opaq_sk_x"})

    @unittest.skipIf(os.environ.get("OFFLINE") == "1", "offline")
    def test_live_catalog(self):
        models = list_models()
        self.assertGreater(len(models), 50)
        self.assertTrue(all(isinstance(m["pricing"]["prompt_per_mtok"], (int, float)) for m in models))
        self.assertTrue(all(m.get("private") for m in list_models(private_only=True)))


if __name__ == "__main__":
    unittest.main()
