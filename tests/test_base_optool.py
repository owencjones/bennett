import subprocess
import sys
import pytest


class TestOPToolCommandLine:
    def test_cmdline_tool_runs(self):
        """Test that the CLI tool runs and returns exit code 0 for a valid BNF code."""
        result = subprocess.run(
            [sys.executable, "optool.py", "1304000H0AAAAAA"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Clobetasone butyrate" in result.stdout


    def test_cmdline_tool_runs_with_weighted_option(self):
        """Test that the CLI tool runs and returns exit code 0 for a valid BNF code."""
        result = subprocess.run(
            [sys.executable, "optool.py", "1304000H0AAAAAA", "--weighted"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Clobetasone butyrate" in result.stdout


    def test_cmdline_tool_runs_with_help_option(self):
        """Test that the CLI tool runs and returns exit code 0 for a valid BNF code."""
        result = subprocess.run(
            [sys.executable, "optool.py", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert result.stdout.startswith("Usage: OpenPrescribe Command Line Tool [-h] [--weighted] bnf_code")


if __name__ == "__main__":
    pytest.main([__file__])