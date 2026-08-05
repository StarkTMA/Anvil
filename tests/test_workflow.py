import pytest
from anvil.lib.schemas import JsonSchemes

def test_github_release_workflow_generation():
    workflow_content = JsonSchemes.github_release_workflow("test_project", "Test Project")
    assert "--tech-notes" in workflow_content
    assert ".pdf" in workflow_content
    assert "newline=\"\\n\"" in workflow_content
    assert "softprops/action-gh-release@v2" in workflow_content
