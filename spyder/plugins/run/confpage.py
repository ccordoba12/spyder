# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

"""Run configuration page."""

# Standard library imports
import functools
from copy import deepcopy
from typing import Dict, List, Set, Tuple
from uuid import uuid4

# Third party imports
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QAbstractItemView,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

# Local imports
from spyder.api.preferences import PluginConfigPage
from spyder.api.translations import _
from spyder.api.widgets.comboboxes import SpyderComboBox
from spyder.plugins.run.api import (
    ExtendedRunExecutionParameters, SupportedExecutionRunConfiguration)
from spyder.plugins.run.container import RunContainer
from spyder.plugins.run.models import (
    RunExecutorNamesListModel, ExecutorRunParametersTableModel)
from spyder.plugins.run.widgets import (
    ExecutionParametersDialog, RunDialogStatus)
from spyder.utils.stylesheet import AppStyle
from spyder.widgets.helperwidgets import HoverRowsTableView


def move_file_to_front(contexts: List[str]) -> List[str]:
    if 'file' in contexts:
        contexts.insert(0, contexts.pop(contexts.index('file')))
    return contexts


class RunParametersTableView(HoverRowsTableView):
    def __init__(self, parent, model):
        super().__init__(parent)
        self._parent = parent
        self.setModel(model)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSortingEnabled(True)
        self.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.selectionModel().selectionChanged.connect(self.selection)
        self.verticalHeader().hide()
        self.reset_plain()

        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.Stretch
        )
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

    def selection(self, index):
        self.update()
        self.isActiveWindow()

        # Detect if a row corresponds to a set of default parameters to prevent
        # users from deleting it.
        index = self.currentIndex().row()
        is_default = False
        if index >= 0:
            params_id = self._parent.table_model.params_index[index]
            params = self._parent.table_model.executor_conf_params[params_id]
            is_default = True if params.get("default") else False

        self._parent.set_clone_delete_btn_status(is_default=is_default)

        # Always enable edit button
        self._parent.edit_configuration_btn.setEnabled(True)

    def adjust_cells(self):
        """Adjust column size based on contents."""
        self.resizeColumnsToContents()
        model: ExecutorRunParametersTableModel = self.model()
        fm = self.horizontalHeader().fontMetrics()
        names = [fm.width(model.get_parameters_name(idx)) for idx in model]
        if names:
            self.setColumnWidth(
                ExecutorRunParametersTableModel.NAME, max(names))
        self.horizontalHeader().setStretchLastSection(True)

    def reset_plain(self):
        self.model().reset_model()
        self.adjust_cells()
        self.selectionModel().selectionChanged.connect(self.selection)

    def show_editor(self, new=False, clone=False):
        extension, context, params = None, None, None
        extensions, contexts, plugin_name, executor_params = (
            self._parent.get_executor_configurations()
        )

        if not new:
            index = self.currentIndex().row()
            model: ExecutorRunParametersTableModel = self.model()
            (extension, context, params) = model[index]

        self.dialog = ExecutionParametersDialog(
            self,
            plugin_name,
            executor_params,
            extensions,
            contexts,
            params,
            extension,
            context,
            new
        )

        self.dialog.setup()
        self.dialog.finished.connect(
            functools.partial(
                self.process_run_dialog_result,
                new=new, clone=clone, params=params
            )
        )

        if not clone:
            self.dialog.open()
        else:
            self.dialog.accept()

    def process_run_dialog_result(self, result, new=False,
                                  clone=False, params=None):
        status = self.dialog.status
        if status == RunDialogStatus.Close:
            return

        conf = self.dialog.get_configuration()
        if conf is None:
            return
        else:
            extension, context, new_executor_params = conf

        if not new and clone:
            new_executor_params["uuid"] = str(uuid4())
            new_executor_params["name"] = _('%s (copy)') % params['name']

        changes = []
        if params and not clone:
            changes.append(('deleted', params))

        changes.append(('new', new_executor_params))
        self.model().apply_changes(changes, extension, context)

    def clone_configuration(self):
        self.show_editor(clone=True)

    def focusInEvent(self, e):
        """Qt Override."""
        super().focusInEvent(e)
        self.selectRow(self.currentIndex().row())
        self.selection(self.currentIndex().row())

    def keyPressEvent(self, event):
        """Qt Override."""
        key = event.key()
        if key in [Qt.Key_Enter, Qt.Key_Return]:
            self.show_editor()
        elif key in [Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right]:
            super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def mouseDoubleClickEvent(self, event):
        """Qt Override."""
        self.show_editor()


