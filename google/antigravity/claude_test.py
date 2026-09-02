# Copyright 2026 Google LLC & Gia Bao Huynh (Jun)
# Licensed under the Apache License, Version 2.0

"""Unit tests for Claude Cowork Bridge."""

import unittest
from google.antigravity.claude import ClaudeCoworkBridge


class TestClaudeCoworkBridge(unittest.TestCase):

    def setUp(self):
        self.bridge = ClaudeCoworkBridge()

    def test_register_and_list_tools(self):
        @self.bridge.register_tool(
            name="calculate_sum",
            description="Add two numbers together",
            input_schema={
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            },
            read_only=True
        )
        def add(a: float, b: float) -> float:
            return a + b

        tools = self.bridge.list_tools()
        self.assertEqual(len(tools), 1)
        self.assertEqual(tools[0]["name"], "calculate_sum")
        self.assertTrue(tools[0]["annotations"]["readOnlyHint"])

    def test_execute_tool(self):
        @self.bridge.register_tool(
            name="multiply",
            description="Multiply two numbers"
        )
        def multiply(x: int, y: int) -> int:
            return x * y

        res = self.bridge.execute_tool("multiply", {"x": 6, "y": 7})
        self.assertFalse(res["isError"])
        self.assertEqual(res["content"][0]["text"], "42")

    def test_missing_tool_error(self):
        res = self.bridge.execute_tool("non_existent", {})
        self.assertTrue(res["isError"])
        self.assertIn("not found", res["content"][0]["text"])


if __name__ == "__main__":
    unittest.main()
