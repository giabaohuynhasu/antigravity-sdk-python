# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for native research tools."""

import subprocess
from pathlib import Path
from unittest import mock

from absl.testing import absltest

from google.antigravity.tools import research


class NotebookLMToolTest(absltest.TestCase):

    def setUp(self):
        super().setUp()
        self.tool = research.NotebookLMTool()

    @mock.patch.object(Path, "exists", return_value=True)
    @mock.patch("subprocess.run")
    def test_query_success(self, mock_run, mock_exists):
        mock_proc = mock.MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = "Test output result\n"
        mock_run.return_value = mock_proc

        result = self.tool.query("Test prompt")

        self.assertTrue(result.success)
        self.assertEqual(result.output, "Test output result")
        self.assertIsNone(result.error)
        mock_run.assert_called_once()

    @mock.patch.object(Path, "exists", return_value=False)
    def test_query_tool_not_found(self, mock_exists):
        result = self.tool.query("Test prompt")

        self.assertFalse(result.success)
        self.assertEqual(result.output, "")
        self.assertIn("nlm.exe not found", result.error)

    @mock.patch.object(Path, "exists", return_value=True)
    @mock.patch("subprocess.run")
    def test_query_exception(self, mock_run, mock_exists):
        mock_run.side_effect = Exception("Subprocess failed")

        result = self.tool.query("Test prompt")

        self.assertFalse(result.success)
        self.assertEqual(result.output, "")
        self.assertEqual(result.error, "Subprocess failed")


class DuckDBSQLToolTest(absltest.TestCase):

    def setUp(self):
        super().setUp()
        self.tool = research.DuckDBSQLTool()

    def test_execute_success(self):
        result = self.tool.execute("SELECT 42 AS num")

        self.assertTrue(result.success)
        self.assertIn("42", result.output)
        self.assertIsNone(result.error)

    def test_execute_invalid_sql(self):
        result = self.tool.execute("SELECT * FROM non_existent_table")

        self.assertFalse(result.success)
        self.assertEqual(result.output, "")
        self.assertIsNotNone(result.error)
        self.assertIn("non_existent_table", result.error)


class SparkEmailToolTest(absltest.TestCase):

    def setUp(self):
        super().setUp()
        self.tool = research.SparkEmailTool()

    @mock.patch("smtplib.SMTP")
    def test_send_success(self, mock_smtp):
        mock_server = mock.MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        result = self.tool.send("Test Subject", "Test Body")

        self.assertTrue(result.success)
        self.assertIn("Email successfully sent", result.output)
        self.assertIsNone(result.error)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once()
        mock_server.send_message.assert_called_once()

    @mock.patch("smtplib.SMTP")
    def test_send_exception(self, mock_smtp):
        mock_server = mock.MagicMock()
        mock_server.send_message.side_effect = Exception("SMTP connection failed")
        mock_smtp.return_value.__enter__.return_value = mock_server

        result = self.tool.send("Test Subject", "Test Body")

        self.assertFalse(result.success)
        self.assertEqual(result.output, "")
        self.assertEqual(result.error, "SMTP connection failed")


if __name__ == "__main__":
    absltest.main()
