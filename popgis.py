# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PopGIS
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
from PyQt4.QtGui import *
from PyQt4.QtCore import QVariant
from qgis.core import *
import qgis.utils
from decimal import Decimal

# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from popgis_dialog import PopGISDialog
import os.path


class PopGIS:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'PopGIS_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&SPC PopGIS')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'PopGIS')
        self.toolbar.setObjectName(u'PopGIS')



    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('PopGIS', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = PopGISDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        # apply callback
        self.dlg.buttons.button(QDialogButtonBox.Apply).clicked.connect(self.apply)
        self.dlg.buttons.button(QDialogButtonBox.Help).clicked.connect(self.help)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/PopGIS/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'PopGIS'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&SPC PopGIS'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass


    def apply(self):
        #validation of comboboxes
        valid = True
        if self.dlg.countryComboBox.currentIndex() == 0: valid = False
        if self.dlg.frameworkComboBox.currentIndex() == 0: valid = False
        if self.dlg.datasetsComboBox.currentIndex() == 0: valid = False
        if self.dlg.dataComboBox.currentIndex() == 0: valid = False
        if not valid:
            self.dlg.error("Select All Variables Before Generating Map Data!")

        #rename data/country folder to frameworks eg: province, enumaration_area etc
        #load data/country/framework layer into workshop (no reload, reduplication)
        if valid:
            #self.debug("Processing...")
            country = self.dlg.countryComboBox.itemText(self.dlg.countryComboBox.currentIndex())
            framework = self.dlg.frameworkComboBox.itemText(self.dlg.frameworkComboBox.currentIndex())
            datasets = self.dlg.datasetsComboBox.itemText(self.dlg.datasetsComboBox.currentIndex())
            data = self.dlg.dataComboBox.itemText(self.dlg.dataComboBox.currentIndex())

            f = framework
            if "school" in f.lower():
                f = "school"

            for dl in self.dlg.popgis.data_layers:
                if dl.startswith(country.lower() + "/" + f.lower().replace(" ", "_")):
                    path = os.path.dirname(os.path.abspath(__file__)) + "/data/" + dl
                    #self.dlg.debug(path)
                    layer = self.iface.addVectorLayer(path, country + "_" + framework.replace(" ", "_"), "ogr")
                    layer.setLayerName(country + "_" + framework.replace(" ", "_") + "_" + data.replace(".", "").replace(" - ", "_").replace(" ", "_"))
                    if not layer:
                        self.dlg.error("Data Not Available!")

                    #self.dlg.hide()

                    # get_values (k,v) and overlay/join with loaded layer
                    # dynamic styling - naming, incremental classification
                    dict = self.dlg.popgis.get_values(data)
                    #self.dlg.debug(str(dict))

                    #add value attribute if doesn't exist
                    if layer.dataProvider().fieldNameIndex("value") == -1:
                        res = layer.dataProvider().addAttributes([QgsField("value", QVariant.Double)])
                        layer.updateFields()


                    index_attr = layer.pendingFields()[0].name()
                    #self.dlg.debug(str(index_attr))
                    layer.startEditing()

                    for feature in layer.getFeatures():
                        fid = feature.id()
                        rid = feature[0]
                        val = float(dict[rid])
                        res = layer.changeAttributeValue(fid, layer.dataProvider().fieldNameIndex("value"), val)
                        if res is False:
                            self.dlg.debug(str(res) + " = " + rid + " : " + str(val) + " -> " + str(type(val)) + ", " + str(fid) + ", " + str(layer.dataProvider().fieldNameIndex("value")))
                        #layer.updateFeature(feature) //breaks

                    layer.commitChanges()

                    #projection
                    crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
                    if country == "Fiji":
                        crs = QgsCoordinateReferenceSystem(3460, QgsCoordinateReferenceSystem.EpsgCrsId)
                    self.iface.mapCanvas().mapRenderer().setDestinationCrs(crs)
                    self.iface.mapCanvas().setExtent(layer.extent())

                    styling = True
                    if styling:
                        #label
                        palyr = QgsPalLayerSettings()
                        palyr.readFromLayer(layer)
                        palyr.enabled = True  # this works
                        palyr.fieldName = 'value'  # this works
                        palyr.fontSizeInMapUnits = False
                        #palyr.textFont.setPointSize(6)  # results in 4 - seems to be integer only
                        #palyr.textColor = QColor(0, 0, 0)  # this works
                        palyr.writeToLayer(layer)

                        #style
                        renderer = QgsGraduatedSymbolRendererV2()
                        renderer.setClassAttribute("value")
                        renderer.setMode(QgsGraduatedSymbolRendererV2.EqualInterval)
                        renderer.updateClasses(layer, QgsGraduatedSymbolRendererV2.EqualInterval, len(dict))
                        style = QgsStyleV2().defaultStyle()
                        defaultColorRampNames = style.colorRampNames()
                        ramp = style.colorRamp(defaultColorRampNames[0])
                        renderer.updateColorRamp(ramp)
                        layer.setRendererV2(renderer)
                        #if self.iface.mapCanvas().isCachingEnabled():
                        #    layer.setCacheImage(None)
                        #else:
                        #    self.iface.mapCanvas().refresh()
                        #layer.triggerRepaint()

                    #finish
                    self.dlg.debug("Map Generated.")





    def help(self):
        layer = self.iface.addVectorLayer("/home/sachin/.qgis2/python/plugins/PopGIS/data/fiji/province/pid32760_geoclip.shp", "fiji", "ogr")
        if not layer:
            self.dlg.error("Data Not Available!")
