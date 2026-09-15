import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

from google.antigravity.tools.research import NotebookLMTool

class TestNotebookLMTool(unittest.TestCase):
    @patch("google.antigravity.tools.research.Path.exists")
    @patch("google.antigravity.tools.research.subprocess.run")
    def test_query_secure_subprocess(self, mock_run, mock_exists):
        # Arrange
        mock_exists.return_value = True
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = "Test output"
        mock_proc.stderr = ""
        mock_run.return_value = mock_proc

        tool = NotebookLMTool()
        prompt = "malicious\" prompt"
        nid = "notebook_id_1"

        # Act
        result = tool.query(prompt, notebook_id=nid)

        # Assert
        self.assertTrue(result.success)
        self.assertEqual(result.output, "Test output")

        # Verify that subprocess.run was called securely with a list of arguments,
        # avoiding shell=True or string construction for powershell.
        mock_run.assert_called_once_with(
            [str(tool.nlm_path), "query", nid, prompt],
            capture_output=True,
            text=True,
            timeout=60
        )

if __name__ == "__main__":
    unittest.main()
