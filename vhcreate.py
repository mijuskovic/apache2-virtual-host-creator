#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File:       vhcreate.py
Author:     Nikola Mijuskovic
Date:       2/15/2018
Desc:       Script creates configuration file, document root and simple index.html file for apache2 virtual host,
            and adds domain to hosts file. Script works for Debian based linux distributions.
Version:    0.2-beta
Python:     2.7
"""

import os
import sys
import argparse
import re
import grp

APACHE2_SITES_AVAILABLE_DIR = '/etc/apache2/sites-available/'

VHOST_ROOT_DIR = '/var/www/'

HOSTS = '/etc/hosts'


def create_conf(domain, document_root_public, server_admin="webmaster@localhost",
                a2sites_avail=APACHE2_SITES_AVAILABLE_DIR):
    """Creates domain.conf file in apache2 sites available directory,
     enables that virtual host, and restarts apache2 service"""
    conf_filename = domain + ".conf"

    conf_path = os.path.join(a2sites_avail, conf_filename)

    if os.path.exists(conf_path):
        print('Configuration file ' + conf_path + 'already exists! Do you want to override it?')
        ans = raw_input('(y/n): ')
        if ans != 'y':
            print('File ' + conf_path + ' is not modified!')
            return False
        else:
            print('Overriding configuration file ' + conf_path)

    srvadm = '\tServerAdmin\t' + server_admin

    docroot = '\tDocumentRoot\t' + document_root_public

    srvname = '\tServerName\t' + domain

    srvalias = '\tServerAlias\twww.' + domain

    config = ['<VirtualHost *:80>',
              '',
              srvadm, docroot, srvname, srvalias,
              "\tErrorLog  ${APACHE_LOG_DIR}/error.log",
              "\tCustomLog ${APACHE_LOG_DIR}/access.log combined",
              "",
              " </VirtualHost>"]

    conf = open(conf_path, 'w')

    for line in config:
        print >> conf, line

    conf.close()

    print('Configuration file' + conf_path + 'has been successfully created.')

    print('Enabling site ' + conf_filename)
    os.system('a2ensite ' + conf_filename)
    print('Site ' + conf_filename + ' is enabled.')

    print('service apache2 reload')
    os.system('service apache2 reload')
    print('Service apache2 has been successfully reloaded.')

    return True


def create_directory(document_root_public):
    """Creates document root directory if it does not exist."""
    if not os.path.exists(document_root_public):
        os.makedirs(document_root_public)
        print('Document root ' + document_root_public + ' has been successfully created!')
    else:
        print('Document root ' + document_root_public + ' already exists!')


def create_index_file(domain, document_root_public):
    """Creates index.html file in document root directory"""
    index_path = os.path.join(document_root_public, 'index.html')

    if os.path.exists(index_path):
        print('File ' + index_path + 'already exists! Do you want to override it?')
        ans = raw_input('(y/n): ')
        if ans != 'y':
            print('File ' + index_path + ' is not modified!')
            return False
        else:
            print('Overriding index.html file ' + index_path)

    content = """
<!DOCTYPE html>
<html>
    <head>
    <title>""" + domain.split('.')[0] + """</title>
    </head>
    <body>

    <h1>""" + domain + """</h1>
    <p>""" + domain.split('.')[0] + """ virtual host is working!</p>

    </body>
</html>"""

    index = open(index_path, 'w')

    index.write(content)

    index.close()
    print('File ' + index_path + ' has been successfully created.')

    return True


def add_host_to_hosts_file(domain, ip='127.0.0.1', hosts_file=HOSTS):
    """Adds specified ip address and domain to hosts file"""
    if domain in open(hosts_file).read():
        print(domain + " already exists in hosts file!")
    else:
        virtual_host = ip + '\t' + domain

        with open(hosts_file, 'r') as original:
            data = original.read()
        with file(hosts_file, 'w') as modified:
            modified.write(virtual_host + '\n' + data)

        print('Domain ' + domain + ' has been successfully added to hosts file!')


def chown_and_chmod(document_root, user):
    """Changes recursively owner user and owner group of document root"""
    group = grp.getgrnam('www-data')
    group_mem = group[3]
    if user in group_mem:
        os.system('chown -R ' + user + ':www-data ' + document_root)
    else:
        os.system('chown -R www-data:www-data ' + document_root)
    os.system('chmod -R 775 ' + document_root)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='vhcreate')

    parser.add_argument('domain', type=str, help='specify domain name for virtual host, e.g. project.development')

    # todo: delete virtual hosts which are assigned to specified domain
    # parser.add_argument('-d', '--delete',
    # action='store_true', help='delete virtual host for specified domain if exists')

    parser.add_argument('--ip', type=str, help='custom ip address to be added to hosts file for specified domain name,'
                                               ' default "127.0.0.1"')

    parser.add_argument('--admin', type=str, help='custom server admin e-mail address, default webmaster@localhost')

    parser.add_argument('--docroot', type=str, help='custom document root, default /var/www/project/public')

    args = parser.parse_args()

    if os.geteuid() != 0:
        print('You must have root privileges to do that! Running sudo...')
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        os.execlpe('sudo', *args)

    u = os.system('whoami')

    dom = args.domain

    if args.docroot is not None:
        temp = args.docroot
        while not os.path.isdir(temp):
            print('Specified directory path not exists! Try again:')
            temp = raw_input("Document root path: ")
        doc_root = temp

    else:

        doc_root = os.path.join('/var/www/', dom.split('.')[0])

    doc_root_public = os.path.join(doc_root, 'public')

    if args.admin is not None:
        create_conf(dom, doc_root_public, args.admin)
    else:
        create_conf(dom, doc_root_public)

    create_directory(doc_root_public)

    create_index_file(dom, doc_root_public)

    chown_and_chmod(doc_root, u)

    ip = args.ip

    if ip is not None:
        while not re.match(r"\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b", ip):
            print('Given ip is not valid. Try again!')
            ip = raw_input("ipv4 address: ")

        add_host_to_hosts_file(dom, args.ip)
    else:
        add_host_to_hosts_file(dom)
