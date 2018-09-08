from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import object
import urllib.request, urllib.error, urllib.parse
import xml.etree.ElementTree as et
import os

from qgis.core import QgsMessageLog

class PopGISUtil(object):

    domain = "popgis.spc.int/GC_tjs.php"
    countries = ["Cooks","Fiji","FSM","Kiribati","Nauru","Niue","Palau","RMI", "Samoa","Solomons","Tonga","Tuvalu","Vanuatu","WF"]

    shp_download_root = 'https://raw.githubusercontent.com/sopac/popgis-plugin/master/data/'
    shp_friends = ['.cpg','.dbf','.prj','.qpj','.shx','.shp']

    data_layers = []
    data_layers.append("solomons/constituency/cid_3857.shp")
    data_layers.append("solomons/ward/wid_3857.shp")
    data_layers.append("solomons/province/pid_3857.shp")
    data_layers.append("solomons/enumeration_area/eaid_3857.shp")
    data_layers.append("tuvalu/island/buffer15_32760_geoclip.shp")
    data_layers.append("tuvalu/island/isl_bkg_32760_geoclip.shp")
    data_layers.append("tuvalu/split/frame 32760 tuvalu.shp")
    data_layers.append("tuvalu/split/iid2_unscaled_xy.shp")
    data_layers.append("tuvalu/split/eaid2_unscaled_xy.shp")
    data_layers.append("tuvalu/split/vid2_unscaled_xy.shp")
    data_layers.append("tuvalu/village/vil_tuv_32760.shp")
    data_layers.append("tuvalu/enumeration_area/eas_32760_geoclip.shp")
    data_layers.append("fiji/localities/Fiji_localities_32760.shp")
    data_layers.append("fiji/tikina/tid32760_geoclip.shp")
    data_layers.append("fiji/province/pid32760_geoclip.shp")
    data_layers.append("fiji/enumeration_area/eas32760_geoclip.shp")
    data_layers.append("vanuatu/school/School_Loc_Van_3857.shp")
    data_layers.append("vanuatu/island/IID_3857_10_2015.shp")
    data_layers.append("vanuatu/province/PID_3857_10_2015.shp")
    data_layers.append("vanuatu/enumeration_area/EAID99_3857_10_2015.shp")
    data_layers.append("vanuatu/area_council/ACID_3857_10_2015.shp")
    data_layers.append("vanuatu/household_gps_points/GPSpoints_3857.shp") 
    data_layers.append("cooks/enumeration_area/CK_EA_clean_3857_name_xy.shp")
    data_layers.append("cooks/census_district/CK_DS_clean_3857_combine_names_xy.shp")
    data_layers.append("cooks/island/CK_IID_clean_names_xy_buff60_3857.shp")
    data_layers.append("cooks/groups_of_islands/CK_GID_buff100_3857_xy2.shp")
    data_layers.append("wf/village/Final_vill_3857.shp")
    data_layers.append("wf/district/Districts_3857.shp")  
    data_layers.append("fsm/edid_names_xy_3857.shp")
    data_layers.append("fsm/mid_names_xy_3857.shp")
    data_layers.append("fsm/sid_buffer100km_xy.shp")
    data_layers.append("fsm/split_mid_nodrawn_frame.shp")
    data_layers.append("kiribati/enumeration_area/KIR_EA_xy_3857.shp")
    data_layers.append("kiribati/village/KIR_VID_xy_3857.shp")
    data_layers.append("kiribati/island/KIR_IID_xy_3857.shp")
    data_layers.append("nauru/Nau_ea_3857_xy.shp")
    data_layers.append("nauru/Nau_did_3857.shp")
    data_layers.append("palau/EAID clean 3857.shp")
    data_layers.append("palau/HID 3857 Final.shp")
    data_layers.append("palau/SID.shp")
    data_layers.append("tonga/census_block/ton_blk_xy_3857_07_09_2015.shp")
    data_layers.append("tonga/district/ton_ds_xy_3857_1_9_2015.shp")
    data_layers.append("tonga/division/TON_dv_3857.shp")
    data_layers.append("tonga/village/ton_vid_xy_3857_5_4_2016.shp")
    data_layers.append("palau/enumeration_area/EAID clean 3857.shp")
    data_layers.append("palau/hamlet/HID 3857 Final.shp")
    data_layers.append("palau/state/SID.shp")
    data_layers.append("rmi/atoll/aid_3857.shp")
    data_layers.append("rmi/enumeration_area/eaid_3857.shp")
    
    frameworks = {}
    datasets = {}
    data = {}
    values = {}

    #describeframeworks
    def get_frameworks(self, country):
        res = {}
        request = urllib.request.Request('http://' + country.lower() + '.' + self.domain + '?SERVICE=TJS&REQUEST=DescribeFrameworks&AcceptVersions=1.0.0',headers={'User-Agent': 'Mozilla/5.0'})
        xml = urllib.request.urlopen(request, timeout = 1000).read()
        root = et.XML(xml)
        for child in root:
            title = ""
            url = ""
            for c in child:
                if c.tag.endswith("Title"):
                    #print c.text
                    title = c.text
                if c.tag.endswith("DescribeDatasetsRequest"):
                    #print c.attrib.values()[0]
                    url = list(c.attrib.values())[0]
            if title is not "" and url is not "":
                res[title] = url
        self.frameworks = res
        return res


    #describedatasets
    def get_datasets(self, framework):
        res = {}
        url = self.frameworks.get(framework)
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        xml = urllib.request.urlopen(request, timeout = 1000).read()
        root = et.XML(xml)
        for child in root:
            for c1 in child:
                title = ""
                url = ""
                for c in c1:
                    if c.tag.endswith("Title"):
                        # print c.text
                        title = c.text
                    if c.tag.endswith("DescribeDataRequest"):
                        # print c.attrib.values()[0]
                        url = list(c.attrib.values())[0]
                if title is not "" and url is not "":
                    res[title] = url
        self.datasets = res
        return res

    #describedata
    def get_data(self, dataset):
        res = {}
        url = self.datasets.get(dataset)
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        xml = urllib.request.urlopen(request, timeout = 1000).read()
        root = et.XML(xml)
        title = ""
        url = ""

        for c0 in root:
            for c1 in c0:
                for c2 in c1:
                    for c3 in c2:
                        for c4 in c3:
                            for c in c4:
                                #print c.tag
                                if c.tag.endswith("Title"):
                                    #print c.text
                                    title = c.text
                                if c.tag.endswith("GetDataRequest"):
                                    # print c.attrib.values()[0]
                                    url = list(c.attrib.values())[0]
                            if title is not "" and url is not "":
                                res[title] = url
        self.data = res
        return res


    #getdata
    def get_values(self, data):
        res = {}
        url = self.data.get(data)
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        xml = urllib.request.urlopen(request, timeout = 2000).read()
        root = et.XML(xml)
        k = ""
        v = ""

        for c0 in root:
            for c1 in c0:
                for c2 in c1:
                    for c3 in c2:
                        for c in c3:
                            #print c.tag
                            if c.tag == "K":
                                #print c.text
                                k = c.text
                            if c.tag == "V":
                                #print c.text
                                v = c.text
                        if k is not "" and v is not "":
                            res[k] = v

        self.values = res
        return res


    def download_all_shapefiles(self, layer):
        for layer in self.data_layers:
            self.download_shapefile(layer)

    def download_shapefile(self, layer, force=False):
        """
        This downloads shapefile&friends from the github repository if it doesn't exist already.
        """
        path = os.path.dirname(os.path.abspath(__file__)) + "/data/" + layer

        if not os.path.exists(path) or force:
            QgsMessageLog.logMessage("{} does not exist or redownload forced.".format(layer),"PopGIS")

            # TODO : progress bar or other UI feedback (some files may be relatively big)

            try:
                for ext in self.shp_friends:
                    download_url = self.shp_download_root + os.path.splitext(layer)[0] + ext
                    save_url = os.path.splitext(path)[0] + ext

                    QgsMessageLog.logMessage("Downloading {}...".format(download_url),"PopGIS")

                    os.makedirs( os.path.dirname(save_url), exist_ok=True )
                    urllib.request.urlretrieve(download_url, save_url)

                    QgsMessageLog.logMessage("Saved to {}".format(save_url),"PopGIS")
            except urllib.error.URLError as e:
                QgsMessageLog.logMessage("Download of {} failed. Removing data.".format(download_url),"PopGIS")

                # We delete all files to avoid leaving corrupted data
                for ext in self.shp_friends:
                    save_url = os.path.splitext(path)[0] + ext

                # We still raise the exception
                raise e

        else:
            QgsMessageLog.logMessage("{} already exists. Using cached version.".format(layer),"PopGIS")

        return path


#test
test = False
if test:
    x = PopGISUtil()
    # fix_print_with_import
    # fix_print_with_import
    print(list(x.get_frameworks("Vanuatu").keys()))
    # fix_print_with_import
    # fix_print_with_import
    print(list(x.get_datasets("Province").keys()))
    # fix_print_with_import
    # fix_print_with_import
    print(list(x.get_data("P11. Religion of total population").keys()))
    #print x.get_values("H1. Type of living quarters - Proportion of HH living in one family house attached to one or more houses - 2009 Census")

