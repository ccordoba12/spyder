# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

"""
Spyder configuration options

Note: Leave this file free of Qt related imports, so that it can be used to
quickly load a user config file
"""

import os
import os.path as osp
import sys

# Local import
from spyder.config.base import (CHECK_ALL, EXCLUDED_NAMES, get_home_dir,
                                SUBFOLDER)
from spyder.config.fonts import MEDIUM, SANS_SERIF
from spyder.config.user import UserConfig
from spyder.config.utils import IMPORT_EXT
from spyder.config.appearance import APPEARANCE
from spyder.plugins.editor.utils.findtasks import TASKS_PATTERN
from spyder.utils.introspection.module_completion import PREFERRED_MODULES


# =============================================================================
# Main constants
# =============================================================================
# Find in files exclude patterns
EXCLUDE_PATTERNS = ['*.csv, *.dat, *.log, *.tmp, *.bak, *.orig']

# Extensions that should be visible in Spyder's file/project explorers
SHOW_EXT = ['.py', '.ipynb', '.txt', '.dat', '.pdf', '.png', '.svg']

# Extensions supported by Spyder (Editor or Variable explorer)
USEFUL_EXT = IMPORT_EXT + SHOW_EXT

# Name filters for file/project explorers (excluding files without extension)
NAME_FILTERS = ['README', 'INSTALL', 'LICENSE', 'CHANGELOG'] + \
               ['*' + _ext for _ext in USEFUL_EXT if _ext]

# Port used to detect if there is a running instance and to communicate with
# it to open external files
OPEN_FILES_PORT = 21128

# OS Specific
WIN = os.name == 'nt'
MAC = sys.platform == 'darwin'
LINUX = sys.platform.startswith('linux')
CTRL = "Meta" if MAC else "Ctrl"


# Modules to be preloaded for Rope and Jedi
PRELOAD_MDOULES = ', '.join(PREFERRED_MODULES)


