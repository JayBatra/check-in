#! /usr/bin/env python

import sys
from warnings import catch_warnings

import click
from envparse import Env

from .github_api import GithubAPI


BASE_ENV_FILE_NAME = 'gh_chk_in_vars'

with catch_warnings(record=True):
    Env.read_envfile(f'/etc/{BASE_ENV_FILE_NAME}')
    Env.read_envfile(f'~/.config/.{BASE_ENV_FILE_NAME}')
    Env.read_envfile(f'~/.{BASE_ENV_FILE_NAME}')
    Env.read_envfile(f'.{BASE_ENV_FILE_NAME}')
    Env.read_envfile()


ENV_VAR_PREFIX = 'GH_CHK_IN_'
ENV_VAR_TMPL = f'{ENV_VAR_PREFIX}{{var_name}}'


@click.group()
@click.option('--private-key-file', prompt=True, envvar=ENV_VAR_TMPL.format(var_name='PRIVATE_KEY_FILE'))
@click.option('--app-id', prompt=True, envvar=ENV_VAR_TMPL.format(var_name='APP_ID'), type=int)
@click.option('--installation-id', prompt=True, envvar=ENV_VAR_TMPL.format(var_name='INSTALLATION_ID'), type=int)
@click.option('--repo-slug', prompt=True, envvar=ENV_VAR_TMPL.format(var_name='REPO_SLUG'))
@click.option('--name', prompt=True)
@click.option('--details-url')
@click.option('--external-id')
@click.option('--status')
@click.option('--started-at')
@click.option('--conclusion')
@click.option('--completed-at')
@click.option('--output')
@click.option('--actions')
@click.pass_context
def cli(ctx, **kwargs):
    app_id = kwargs.pop('app_id')
    installation_id = kwargs.pop('installation_id')
    private_key_file = kwargs.pop('private_key_file')
    repo_slug = kwargs.pop('repo_slug')
    gh_api = GithubAPI(app_id, installation_id, private_key_file, repo_slug)
    ctx.obj.update(kwargs)
    ctx.obj['github_api'] = gh_api


@cli.command()
@click.option('--head-branch', default='master')
@click.option('--head-sha', default='HEAD')
@click.pass_context
def post_check(ctx, head_branch, head_sha):
    try:
        with ctx.obj['github_api'] as gh_client:
            ctx.obj.pop('github_api')
            res = gh_client.post_check(head_branch, head_sha, ctx.obj)
        click.echo(f"Check Suite ID: {res['check_suite']['id']}")
        click.echo(f"Check Run ID: {res['id']}")
    except ValueError as val_exc:
        click.echo(val_exc)
        sys.exit(2)


@cli.command()
@click.option('--check-run-id', prompt=True, type=int)
@click.pass_context
def update_check(ctx, check_run_id):
    try:
        with ctx.obj['github_api'] as gh_client:
            ctx.obj.pop('github_api')
            res = gh_client.update_check(check_run_id, ctx.obj)
        click.echo(f"Check Suite ID: {res['check_suite']['id']}")
        click.echo(f"Check Run ID: {res['id']}")
    except ValueError as val_exc:
        click.echo(val_exc)
        sys.exit(2)


def main():
    return cli(obj={}, auto_envvar_prefix=ENV_VAR_PREFIX)


__name__ == '__main__' and main()