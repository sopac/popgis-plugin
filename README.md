## QGIS Table Joining Service (QGC-TJS) Integration Plugin for SPC PopGIS

###### Prerequiste

Requirement: QGIS 3.2.x 

###### Repository Installation

1. Goto Plugins -> Manage and Install Plugins -> Settings
2. Add Plugin Repository with following paramters:
Name: SPC, URL : http://services.gem.spc.int/plugins/plugins.xml
3. Search for *"SPC PopGIS"*, Install and Enable.

###### Manual Installation *(Alternative)*

1. Download the [latest release](https://github.com/sopac/popgis-plugin/releases) and extract them to your QGIS plugins folder at `$HOME/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
2. *Rename* the extracted folder to `PopGIS`.
3. Launch QGIS and open menu Plugins -> Manage and Install Plugins.
4. Enable *"SPC PopGIS"* plugin in the Plugins dialog.

###### Usage

1. Click on the SPC stars logo to launch the plugin.
2. Select Country, Framework, Datasets and Data before clicking the *Apply* button.

###### Reference

http://www.opengeospatial.org/standards/tjs

http://prism.spc.int/regional-data-and-tools/popgis2

###### Issues
File bugs and issues using GitHub Issues functionality on this repository.

###### Screenshots
![Fiji Example](popgis_plugin_screen_2.png)

![Vanuatu Example](popgis_plugin_screen_1.png)








