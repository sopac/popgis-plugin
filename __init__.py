# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PopGIS
                                 A QGIS plugin
 QGIS Plugin Integration with SPC PopGIS
                             -------------------
        begin                : 2017-07-18
        copyright            : (C) 2017 by Sachindra Singh
        email                : sachindras@spc.int
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load PopGIS class from file PopGIS.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .popgis import PopGIS
    return PopGIS(iface)
