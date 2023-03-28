from channels.generic.websocket import WebsocketConsumer
from six import StringIO

from Terminal.tools.ssh import SSH
from django.http.request import QueryDict
# from django.utils.six import StringIO
from Opra.settings import TMP_DIR
import os
import json
import base64
import re


class WebSSH(WebsocketConsumer):
    message = {'status': 0, 'message': None}
    """
        trạng thái:
            0: kết nối ssh bình thường, websocket bình thường
            1: Đã xảy ra lỗi không xác định, đóng kết nối ssh và websocket

        tin nhắn:
            Khi trạng thái là 1, thông báo là thông báo lỗi cụ thể
            Khi trạng thái là 0, thông báo là dữ liệu do ssh trả về và trang đầu cuối sẽ lấy dữ liệu do ssh trả về và ghi vào trang đầu cuối
        """

    def connect(self):
        """
        Mở kết nối websocket và thử kết nối với máy chủ ssh thông qua các tham số được truyền từ giao diện người dùng
        :return:
        """
        self.accept()
        query_string = self.scope.get('query_string')
        ssh_args = QueryDict(query_string=query_string, encoding='utf-8')

        width = ssh_args.get('width')
        height = ssh_args.get('height')
        port = ssh_args.get('port')

        width = int(width)
        height = int(height)
        port = int(port)

        auth = ssh_args.get('auth')
        ssh_key_name = ssh_args.get('ssh_key')
        passwd = ssh_args.get('password')

        host = ssh_args.get('host')
        user = ssh_args.get('user')

        if passwd:
            passwd = base64.b64decode(passwd).decode('utf-8')
        else:
            passwd = None

        self.ssh = SSH(websocker=self, message=self.message)

        ssh_connect_dict = {
            'host': host,
            'user': user,
            'port': port,
            'timeout': 30,
            'pty_width': width,
            'pty_height': height,
            'password': passwd
        }

        if auth == 'key':
            ssh_key_file = os.path.join(TMP_DIR, ssh_key_name)
            with open(ssh_key_file, 'r') as f:
                ssh_key = f.read()

            string_io = StringIO()
            string_io.write(ssh_key)
            string_io.flush()
            string_io.seek(0)
            ssh_connect_dict['ssh_key'] = string_io

            os.remove(ssh_key_file)

        self.ssh.connect(**ssh_connect_dict)

    def disconnect(self, close_code):
        try:
            if close_code == 3001:
                pass
            else:
                self.ssh.close()
        except:
            pass
        finally:
            # Các ký tự màu trong kết quả điểm đã lọc
            # res = re.sub('(\[\d{2};\d{2}m|\[0m)', '', self.ssh.res)
            print('命令: ')
            print(self.ssh.cmd)
            # print('result: ')
            # print(res)
            pass

    def receive(self, text_data=None, bytes_data=None):
        if text_data is None:
            self.ssh.django_bytes_to_ssh(bytes_data)
        else:
            data = json.loads(text_data)
            if type(data) == dict:
                status = data['status']
                if status == 0:
                    data = data['data']
                    self.ssh.shell(data)
                else:
                    cols = data['cols']
                    rows = data['rows']
                    self.ssh.resize_pty(cols=cols, rows=rows)
