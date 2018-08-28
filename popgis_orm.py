from __future__ import print_function
from __future__ import absolute_import
#Author: Sachindra Singh <sachindras@spc.int>
#Date: 19/08/2017
#ORM - Object Relational Mapper for OGC Table Joining Service Instances

from pony.orm import *
from . import popgis_util
import time

db = Database()

class Country(db.Entity):
    name = Required(str)
    frameworks = Set('Framework')

class Framework(db.Entity):
    country = Required(Country)
    title = Required(str)
    datasets = Set('DataSet')

class DataSet(db.Entity):
    framework = Required(Framework)
    title = Required(str)
    data = Set('Data')

class Data(db.Entity):
    dataset = Required(DataSet)
    title = Required(str)
    values = Set('Values')

class Values(db.Entity):
    data = Required(Data)
    k = Required(str)
    v = Required(str)

#binding
#db.bind(provider='postgres', user='sachin', password='', host='localhost', database='popgis_db')
db.bind(provider='sqlite', filename='popgis.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

#transfer objects
sql_debug(False)
tjs = popgis_util.PopGISUtil()

with db_session:
    #countries
    for co in tjs.countries:
        # fix_print_with_import
        print(co)
        c1 = Country(name=co)
        commit()
        #frameworks
        for fr in list(tjs.get_frameworks(co).keys()):
            f1 = Framework(country=c1, title=fr)
            commit()
            #time.sleep(10)
            #datasets
            for ds in list(tjs.get_datasets(fr).keys()):
                ds1 = DataSet(framework=f1, title=ds)
                commit()
                #time.sleep(1)
                #data
                for da1 in list(tjs.get_data(ds).keys()):
                    if da1 is not None:
                        d1 = Data(dataset=ds1, title=da1)
                        try:
                            # fix_print_with_import
                            print(co + ":" + fr + " - " + da1)
                        except:
                            pass
                        commit()
                        #time.sleep(1)
                        #values
                        try:
                            values = tjs.get_values(da1) #xml.etree.ElementTree.ParseError: not well-formed (invalid token): line 1, column 1
                            for val in list(values.keys()):
                                t = values[val]
                                if t is None:
                                    t = "0"
                                v1 = Values(data=d1, k=val, v=t)
                                commit()
                        except:
                            # fix_print_with_import
                            print("ERROR getting values for : " + da1)
                            pass


# fix_print_with_import
print("DTO Complete.")





