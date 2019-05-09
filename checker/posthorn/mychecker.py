from ctf_gameserver.checker import BaseChecker, OK, NOTFOUND, NOTWORKING

import os
import random
import binascii
import subprocess
import pprint

import requests

from .utils import generate_message


class Username:
    def __init__(self):
        first = random.choice(['John',
                               'Jane',
                               'Alice',
                               'Bob',
                               'Carol',
                               'Dave',
                               'Eve'
            ])
        second = random.choice(['Doe',
                                'Duck'
            ])
        nonce = binascii.hexlify(os.urandom(4)).decode()

        self._name = "%s-%s-%s" % (first, second, nonce)


    def __str__(self):
        return self._name



class Password:
    def __init__(self):
        self._password = binascii.hexlify(os.urandom(16)).decode()


    def __str__(self):
        return self._password



class PosthornChecker(BaseChecker):
    def __init__(self, tick, team, service, ip):
        BaseChecker.__init__(self, tick, team, service, ip)
        self._baseurl = 'http://%s:5001/' % ip


    def place_flag(self):
        session = requests.session()

        session.get(self._baseurl + 'index.cgi')
        session.get(self._baseurl + 'index.cgi?page=register')
        username, password = self._register(session)
        self._login(session, username, password)

        self.store_yaml(str(self.tick), {'username': str(username), 'password': str(password)})
        self.store_blob('flagid_%03d' % self.tick, str(username).encode())

        flag = self.get_flag(self.tick)
        session.get(self._baseurl + 'index.cgi')
        self._post(session, flag)

        return OK


    def check_flag(self, tick):
        session = requests.session()
        session.get(self._baseurl + 'index.cgi')

        data = self.retrieve_yaml(str(tick))
        flag = self.get_flag(tick)
        if data is None:
            return NOTFOUND
        self._login(session, data['username'], data['password'])

        r = session.get(self._baseurl + 'index.cgi')
        s = subprocess.Popen(['pdftotext', '-', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        s.stdin.write(r.content)
        s.stdin.close()
        lines = [ i.strip().decode() for i in s.stdout.readlines() ]

        if flag in lines:
            return OK
        else:
            return NOTFOUND


    def check_service(self):
        session = requests.session()
        r = session.get(self._baseurl + 'index.cgi')
        if not b'/Producer(GPL Ghostscript 9.26)' in r.content:
            return NOTWORKING

        # left user
        session = requests.session()
        session.get(self._baseurl + 'index.cgi')
        session.get(self._baseurl + 'index.cgi?page=register')
        username, password = self._register(session)

        # right user
        session = requests.session()
        session.get(self._baseurl + 'index.cgi')
        session.get(self._baseurl + 'index.cgi?page=register')
        username2, password2 = self._register(session)

        self._login(session, username2, password2)
        session.get(self._baseurl + 'index.cgi')
        flag = generate_message()
        self.logger.info("Using message >>>%s<<< from %s to %s", flag, username2, username)
        self._post(session, str(flag), receiver=[str(username)])

        session = requests.session()
        session.get(self._baseurl + 'index.cgi')
        self._login(session, username, password)

        r = session.get(self._baseurl + 'index.cgi')
        s = subprocess.Popen(['pdftotext', '-', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        s.stdin.write(r.content)
        s.stdin.close()
        lines = [ i.strip().decode() for i in s.stdout.readlines() ]

        if flag[:65] in [ i[:65] for i in lines]:
            return OK
        else:
            self.logger.warn("Was looking for >>%s<< but only got >>%s<<", flag[:70], [ i[:70] for i in lines])
            return NOTWORKING

        return OK


    def _post(self, session, post, receiver=[]):
        with open(os.path.join(os.path.dirname(__file__), 'post.fdf'), 'r') as fdf:
            template = fdf.read()
            fdfdata = template.format(host=self._ip, post=post, receiver=','.join(receiver))
            self.logger.debug("Posting >>%s<< to users >>%s<<", post, receiver)
            session.post('http://%s:5001/post.cgi' % self._ip, data=fdfdata)


    def _register(self, session):
        with open(os.path.join(os.path.dirname(__file__), 'login.fdf'), 'r') as fdf:
            template = fdf.read()
            username = Username()
            password = Password()
            fdfdata = template.format(host=self._ip, username=username, password=password)
            self.logger.debug("Registering user >>%s<< password >>%s<<", str(username), str(password))
            session.post('http://%s:5001/register.cgi' % self._ip, data=fdfdata)
            return username, password


    def _login(self, session, username, password):
        with open(os.path.join(os.path.dirname(__file__), 'login.fdf'), 'r') as fdf:
            template = fdf.read()
            fdfdata = template.format(host=self._ip, username=username, password=password)
            self.logger.debug("Logging in as user >>%s<< password >>%s<<", str(username), str(password))
            session.post('http://%s:5001/login.cgi' % self._ip, data=fdfdata)
