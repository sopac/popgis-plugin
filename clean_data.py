from __future__ import print_function

from builtins import str
from builtins import range
import os, sys

for root, subFolders, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith(".shp"):
            path = os.path.join(root, file)
            col = "value"
            print('ogrinfo -sql "ALTER TABLE ' + file.replace(".shp", "") + ' DROP COLUMN ' + col + '" ' + path)
            for i in range(30):
                col = "value_" + str(i + 1)
                print('ogrinfo -sql "ALTER TABLE ' + file.replace(".shp", "") + ' DROP COLUMN ' + col + '" ' + path)


