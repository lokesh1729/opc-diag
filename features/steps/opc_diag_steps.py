# -*- coding: utf-8 -*-
#
# opc_diag_steps.py
#
# Copyright (C) 2012, 2013 Steve Canny scanny@cisco.com
#
# This module is part of opc-diag and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Acceptance test steps for opc-diag package."""

import os
import shutil

from behave import given, then, when

from helpers import (
    assertManifestsMatch, assertPackagesMatch, OpcCommand, ref_pkg_path,
    scratch_path
)
from step_data import Manifest


SUBCMD_BROWSE = 'browse'
SUBCMD_DIFF = 'diff'
SUBCMD_DIFF_ITEM = 'diff-item'
SUBCMD_EXTRACT = 'extract'
SUBCMD_REPACKAGE = 'repackage'
SUBCMD_SUBSTITUTE = 'substitute'
URI_CONTENT_TYPES = '[Content_Types].xml'
URI_CORE_PROPS = 'docProps/core.xml'
URI_PKG_RELS = '_rels/.rels'
URI_SLIDE_MASTER = 'ppt/slideMasters/slideMaster1.xml'


# commonly used paths ------------------
base_dir_pkg_path = ref_pkg_path('source')
base_zip_pkg_path = ref_pkg_path('base.pptx')
pkg_paths = {'dir': base_dir_pkg_path, 'zip': base_zip_pkg_path}

base_pkg_path = ref_pkg_path('base.pptx')
changed_pkg_path = ref_pkg_path('changed.pptx')
expanded_dir = ref_pkg_path('source')
extract_dir = scratch_path('extracted')
scratch_pkg_path = scratch_path('test_out.pptx')


# given ====================================================

@given('a target directory that does not exist')
def step_remove_target_directory(context):
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)


# when =====================================================

@when('I issue a command to browse an XML part in a {pkg_type} package')
def step_issue_command_to_browse_pkg_part(context, pkg_type):
    context.cmd = OpcCommand(SUBCMD_BROWSE, pkg_paths[pkg_type],
                             URI_CORE_PROPS).execute()


@when('I issue a command to browse the content types of a {pkg_type} package')
def step_issue_command_to_browse_content_types(context, pkg_type):
    context.cmd = OpcCommand(SUBCMD_BROWSE, pkg_paths[pkg_type],
                             URI_CONTENT_TYPES).execute()


@when('I issue a command to browse the package rels of a {pkg_type} package')
def step_issue_command_to_browse_pkg_rels(context, pkg_type):
    context.cmd = OpcCommand(SUBCMD_BROWSE, pkg_paths[pkg_type],
                             URI_PKG_RELS).execute()


@when('I issue a command to diff the content types between two packages')
def step_command_diff_content_types(context):
    context.cmd = OpcCommand(
        SUBCMD_DIFF_ITEM, base_pkg_path, changed_pkg_path, URI_CONTENT_TYPES
    ).execute()


@when('I issue a command to diff the package rels between two packages')
def step_command_diff_pkg_rels_item(context):
    context.cmd = OpcCommand(
        SUBCMD_DIFF_ITEM, base_pkg_path, changed_pkg_path, URI_PKG_RELS
    ).execute()


@when('I issue a command to diff the slide master between two packages')
def step_command_diff_slide_master(context):
    context.cmd = OpcCommand(
        SUBCMD_DIFF_ITEM, base_pkg_path, changed_pkg_path, URI_SLIDE_MASTER
    ).execute()


@when('I issue a command to diff two packages')
def step_command_diff_two_packages(context):
    context.cmd = OpcCommand(
        SUBCMD_DIFF, base_pkg_path, changed_pkg_path
    ).execute()


@when('I issue a command to extract a package')
def step_command_extract_package(context):
    context.cmd = OpcCommand(
        SUBCMD_EXTRACT, base_pkg_path, extract_dir
    ).execute()


@when('I issue a command to repackage an expanded package directory')
def step_command_repackage_expanded_pkg_dir(context):
    context.cmd = OpcCommand(
        SUBCMD_REPACKAGE, expanded_dir, scratch_pkg_path
    ).execute()


@when('I issue a command to substitute a package item')
def step_command_substitute_pkg_item(context):
    context.cmd = OpcCommand(
        SUBCMD_SUBSTITUTE, URI_SLIDE_MASTER, changed_pkg_path, base_pkg_path,
        scratch_pkg_path
    ).execute()


# then =====================================================

@then('a zip package with matching contents appears at the path I specified')
def step_then_matching_zip_pkg_appears_at_specified_path(context):
    context.cmd.assert_stderr_empty()
    context.cmd.assert_stdout_empty()
    assertPackagesMatch(expanded_dir, scratch_pkg_path)


@then('the content types diff appears on stdout')
def step_then_content_types_diff_appears_on_stdout(context):
    context.cmd.assert_stderr_empty()
    context.cmd.assert_stdout_matches('diff-item.content_types.txt')


@then('the formatted content types item appears on stdout')
def step_then_content_types_appear_on_stdout(context):
    context.cmd.assert_stderr_empty()
    context.cmd.assert_stdout_matches('browse.content_types.txt')


@then('the formatted package part XML appears on stdout')
def step_then_pkg_part_xml_appears_on_stdout(context):
    context.cmd.assert_stderr_empty()
    context.cmd.assert_stdout_matches('browse.core_props.txt')


@then('the formatted package rels XML appears on stdout')
def step_then_pkg_rels_xml_appears_on_stdout(context):
    context.cmd.assert_stderr_empty()
    context.cmd.assert_stdout_matches('browse.pkg_rels.txt')


@then('the package diff appears on stdout')
def step_then_pkg_diff_appears_on_stdout(context):
    context.cmd.assert_stderr_empty()
    context.cmd.assert_stdout_matches('diff.txt')


@then('the package items appear in the target directory')
def step_then_pkg_appears_in_target_dir(context):
    context.cmd.assert_stderr_empty()
    context.cmd.assert_stdout_empty()
    assertPackagesMatch(base_pkg_path, extract_dir)


@then('the package rels diff appears on stdout')
def step_then_pkg_rels_diff_appears_on_stdout(context):
    context.cmd.assert_stderr_empty()
    context.cmd.assert_stdout_matches('diff-item.pkg_rels.txt')


@then('the resulting package contains the substituted item')
def step_then_resulting_pkg_contains_substituted_item(context):
    context.cmd.assert_stderr_empty()
    context.cmd.assert_stdout_matches('substitute.txt')
    subst_sha = Manifest(changed_pkg_path)[URI_SLIDE_MASTER]
    expected_manifest = Manifest(base_pkg_path)
    expected_manifest[URI_SLIDE_MASTER] = subst_sha
    actual_manifest = Manifest(scratch_pkg_path)
    assertManifestsMatch(
        actual_manifest, expected_manifest, 'actual', 'expected')


@then('the slide master diff appears on stdout')
def step_then_slide_master_diff_appears_on_stdout(context):
    context.cmd.assert_stderr_empty()
    context.cmd.assert_stdout_matches('diff-item.slide_master.txt')