class RunConfigPage(PluginConfigPage):
    """Default Run Settings configuration page."""

    def setup_page(self):
        self._params_to_delete = {}

        self.plugin_container: RunContainer = self.plugin.get_container()
        self.executor_model = RunExecutorNamesListModel(
            self, self.plugin_container.executor_model)
        self.table_model = ExecutorRunParametersTableModel(self)
        self.table_model.sig_data_changed.connect(
            lambda: self.set_modified(True)
        )

        self.all_executor_model: Dict[
            str, Dict[Tuple[str, str, str],
            ExtendedRunExecutionParameters]] = {}
        self.previous_executor_index: int = 0
        self.default_executor_conf_params: Dict[
            str, Dict[Tuple[str, str, str],
            ExtendedRunExecutionParameters]] = {}

        about_label = QLabel(
            _(
                "The following are the global configuration settings of the "
                "different plugins that can execute files in Spyder."
            )
        )
        about_label.setWordWrap(True)

        # The paremeters table needs to be created before the executor_combo
        # below, although is displayed after it.
        params_label = QLabel(_('Available parameters:'))
        self.params_table = RunParametersTableView(self, self.table_model)
        self.params_table.setMaximumHeight(180)

        params_table_layout = QHBoxLayout()
        params_table_layout.addSpacing(2 * AppStyle.MarginSize)
        params_table_layout.addWidget(self.params_table)
        params_table_layout.addSpacing(2 * AppStyle.MarginSize)

        executor_label = QLabel(_("Executor:"))
        self.executor_combo = SpyderComboBox(self)
        self.executor_combo.setMinimumWidth(250)
        self.executor_combo.currentIndexChanged.connect(
            self.executor_index_changed
        )
        self.executor_combo.setModel(self.executor_model)

        executor_layout = QHBoxLayout()
        executor_layout.addWidget(executor_label)
        executor_layout.addWidget(self.executor_combo)
        executor_layout.addStretch()

        self.new_configuration_btn = QPushButton(_("New parameters"))
        self.edit_configuration_btn = QPushButton(_("Edit selected"))
        self.clone_configuration_btn = QPushButton(_("Clone selected"))
        self.delete_configuration_btn = QPushButton(_("Delete selected"))
        self.reset_changes_btn = QPushButton(_("Reset changes"))
        self.edit_configuration_btn.setEnabled(False)
        self.delete_configuration_btn.setEnabled(False)
        self.clone_configuration_btn.setEnabled(False)

        self.new_configuration_btn.clicked.connect(
            self.create_new_configuration)
        self.edit_configuration_btn.clicked.connect(
            lambda checked: self.params_table.show_editor()
        )
        self.clone_configuration_btn.clicked.connect(
            self.clone_configuration)
        self.delete_configuration_btn.clicked.connect(
            self.delete_configuration)
        self.reset_changes_btn.clicked.connect(self.reset_changes)

        # Buttons layout
        btns = [
            self.new_configuration_btn,
            self.edit_configuration_btn,
            self.delete_configuration_btn,
            self.clone_configuration_btn,
            self.reset_changes_btn,
        ]
        sn_buttons_layout = QGridLayout()
        for i, btn in enumerate(btns):
            sn_buttons_layout.addWidget(btn, i, 1)
        sn_buttons_layout.setColumnStretch(0, 1)
        sn_buttons_layout.setColumnStretch(1, 2)
        sn_buttons_layout.setColumnStretch(2, 1)

        # --- Editor interactions tab ---
        newcb = self.create_checkbox
        saveall_box = newcb(_("Save all files before running script"),
                            'save_all_before_run')
        run_cell_box = newcb(_("Copy full cell contents to the console when "
                               "running code cells"), 'run_cell_copy')

        run_layout = QVBoxLayout()
        run_layout.addWidget(saveall_box)
        run_layout.addWidget(run_cell_box)
        run_widget = QWidget()
        run_widget.setLayout(run_layout)

        vlayout = QVBoxLayout()
        vlayout.addWidget(about_label)
        vlayout.addSpacing(3 * AppStyle.MarginSize)
        vlayout.addLayout(executor_layout)
        vlayout.addSpacing(3 * AppStyle.MarginSize)
        vlayout.addWidget(params_label)
        vlayout.addLayout(params_table_layout)
        vlayout.addSpacing(2 * AppStyle.MarginSize)
        vlayout.addLayout(sn_buttons_layout)
        vlayout.addStretch()
        executor_widget = QWidget()
        executor_widget.setLayout(vlayout)

        self.create_tab(_("Run executors"), executor_widget)
        self.create_tab(_("Editor interactions"), run_widget)

    def executor_index_changed(self, index: int):
        # Save previous executor configuration
        prev_executor_info = self.table_model.get_current_view()
        previous_executor_name, _ = self.executor_model.selected_executor(
            self.previous_executor_index)
        self.all_executor_model[previous_executor_name] = prev_executor_info

        # Handle current executor configuration
        executor, available_inputs = self.executor_model.selected_executor(
            index)
        container = self.plugin_container

        executor_conf_params = self.all_executor_model.get(executor, {})
        if executor_conf_params == {}:
            for (ext, context) in available_inputs:
                params = container.get_executor_configuration_parameters(
                    executor, ext, context
                )
                params = params["params"]
                for exec_params_id in params:
                    exec_params = params[exec_params_id]

                    # Don't display configs set for specific files. Here
                    # users are allowed to configure global configs, i.e. those
                    # that can be used by any file.
                    if exec_params.get("file_uuid") is not None:
                        continue

                    params_key = (ext, context, exec_params_id)
                    executor_conf_params[params_key] = exec_params

            self.default_executor_conf_params[executor] = deepcopy(
                executor_conf_params)

            self.all_executor_model[executor] = deepcopy(executor_conf_params)

        self.table_model.set_parameters(executor_conf_params)
        self.previous_executor_index = index
        self.set_clone_delete_btn_status()

        # Repopulating the params table removes any selection, so we need to
        # disable the edit button.
        if hasattr(self, "edit_configuration_btn"):
            self.edit_configuration_btn.setEnabled(False)

    def set_clone_delete_btn_status(self, is_default=False):
        # We need to enclose the code below in a try/except because these
        # buttons might not be created yet, which gives an AttributeError.
        try:
            if is_default:
                # Don't allow to delete default configurations, only to clone
                # them
                self.delete_configuration_btn.setEnabled(False)
                self.clone_configuration_btn.setEnabled(True)
            else:
                status = (
                    self.table_model.rowCount() != 0
                    and self.params_table.currentIndex().isValid()
                )
                self.delete_configuration_btn.setEnabled(status)
                self.clone_configuration_btn.setEnabled(status)
        except AttributeError:
            pass

    def get_executor_configurations(self) -> Dict[
            str, SupportedExecutionRunConfiguration]:
        exec_index = self.executor_combo.currentIndex()
        executor_name, available_inputs = (
            self.executor_model.selected_executor(exec_index)
        )

        executor_params: Dict[str, SupportedExecutionRunConfiguration] = {}
        extensions: Set[str] = set({})
        contexts: Dict[str, List[str]] = {}

        conf_indices = (
            self.plugin_container.executor_model.executor_configurations
        )

        for _input in available_inputs:
            extension, context = _input
            extensions |= {extension}
            ext_contexts = contexts.get(extension, [])
            ext_contexts.append(context)
            contexts[extension] = ext_contexts

            executors = conf_indices[_input]
            conf = executors[executor_name]
            executor_params[_input] = conf

        contexts = {
            ext: move_file_to_front(ctx) for ext, ctx in contexts.items()
        }

        # Localized version of the executor
        executor_loc_name = self.main.get_plugin(executor_name).get_name()

        return (
            list(sorted(extensions)),
            contexts,
            executor_loc_name,
            executor_params
        )

    def create_new_configuration(self):
        self.params_table.show_editor(new=True)

    def clone_configuration(self):
        self.params_table.clone_configuration()
        self.edit_configuration_btn.setEnabled(False)

    def delete_configuration(self):
        executor_name, _ = self.executor_model.selected_executor(
            self.previous_executor_index
        )
        index = self.params_table.currentIndex().row()
        conf_index = self.table_model.get_tuple_index(index)

        executor_params = self.all_executor_model[executor_name]
        executor_params.pop(conf_index, None)

        if executor_name not in self._params_to_delete:
            self._params_to_delete[executor_name] = []
        self._params_to_delete[executor_name].append(conf_index)

        self.table_model.set_parameters(executor_params)
        self.table_model.reset_model()
        self.set_modified(True)
        self.set_clone_delete_btn_status()
        self.edit_configuration_btn.setEnabled(False)

    def reset_changes(self):
        """Reset changes to the parameters loaded when the page was created."""
        self.all_executor_model = deepcopy(self.default_executor_conf_params)
        executor_name, _ = self.executor_model.selected_executor(
            self.previous_executor_index
        )
        executor_params = self.all_executor_model[executor_name]
        self.table_model.set_parameters(executor_params)
        self.table_model.reset_model()
        self.set_modified(True)
        self.set_clone_delete_btn_status()

    def apply_settings(self):
        prev_executor_info = self.table_model.get_current_view()
        previous_executor_name, _ = self.executor_model.selected_executor(
            self.previous_executor_index
        )
        self.all_executor_model[previous_executor_name] = prev_executor_info

        # Save new parameters
        for executor in self.all_executor_model:
            executor_params = self.all_executor_model[executor]
            stored_execution_params: Dict[
                Tuple[str, str],
                Dict[str, ExtendedRunExecutionParameters]] = {}

            for key in executor_params:
                (extension, context, params_id) = key
                params = executor_params[key]
                ext_ctx_list = stored_execution_params.get(
                    (extension, context), {})
                ext_ctx_list[params_id] = params
                stored_execution_params[(extension, context)] = ext_ctx_list

            for extension, context in stored_execution_params:
                ext_ctx_list = stored_execution_params[(extension, context)]
                self.plugin_container.set_executor_configuration_parameters(
                    executor, extension, context, {'params': ext_ctx_list}
                )

        # Delete removed parameters
        for executor in self._params_to_delete:
            executor_params_to_delete = self._params_to_delete[executor]

            for key in executor_params_to_delete:
                (extension, context, params_id) = key
                self.plugin_container.delete_executor_configuration_parameters(
                    executor, extension, context, params_id
                )

        self._params_to_delete = {}

        return {'parameters'}
