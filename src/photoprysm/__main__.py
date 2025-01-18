#!/usr/bin/env python3
import cmd
import requests
import argparse
from photoprysm import core
from photoprysm import albums

class PhotoprysmCLI(cmd.Cmd):
    intro = ('Welcome to the Photoprysm CLI. Type \'help\' or \'?\' to list '
             'commands.\n')
    prompt = '(photoprysm) '
    mode: str
    server_api: core.ServerAPI
    user: core.User
    client: core.Client
    session: requests.Session

    # Setup
    def preloop(self):
        # We gotta log in
        if self.mode == 'user':
            self.session = self.user.login(self.server_api)
        else:
            self.session = self.client.login(self.server_api)

    def postloop(self):
        if self.mode == 'user':
            self.user.logout()
        else:
            self.client.logout()

    # Quit
    def do_quit(self, arg):
        '''Log out of the session and exit the Photoprysm shell'''
        print('Goodbye.')
        return True

    # Commands
    def do_status(self, arg):
        '''Get the status of the Photoprism server'''
        resp = core.request(
            session = self.session,
            server_api = self.server_api,
            method = 'GET',
            endpoint = 'status')
        resp.raise_for_status()
        print('Server is '+resp.json()['status'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Photprysm CLI')
    parser.add_argument('host',
                        help = 'Host of the Photoprism server')
    parser.add_argument('port',
                        type = int,
                        help = 'Port where the Photoprism server communicates')
    parser.add_argument('--scheme',
                        default = 'http',
                        help = 'Scheme to send requests with')
    subparsers = parser.add_subparsers(dest = 'mode')
    parser_user = subparsers.add_parser('user',
                                        help = 'Login as user')
    parser_user.add_argument('username',
                             help = 'Username of user account')
    parser_user.add_argument('password',
                             help = 'Password of user account')
    parser_client = subparsers.add_parser('client',
                                          help = 'Login as client')
    parser_client.add_argument('id',
                               help = 'Client ID')
    parser_client.add_argument('secret',
                               help = 'Client secret')
    args = parser.parse_args()
    server_api = core.ServerAPI(
        host = args.host,
        port = args.port,
        scheme = args.scheme)
    commander = PhotoprysmCLI()
    commander.server_api = server_api
    commander.mode = args.mode
    if args.mode == 'user':
        commander.user = core.User(args.username, args.password)
    else:
        commander.client = core.Client(args.id, args.secret)
    commander.cmdloop()
    
