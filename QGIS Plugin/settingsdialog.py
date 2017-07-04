# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ProjectSelectorDialog
                                 A QGIS plugin
 Tool for selecting pre-defined QGIS projects.
                             -------------------
        begin                : 2013-12-04
        copyright            : (C) 2013 by Dartmoor National Park Authority
        email                : gi@dartmoor.gov.uk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4 import QtCore, QtGui
from ui_settings import Ui_Dialog
# create the dialog for zoom to point

import os

PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULTS = os.path.join(PARENT_DIR, 'defaults.txt')


class SettingsDialog(QtGui.QDialog):

    def __init__(self):
        
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.settings = QtCore.QSettings()

        # Populate the values
        with open(DEFAULTS) as paths:
            projects = paths.readline().strip().split(':', 1)[-1]
            templates = paths.readline().strip().split(':', 1)[-1]
            self.ui.projectsFolderLineEdit.setText(projects)
            self.ui.templateRootLineEdit.setText(templates)

    def browseForProjectRoot(self):
        startingDir = str(self.settings.value("MoorTools/ProjectSelector/projectRoot", os.path.expanduser("~"), type=str))
        d = str(QtGui.QFileDialog.getExistingDirectory(None, 'Select Projects Folder', startingDir))
        if d != os.sep and d.lower() != 'c:\\' and d != '':
            self.ui.projectsFolderLineEdit.setText(d)

    def browseForTemplateRoot(self):
        startingDir = str(self.settings.value("MoorTools/TemplateSelector/templateRoot", os.path.expanduser("~"), type=str))
        d = str(QtGui.QFileDialog.getExistingDirectory(None, 'Select Root of Template Folder Structure', startingDir))
        if d != os.sep and d.lower() != 'c:\\' and d != '':
            self.ui.templateRootLineEdit.setText(d)

    def accept(self):
        projects = self.ui.projectsFolderLineEdit.text()
        self.settings.setValue("MoorTools/ProjectSelector/projectRoot", projects)
        templates = self.ui.templateRootLineEdit.text()
        self.settings.setValue("MoorTools/TemplateSelector/templateRoot", templates)
        with open(DEFAULTS, 'w') as paths:
            paths.write('projects:{}\n'.format(projects))
            paths.write('templates:{}\n'.format(templates))
        QtGui.QDialog.accept(self)
