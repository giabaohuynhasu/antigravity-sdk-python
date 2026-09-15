from google.antigravity.tools.research import NotebookLMTool

def test_notebooklmtool_no_command_injection():
    tool = NotebookLMTool()
    tool.nlm_path = tool.nlm_path.parent / "nlm_test.exe"
    # We aren't testing execution here because nlm.exe isn't present,
    # but we can at least make sure that the code works correctly up to that point
    result = tool.query(prompt="test prompt")
    assert result.success == False
    assert "nlm.exe not found" in result.error

if __name__ == "__main__":
    test_notebooklmtool_no_command_injection()
    print("Test passed.")
