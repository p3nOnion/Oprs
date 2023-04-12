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
password = "admin"
# SSHConnection(path=path)  # UnixSocketConnection(path=path)
connection = gvm.connections.UnixSocketConnection(path=path)
with Gmp(connection=connection) as gmp:
    def get_version():
        gmp.authenticate(username, password)
        return gmp.get_version()
    def get_tasks():
        gmp.authenticate(username, password)
        response = gmp.get_tasks()
        return response
    def get_task(id):
        gmp.authenticate(username, password)
        response = gmp.get_task(task_id=id)
        return response
    def get_results():
        gmp.authenticate(username, password)
        response = gmp.get_results()
        return response
    def get_result(id):
        gmp.authenticate(username, password)
        response = gmp.get_result(result_id=id)
        return response