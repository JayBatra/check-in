"""Tests for functions implemented in cli.py."""

import click
from pytest_mock import mocker
from click.testing import CliRunner
from check_in.cli import cli

def test_cli_method(mocker):
    runner = CliRunner()
    mocker.patch("check_in.cli.GithubAPI")
    mocker.return_value = "test"
    result = runner.invoke(cli, ['--private-key-file', "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.pem"])
    assert result.exit_code == 0    
