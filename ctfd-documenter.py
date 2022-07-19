#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : ctfd-documenter.py
# Author             : Mucahit Kurtlar (github.com/mucahitkurtlar)
# Date created       : 19 Jul 2022

import argparse
import json
import requests
import re
from mdutils.mdutils import MdUtils

class CTFdDocumenter(object):
    """CTFdDocumenter class"""
    def __init__(self, target, login, password, solved=False):
        super(CTFdDocumenter, self).__init__()
        self.target = target
        self.challenges = {}
        self.credentials = {
            'user': login,
            'password': password
        }
        self.session = requests.Session()
        self.solved = solved

    def login(self):
        """Logs in to target URL"""
        r = self.session.get(self.target + '/login')
        matched = re.search(b"""('csrfNonce':[ \t]+"([a-f0-9A-F]+))""", r.content)
        nonce = ""
        if matched is not None:
            nonce = matched.groups()[1]
        r = self.session.post(
            self.target + '/login',
            data={
                'name': self.credentials['user'],
                'password': self.credentials['password'],
                '_submit': 'Submit',
                'nonce': nonce.decode('UTF-8')
            }
        )
        if r.status_code == 200:
            return True
        else:
            return False


    def get_challenges(self):
        """Fetchs challenges from target URL"""
        r = self.session.get(self.target + "/api/v1/challenges")

        if r.status_code == 200:
            json_challs = json.loads(r.content)
            if json_challs is not None:
                if json_challs['success']:
                    self.challenges = json_challs['data']
                else:
                    print("[warn] An error occurred while requesting /api/v1/challenges")
            return json_challs
        else:
            return None

    def prepare_document(self):
        """Creates Write-up.md file"""
        mdFile = MdUtils(file_name='write-up')
        mdFile.new_header(level=1, title='Write-up')
        mdFile.new_paragraph(f"Author: ``{self.credentials['user']}``")


        for challenge in self.challenges:
            if not self.solved or challenge["solved_by_me"]:
                mdFile.new_header(level=2, title=challenge['name'])
                mdFile.new_paragraph(f"**Category**: {challenge['category']}")
                mdFile.new_paragraph(f"**Points**: {challenge['value']}")
                mdFile.new_paragraph("<!-- Answer Begin -->")
                mdFile.new_paragraph("<!-- Answer End -->")
                mdFile.new_paragraph("**Flag:** ")
                mdFile.new_paragraph("<br>")
                mdFile.new_paragraph()
        mdFile.create_md_file()

        return None


def parseArgs():
    parser = argparse.ArgumentParser(description="CTFd Documenter"
                                     " - A tool to generate a write-up file from CTFd")
    parser.add_argument("-t", "--target", required=True, help="CTFd target (domain or ip)")
    parser.add_argument("-u", "--user", required=True, help="Username to login to target")
    parser.add_argument("-p", "--password", required=True, help="Password to login to target")
    parser.add_argument("-s", "--solved", default=False, action="store_true", help="Only solved challenges. (default: False)")

    return parser.parse_args()


if __name__ == '__main__':
    args = parseArgs()

    if not re.match("^https?://", args.target):
        args.target = "https://" + args.target
    args.target = args.target.rstrip('/')

    cp = CTFdDocumenter(args.target, args.user, args.password, args.solved)
    cp.login()
    cp.get_challenges()
    cp.prepare_document()
