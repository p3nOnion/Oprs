import xmltodict
from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import Gmp
from gvm.protocols.latest import Osp
import json
import xml.etree.ElementTree as ET
import gvm
from bs4 import BeautifulSoup
path = '/run/gvmd/gvmd.sock'
username = "admin"
password = "71639dc5-2418-4a6c-8cb3-31a621623aa2"
# SSHConnection(path=path)  # UnixSocketConnection(path=path)
connection = gvm.connections.UnixSocketConnection(path=path)
with Gmp(connection=connection) as gmp:

    # print(gmp.get_version())

    gmp.authenticate(username, password)
    

    response = gmp.get_results()

   

    
   
    targets_1 = []

    for item in targets_dicts['get_targets_response']['target']:
        
        print(item['@id'])

    # print(response)

    print(targets_dicts['get_targets_response']['target'])

    # print(targets)

def getTargetList(gmp):
    targets = gmp.get_targets()
    targets_dicts = xmltodict.parse(targets)

    results = []

    for item in targets_dicts[]








    