"""Snapshot Restore Singleton"""

import click
from curator.cli_singletons.object_class import CLIAction
from curator.cli_singletons.utils import json_to_dict, validate_filter_json


# pylint: disable=line-too-long
@click.command()
@click.option('--repository', type=str, required=True, help='Snapshot repository')
@click.option('--name', type=str, help='Snapshot name', required=False, default=None)
@click.option(
    '--index',
    multiple=True,
    help='Index name to restore. (Can invoke repeatedly for multiple indices)',
)
@click.option(
    '--rename_pattern', type=str, help='Rename pattern', required=False, default=None
)
@click.option(
    '--rename_replacement',
    type=str,
    help='Rename replacement',
    required=False,
    default=None,
)
@click.option(
    '--extra_settings',
    type=str,
    help='JSON version of extra_settings (see documentation)',
    callback=json_to_dict,
)
@click.option(
    '--include_aliases',
    is_flag=True,
    show_default=True,
    help='Include aliases with restored indices.',
)
@click.option(
    '--ignore_unavailable',
    is_flag=True,
    show_default=True,
    help='Ignore unavailable shards/indices.',
)
@click.option(
    '--include_global_state',
    is_flag=True,
    show_default=True,
    help='Restore cluster global state with snapshot.',
)
@click.option(
    '--partial',
    is_flag=True,
    show_default=True,
    help='Restore partial data (from snapshot taken with --partial).',
)
@click.option(
    '--wait_for_completion/--no-wait_for_completion',
    default=True,
    show_default=True,
    help='Wait for the snapshot to complete',
)
@click.option(
    '--wait_interval',
    default=9,
    type=int,
    help='Seconds to wait between completion checks.',
)
@click.option(
    '--max_wait',
    default=-1,
    type=int,
    help='Maximum number of seconds to wait_for_completion',
)
@click.option(
    '--skip_repo_fs_check',
    is_flag=True,
    show_default=True,
    help='Skip repository filesystem access validation.',
)
@click.option(
    '--ignore_empty_list',
    is_flag=True,
    help='Do not raise exception if there are no actionable indices',
)
@click.option(
    '--allow_ilm_indices/--no-allow_ilm_indices',
    help='Allow Curator to operate on Index Lifecycle Management monitored indices.',
    default=False,
    show_default=True,
)
@click.option(
    '--include_hidden/--no-include_hidden',
    help='Allow Curator to operate on hidden indices (and data_streams).',
    default=False,
    show_default=True,
)
@click.option(
    '--filter_list',
    callback=validate_filter_json,
    help='JSON array of filters selecting snapshots to act on.',
    required=True,
)
@click.pass_context
def restore(
    ctx,
    repository,
    name,
    index,
    rename_pattern,
    rename_replacement,
    extra_settings,
    include_aliases,
    ignore_unavailable,
    include_global_state,
    partial,
    wait_for_completion,
    wait_interval,
    max_wait,
    skip_repo_fs_check,
    ignore_empty_list,
    allow_ilm_indices,
    include_hidden,
    filter_list,
):
    """
    Restore Indices
    """
    indices = list(index)
    manual_options = {
        'name': name,
        'extra_settings': extra_settings,
        'indices': indices,
        'rename_pattern': rename_pattern,
        'rename_replacement': rename_replacement,
        'ignore_unavailable': ignore_unavailable,
        'include_aliases': include_aliases,
        'include_global_state': include_global_state,
        'partial': partial,
        'skip_repo_fs_check': skip_repo_fs_check,
        'wait_for_completion': wait_for_completion,
        'max_wait': max_wait,
        'wait_interval': wait_interval,
        'allow_ilm_indices': allow_ilm_indices,
        'include_hidden': include_hidden,
    }
    # ctx.info_name is the name of the function or name specified in
    # @click.command decorator
    action = CLIAction(
        ctx.info_name,
        ctx.obj['configdict'],
        manual_options,
        filter_list,
        ignore_empty_list,
        repository=repository,
    )
    action.do_singleton_action(dry_run=ctx.obj['dry_run'])
