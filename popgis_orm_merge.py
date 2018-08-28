from __future__ import print_function
#Author: Sachindra Singh <sachindras@spc.int>
#Date: 19/08/2017
#ORM - Object Relational Mapper for OGC Table Joining Service Instances

from builtins import str
from pony.orm import *
import sqlite3, os

#delete
#try:
#    os.remove("/home/sachin/.qgis2/python/plugins/PopGIS/popgis.master.sqlite")
#except:
#    pass

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
db.bind(provider='postgres', user='postgres', password='erlang44', host='localhost', database='popgis')
#db.bind(provider='sqlite', filename='popgis.master.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

#merge objects
path = "/home/sachin/"
split_databases = ["popgis.1.sqlite", "popgis.2.sqlite", "popgis.3.sqlite"]


for d in split_databases:
    with db_session:
        #print d
        conn = sqlite3.connect(path + d)
        cursora = conn.cursor()
        cursora.execute("select name, id from country")
        for ra in cursora:
            # fix_print_with_import
            print(ra[0]) #country
            c1 = Country(name=ra[0])
            cid = ra[1]
            commit()
            cursorb = conn.cursor()
            cursorb.execute("select title, id from framework where country=" + str(cid))
            for rb in cursorb:
                f1 = Framework(country=c1, title=rb[0])
                fid = rb[1]
                commit()
                cursorc = conn.cursor()
                cursorc.execute("select title, id from dataset where framework=" + str(fid))
                for rc in cursorc:
                    ds1 = DataSet(framework=f1, title=rc[0])
                    dsid = rc[1]
                    commit()
                    cursord = conn.cursor()
                    cursord.execute("select title, id from data where dataset=" + str(dsid))
                    for rd in cursord:
                        d1 = Data(dataset=ds1, title=rd[0])
                        did = rd[1]
                        commit()
                        #print rb[0] + " : " + rc[0] + " : " + rd[0]
                        cursore = conn.cursor()
                        cursore.execute("select k, v from 'values' where data=" + str(did))
                        for re in cursore:
                            v1 = Values(data=d1, k=re[0], v=re[1])
                            commit()

        conn.close()


# fix_print_with_import
print("DTO Merge Complete.")





