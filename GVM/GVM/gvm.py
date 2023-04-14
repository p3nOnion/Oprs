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
    def get_version():
        gmp.authenticate(username, password)
        return gmp.get_version()

    def get_targets():
        gmp.authenticate(username, password)
        response = gmp.get_targets()
        return response

    def get_target(id):
        gmp.authenticate(username, password)
        response = gmp.get_target(id=id)
        return response

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

    def get_reports():
        gmp.authenticate(username, password)
        response = gmp.get_reports()
        return response

    def get_report(id):
        gmp.authenticate(username, password)
        response = gmp.get_report(
            report_id=id, filter_string="apply_overrides=0 levels=hml rows=100 min_qod=70 first=1 sort-reverse=severity")
        return response

    def get_port_lists():
        gmp.authenticate(username, password)
        response = gmp.get_port_lists()
        return response

    def get_port_list(id):
        gmp.authenticate(username, password)
        response = gmp.get_port_list(id=id)
        return response

    def create_target(name, hosts, comment, port_list_id):
        gmp.authenticate(username, password)
        gmp.create_target(name=name, hosts=hosts,
                          comment=comment, port_list_id=port_list_id)

    def delete_target(id):
        gmp.authenticate(username, password)
        gmp.delete_target(id)