# =============================================================================
#  Defaults
# =============================================================================
DEFAULTS = [
            ('main',
             {
              'opengl': 'software',
              'single_instance': True,
              'open_files_port': OPEN_FILES_PORT,
              'tear_off_menus': False,
              'normal_screen_resolution': True,
              'high_dpi_scaling': False,
              'high_dpi_custom_scale_factor': False,
              'high_dpi_custom_scale_factors': '1.5',
              'vertical_dockwidget_titlebars': False,
              'vertical_tabs': False,
              'animated_docks': True,
              'prompt_on_exit': False,
              'panes_locked': True,
              'window/size': (1260, 740),
              'window/position': (10, 10),
              'window/is_maximized': True,
              'window/is_fullscreen': False,
              'window/prefs_dialog_size': (1050, 530),
              'show_status_bar': True,
              'memory_usage/enable': True,
              'memory_usage/timeout': 2000,
              'cpu_usage/enable': False,
              'cpu_usage/timeout': 2000,
              'use_custom_margin': True,
              'custom_margin': 0,
              'use_custom_cursor_blinking': False,
              'show_internal_errors': True,
              'check_updates_on_startup': True,
              'toolbars_visible': True,
              'cursor/width': 2,
              'completion/size': (300, 180),
              'report_error/remember_me': False,
              'report_error/remember_token': False,
              }),
            ('quick_layouts',
             {
              'place_holder': '',
              'names': ['Matlab layout', 'Rstudio layout', 'Vertical split', 'Horizontal split'],
              'order': ['Matlab layout', 'Rstudio layout', 'Vertical split', 'Horizontal split'],
              'active': ['Matlab layout', 'Rstudio layout', 'Vertical split', 'Horizontal split'],
              }),
            ('internal_console',
             {
              'max_line_count': 300,
              'working_dir_history': 30,
              'working_dir_adjusttocontents': False,
              'wrap': True,
              'codecompletion/auto': False,
              'external_editor/path': 'SciTE',
              'external_editor/gotoline': '-goto:',
              }),
            ('main_interpreter',
             {
              'default': True,
              'custom': False,
              'umr/enabled': True,
              'umr/verbose': True,
              'umr/namelist': [],
              'custom_interpreters_list': [],
              'custom_interpreter': '',
              }),
            ('ipython_console',
             {
              'show_banner': True,
              'completion_type': 0,
              'use_pager': False,
              'show_calltips': True,
              'ask_before_closing': False,
              'show_reset_namespace_warning': True,
              'buffer_size': 500,
              'pylab': True,
              'pylab/autoload': False,
              'pylab/backend': 0,
              'pylab/inline/figure_format': 0,
              'pylab/inline/resolution': 72,
              'pylab/inline/width': 6,
              'pylab/inline/height': 4,
              'pylab/inline/bbox_inches': True,
              'startup/run_lines': '',
              'startup/use_run_file': False,
              'startup/run_file': '',
              'greedy_completer': False,
              'jedi_completer': False,
              'autocall': 0,
              'symbolic_math': False,
              'in_prompt': '',
              'out_prompt': '',
              'show_elapsed_time': False,
              'ask_before_restart': True,
              # This is True because there are libraries like Pyomo
              # that generate a lot of Command Prompts while running,
              # and that's extremely annoying for Windows users.
              'hide_cmd_windows': True
              }),
            ('variable_explorer',
             {
              'check_all': CHECK_ALL,
              'dataframe_format': '.6g',  # No percent sign to avoid problems
                                          # with ConfigParser's interpolation
              'excluded_names': EXCLUDED_NAMES,
              'exclude_private': True,
              'exclude_uppercase': True,
              'exclude_capitalized': False,
              'exclude_unsupported': True,
              'truncate': True,
              'minmax': False,
              'show_callable_attributes': True,
              'show_special_attributes': False
             }),
            ('plots',
             {
              'mute_inline_plotting': True,
              'show_plot_outline': False,
              'auto_fit_plotting': True
             }),
            ('editor',
             {
              'printer_header/font/family': SANS_SERIF,
              'printer_header/font/size': MEDIUM,
              'printer_header/font/italic': False,
              'printer_header/font/bold': False,
              'wrap': False,
              'wrapflag': True,
              'todo_list': True,
              'realtime_analysis': True,
              'realtime_analysis/timeout': 2500,
              'outline_explorer': True,
              'line_numbers': True,
              'blank_spaces': False,
              'edge_line': True,
              'edge_line_columns': '79',
              'indent_guides': False,
              'scroll_past_end': False,
              'toolbox_panel': True,
              'close_parentheses': True,
              'close_quotes': True,
              'add_colons': True,
              'auto_unindent': True,
              'indent_chars': '*    *',
              'tab_stop_width_spaces': 4,
              'check_eol_chars': True,
              'convert_eol_on_save': False,
              'convert_eol_on_save_to': 'LF',
              'tab_always_indent': False,
              'intelligent_backspace': True,
              'underline_errors': False,
              'highlight_current_line': True,
              'highlight_current_cell': True,
              'occurrence_highlighting': True,
              'occurrence_highlighting/timeout': 1500,
              'always_remove_trailing_spaces': False,
              'show_tab_bar': True,
              'show_class_func_dropdown': False,
              'max_recent_files': 20,
              'save_all_before_run': True,
              'focus_to_editor': True,
              'run_cell_copy': False,
              'onsave_analysis': False,
              'autosave_enabled': True,
              'autosave_interval': 60,
              'docstring_type': 'Numpydoc',
              'strip_trailing_spaces_on_modify': True,
              }),
            ('historylog',
             {
              'enable': True,
              'max_entries': 100,
              'wrap': True,
              'go_to_eof': True,
              'line_numbers': False,
              }),
            ('help',
             {
              'enable': True,
              'max_history_entries': 20,
              'wrap': True,
              'connect/editor': False,
              'connect/ipython_console': False,
              'math': True,
              'automatic_import': True,
              }),
            ('onlinehelp',
             {
              'enable': True,
              'zoom_factor': .8,
              'max_history_entries': 20,
              }),
            ('outline_explorer',
             {
              'enable': True,
              'show_fullpath': False,
              'show_all_files': False,
              'group_cells': True,
              'sort_files_alphabetically': False,
              'show_comments': True,
              }),
            ('project_explorer',
             {
              'name_filters': NAME_FILTERS,
              'show_all': True,
              'show_hscrollbar': True,
              'visible_if_project_open': True
              }),
            ('explorer',
             {
              'enable': True,
              'wrap': True,
              'name_filters': NAME_FILTERS,
              'show_hidden': True,
              'show_all': True,
              'show_icontext': False,
              'single_click_to_open': False,
              }),
            ('find_in_files',
             {
              'enable': True,
              'supported_encodings': ["utf-8", "iso-8859-1", "cp1252"],
              'exclude': EXCLUDE_PATTERNS,
              'exclude_regexp': False,
              'search_text_regexp': False,
              'search_text': [''],
              'search_text_samples': [TASKS_PATTERN],
              'more_options': True,
              'case_sensitive': False
              }),
            ('breakpoints',
             {
              'enable': True,
              }),
            ('profiler',
             {
              'enable': True,
              }),
            ('pylint',
             {
              'enable': True,
              }),
            ('workingdir',
             {
              'working_dir_adjusttocontents': False,
              'working_dir_history': 20,
              'console/use_project_or_home_directory': False,
              'console/use_cwd': True,
              'console/use_fixed_directory': False,
              }),
            ('shortcuts',
             {
              # ---- Global ----
              # -- In app/spyder.py
              '_/close pane': "Shift+Ctrl+F4",
              '_/lock unlock panes': "Shift+Ctrl+F5",
              '_/use next layout': "Shift+Alt+PgDown",
              '_/use previous layout': "Shift+Alt+PgUp",
              '_/preferences': "Ctrl+Alt+Shift+P",
              '_/maximize pane': "Ctrl+Alt+Shift+M",
              '_/fullscreen mode': "F11",
              '_/save current layout': "Shift+Alt+S",
              '_/layout preferences': "Shift+Alt+P",
              '_/show toolbars': "Alt+Shift+T",
              '_/spyder documentation': "F1",
              '_/restart': "Shift+Alt+R",
              '_/quit': "Ctrl+Q",
              # -- In plugins/editor
              '_/file switcher': 'Ctrl+P',
              '_/symbol finder': 'Ctrl+Alt+P',
              '_/debug': "Ctrl+F5",
              '_/debug step over': "Ctrl+F10",
              '_/debug continue': "Ctrl+F12",
              '_/debug step into': "Ctrl+F11",
              '_/debug step return': "Ctrl+Shift+F11",
              '_/debug exit': "Ctrl+Shift+F12",
              '_/run': "F5",
              '_/configure': "Ctrl+F6",
              '_/re-run last script': "F6",
              # -- In plugins/init
              '_/switch to help': "Ctrl+Shift+H",
              '_/switch to outline_explorer': "Ctrl+Shift+O",
              '_/switch to editor': "Ctrl+Shift+E",
              '_/switch to historylog': "Ctrl+Shift+L",
              '_/switch to onlinehelp': "Ctrl+Shift+D",
              '_/switch to project_explorer': "Ctrl+Shift+P",
              '_/switch to ipython_console': "Ctrl+Shift+I",
              '_/switch to variable_explorer': "Ctrl+Shift+V",
              '_/switch to find_in_files': "Ctrl+Shift+F",
              '_/switch to explorer': "Ctrl+Shift+X",
              '_/switch to plots': "Ctrl+Shift+G",
              # -- In widgets/findreplace.py
              '_/find text': "Ctrl+F",
              '_/find next': "F3",
              '_/find previous': "Shift+F3",
              '_/replace text': "Ctrl+R",
              '_/hide find and replace': "Escape",
              # ---- Editor ----
              # -- In widgets/sourcecode/codeeditor.py
              'editor/code completion': CTRL+'+Space',
              'editor/duplicate line': "Ctrl+Alt+Up" if WIN else \
                                       "Shift+Alt+Up",
              'editor/copy line': "Ctrl+Alt+Down" if WIN else \
                                  "Shift+Alt+Down",
              'editor/delete line': 'Ctrl+D',
              'editor/transform to uppercase': 'Ctrl+Shift+U',
              'editor/transform to lowercase': 'Ctrl+U',
              'editor/indent': 'Ctrl+]',
              'editor/unindent': 'Ctrl+[',
              'editor/move line up': "Alt+Up",
              'editor/move line down': "Alt+Down",
              'editor/go to new line': "Ctrl+Shift+Return",
              'editor/go to definition': "Ctrl+G",
              'editor/toggle comment': "Ctrl+1",
              'editor/blockcomment': "Ctrl+4",
              'editor/unblockcomment': "Ctrl+5",
              'editor/start of line': "Meta+A",
              'editor/end of line': "Meta+E",
              'editor/previous line': "Meta+P",
              'editor/next line': "Meta+N",
              'editor/previous char': "Meta+B",
              'editor/next char': "Meta+F",
              'editor/previous word': "Ctrl+Left",
              'editor/next word': "Ctrl+Right",
              'editor/kill to line end': "Meta+K",
              'editor/kill to line start': "Meta+U",
              'editor/yank': 'Meta+Y',
              'editor/rotate kill ring': 'Shift+Meta+Y',
              'editor/kill previous word': 'Meta+Backspace',
              'editor/kill next word': 'Meta+D',
              'editor/start of document': 'Ctrl+Home',
              'editor/end of document': 'Ctrl+End',
              'editor/undo': 'Ctrl+Z',
              'editor/redo': 'Ctrl+Shift+Z',
              'editor/cut': 'Ctrl+X',
              'editor/copy': 'Ctrl+C',
              'editor/paste': 'Ctrl+V',
              'editor/delete': 'Del',
              'editor/select all': "Ctrl+A",
              # -- In widgets/editor.py
              'editor/inspect current object': 'Ctrl+I',
              'editor/breakpoint': 'F12',
              'editor/conditional breakpoint': 'Shift+F12',
              'editor/run selection': "F9",
              'editor/go to line': 'Ctrl+L',
              'editor/go to previous file': CTRL + '+Shift+Tab',
              'editor/go to next file': CTRL + '+Tab',
              'editor/cycle to previous file': 'Ctrl+PgUp',
              'editor/cycle to next file': 'Ctrl+PgDown',
              'editor/new file': "Ctrl+N",
              'editor/open last closed':"Ctrl+Shift+T",
              'editor/open file': "Ctrl+O",
              'editor/save file': "Ctrl+S",
              'editor/save all': "Ctrl+Alt+S",
              'editor/save as': 'Ctrl+Shift+S',
              'editor/close all': "Ctrl+Shift+W",
              'editor/last edit location': "Ctrl+Alt+Shift+Left",
              'editor/previous cursor position': "Ctrl+Alt+Left",
              'editor/next cursor position': "Ctrl+Alt+Right",
              'editor/previous warning': "Ctrl+Alt+Shift+,",
              'editor/next warning': "Ctrl+Alt+Shift+.",
              'editor/zoom in 1': "Ctrl++",
              'editor/zoom in 2': "Ctrl+=",
              'editor/zoom out': "Ctrl+-",
              'editor/zoom reset': "Ctrl+0",
              'editor/close file 1': "Ctrl+W",
              'editor/close file 2': "Ctrl+F4",
              'editor/run cell': CTRL + '+Return',
              'editor/run cell and advance': 'Shift+Return',
              'editor/go to next cell': 'Ctrl+Down',
              'editor/go to previous cell': 'Ctrl+Up',
              'editor/re-run last cell': 'Alt+Return',
              'editor/split vertically': "Ctrl+{",
              'editor/split horizontally': "Ctrl+_",
              'editor/close split panel': "Alt+Shift+W",
              'editor/docstring': "Ctrl+Alt+D",
              # -- In Breakpoints
              '_/switch to breakpoints': "Ctrl+Shift+B",
              # ---- Consoles (in widgets/shell) ----
              'console/inspect current object': "Ctrl+I",
              'console/clear shell': "Ctrl+L",
              'console/clear line': "Shift+Escape",
              # ---- In Pylint ----
              'pylint/run analysis': "F8",
              # ---- In Profiler ----
              'profiler/run profiler': "F10",
              # ---- In widgets/ipythonconsole/shell.py ----
              'ipython_console/new tab': "Ctrl+T",
              'ipython_console/reset namespace': "Ctrl+Alt+R",
              'ipython_console/restart kernel': "Ctrl+.",
              # ---- In widgets/arraybuider.py ----
              'array_builder/enter array inline': "Ctrl+Alt+M",
              'array_builder/enter array table': "Ctrl+M",
              # ---- In widgets/variableexplorer/aarayeditor.py ----
              'variable_explorer/copy': 'Ctrl+C',
              # ---- In widgets/plots/figurebrowser.py ----
              'plots/copy': 'Ctrl+C',
              'plots/previous figure': 'Ctrl+PgUp',
              'plots/next figure': 'Ctrl+PgDown',
              # ---- In widgets/explorer ----
              'explorer/copy file': 'Ctrl+C',
              'explorer/paste file': 'Ctrl+V',
              'explorer/copy absolute path': 'Ctrl+Alt+C',
              'explorer/copy relative path': 'Ctrl+Alt+Shift+C',
              }),
            ('appearance', APPEARANCE),
            ('lsp-server',
             {
              # This option is not used with the LSP server config
              # It is used to disable hover hints in the editor
              'enable_hover_hints': True,
              'code_completion': True,
              'jedi_definition': True,
              'jedi_definition/follow_imports': True,
              'jedi_signature_help': True,
              'preload_modules': PRELOAD_MDOULES,
              'pyflakes': True,
              'mccabe': False,
              'pycodestyle': False,
              'pycodestyle/filename': '',
              'pycodestyle/exclude': '',
              'pycodestyle/select': '',
              'pycodestyle/ignore': '',
              'pycodestyle/max_line_length': 79,
              'pydocstyle': False,
              'pydocstyle/convention': 'numpy',
              'pydocstyle/select': '',
              'pydocstyle/ignore': '',
              'pydocstyle/match': '(?!test_).*\\.py',
              'pydocstyle/match_dir': '[^\\.].*',
              'advanced/command_launch': 'pyls',
              'advanced/host': '127.0.0.1',
              'advanced/port': 2087,
              'advanced/external': False,
              'advanced/stdio': False
             })
            ]


# =============================================================================
# Config instance
# =============================================================================
# IMPORTANT NOTES:
# 1. If you want to *change* the default value of a current option, you need to
#    do a MINOR update in config version, e.g. from 3.0.0 to 3.1.0
# 2. If you want to *remove* options that are no longer needed in our codebase,
#    or if you want to *rename* options, then you need to do a MAJOR update in
#    version, e.g. from 3.0.0 to 4.0.0
# 3. You don't need to touch this value if you're just adding a new option
CONF_VERSION = '50.2.0'


# Main configuration instance
try:
    CONF = UserConfig('spyder', defaults=DEFAULTS, load=True,
                      version=CONF_VERSION, subfolder=SUBFOLDER, backup=True,
                      raw_mode=True)
except Exception:
    CONF = UserConfig('spyder', defaults=DEFAULTS, load=False,
                      version=CONF_VERSION, subfolder=SUBFOLDER, backup=True,
                      raw_mode=True)

# Removing old .spyder.ini location:
old_location = osp.join(get_home_dir(), '.spyder.ini')
if osp.isfile(old_location):
    os.remove(old_location)
