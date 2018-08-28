# -*- coding: utf-8 -*-
from __future__ import absolute_import
# -*- coding: utf-8 -*-
from . import popgis_util
"""
/***************************************************************************
 PopGISDialog
                                 A QGIS plugin
 QGIS Plugin Integration with SPC PopGIS
                             -------------------
        begin                : 2017-07-18
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Sachindra Singh
        email                : sachindras@spc.int
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

import os

from qgis.PyQt import QtGui, uic
from qgis.PyQt.QtWidgets import *
from qgis.PyQt import *

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'popgis_dialog_base.ui'))

#pyrcc5 -o resources.py resources.qrc

class PopGISDialog(QDialog, FORM_CLASS):

    popgis = popgis_util.PopGISUtil()

    #debug
    def debug(self, text):
        QMessageBox.about(self, "PopGIS Message", text)

    def error(self, text):
        QMessageBox.critical(self, "PopGIS Warning", text)

    def fullreset(self):
        self.frameworkComboBox.clear()
        self.datasetsComboBox.clear()
        self.dataComboBox.clear()
        self.frameworkComboBox.addItem("---")
        self.datasetsComboBox.addItem("---")
        self.dataComboBox.addItem("---")
        self.countryComboBox.setCurrentIndex(0)

    def reset(self):
        self.frameworkComboBox.clear()
        self.datasetsComboBox.clear()
        self.dataComboBox.clear()
        self.frameworkComboBox.addItem("---")
        self.datasetsComboBox.addItem("---")
        self.dataComboBox.addItem("---")



    def __init__(self, parent=None):
        """Constructor."""
        super(PopGISDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)


        self.countryComboBox.addItem("---")
        self.reset()
        self.countryComboBox.addItems(self.popgis.countries)

        #event handlers
        self.countryComboBox.currentIndexChanged.connect(self.countryChange)
        self.frameworkComboBox.currentIndexChanged.connect(self.frameworkChange)
        self.datasetsComboBox.currentIndexChanged.connect(self.datasetsChange)

        self.buttons.button(QDialogButtonBox.Reset).clicked.connect(self.fullreset)
        self.buttons.button(QDialogButtonBox.Help).clicked.connect(self.help)
        #self.buttons.button(QDialogButtonBox.Apply).clicked.connect(self.apply)

    def help(self):
        self.debug("OGC Table Joining Service Integration with SPC PopGIS Instances.")

    def countryChange(self, i):
        country = self.countryComboBox.itemText(i)
        #self.debug(country)
        self.reset()
        if i > 0:
            dict = self.popgis.get_frameworks(country)
            self.frameworkComboBox.addItems(list(dict.keys()))

    def frameworkChange(self, i):
        framework = self.frameworkComboBox.itemText(i)
        # self.debug(country)
        #self.reset()
        self.datasetsComboBox.clear()
        self.dataComboBox.clear()
        self.datasetsComboBox.addItem("---")
        self.dataComboBox.addItem("---")
        if i > 0:
            dict = self.popgis.get_datasets(framework)
            l = list(dict.keys())
            l.sort()
            self.datasetsComboBox.addItems(l)

    def datasetsChange(self, i):
        datasets = self.datasetsComboBox.itemText(i)
        self.dataComboBox.clear()
        self.dataComboBox.addItem("---")
        if i > 0:
            dict = self.popgis.get_data(datasets)
            l = list(dict.keys())
            l.sort()
            self.dataComboBox.addItems(l)



