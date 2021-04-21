# -*- coding: utf-8 -*-
import argparse
from datetime import datetime
from selenium import webdriver
import json, sys, unittest, urllib.parse, uuid

def get_ts():
    return datetime.strftime(datetime.now(), '%Y.%m.%d %H:%M:%S')

class setup(unittest.TestCase):
    def __init__(
        self
    ):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5) # 5 Seconds
        self.args = self.make_parser()
        self.parameters = self.parameters(self.args.Configurations)

    def make_parser(self):
        parser = argparse.ArgumentParser(
            description='This script will help create a company site on the production server for vendor feed configurations.'
        )
        parser.add_argument('-cn','--CompanyName', help='Name of the site to be created.', required=True)
        parser.add_argument('-cf','--Configurations', help='Configurations JSON, which includes servers and GUIDs (on that server).', required=True)
        parser.add_argument('-fn','--FirstName', help='Default User FirstName', required=False, default='Internal')
        parser.add_argument('-ln','--LastName', help='Default User LastName', required=False, default='Admin')
        return parser.parse_args()

    def tear_down(self):
        self.driver.quit()
        self.parameters._log.close()

    class parameters:
        def __init__(
            self,
            configs
        ):
            self._username = f'USERNAME'
            self._password = f'PASSWORD'
            self._configs = self._get_configurations(configs)
            self._urls = self._make_urls()
            self._login_urls = self._urls[0]
            self._create_urls = self._urls[1]
            self._permission_urls = self._urls[2]
            self._log = self._make_log()

        def _encode_name(self, name):
            return urllib.parse.quote(name)
        
        def _get_configurations(self, configs):
            return json.loads(open(configs, 'r').read())

        def _make_urls(self, login_urls=[], create_urls=[], permission_urls=[]):
            for server in self._configs:
                login_urls.append('https://{0}.production.com/default.aspx'.format(server))
                create_urls.append('https://{0}.production.com/admin.aspx'.format(server))
                for user in self._configs[server]:
                    permission_urls.append('https://{0}.production.com/permit.aspx?GUID={1}'.format(server, user))
            return [login_urls, create_urls, permission_urls]

        def _make_log(self):
            return open('log_{0}.log'.format(datetime.strftime(datetime.now(), '%Y.%m.%d %H%M%S')), 'w')

def test_make_site():
    main = setup()
    driver = main.driver
    params = main.parameters
    args = main.args

    def base_logon(url):
        try:
            driver.get(url)
            driver.find_element_by_name('Username').send_keys(params._username)
            driver.find_element_by_name('Password').send_keys(params._password)
            driver.find_element_by_xpath("//input[@value='Logon']").click()
        except:
            params._log.write('{0} | Issue with logging into {1}\n'.format(
                get_ts(),
                url
            ))

    def create_site(url):
        try:
            params._log.write('{0} | Creating site: {1}\n'.format(
                get_ts(),
                args.CompanyName
            ))
            
            driver.get(url)
            driver.find_element_by_name("CompanyName").send_keys(args.CompanyName)
            driver.find_element_by_name("FirstName").send_keys(args.FirstName)
            driver.find_element_by_name("LastName").send_keys(args.LastName)
            driver.find_element_by_name("EmailAddress").send_keys('{0}@production.com'.format(str(uuid.uuid4())))
            driver.find_element_by_name("submit1").click()
            
            params._log.write('{0} | Site {1} was created.\n'.format(
                get_ts(),
                args.CompanyName
            ))
        except:
            params._log.write('{0} | Unable to create site: {1}\n'.format(
                get_ts(),
                args.CompanyName
            ))

    def give_permissions(url):
        try:
            driver.get(url)
            driver.find_element_by_xpath("//input[@value='Check All']").click()
            driver.find_element_by_name("submit1").click()
        except:
            params._log.write('{0} | Unable to give permissions for: {1}\n'.format(
                get_ts(),
                url
            ))

    params._log.write(
        '{0} | Starting process in creating {1} site(s).\n'.format(
            get_ts(),
            len(params._create_urls)
        )
    )

    for i, _ in enumerate(params._login_urls):
        base_logon(params._login_urls[i])
        create_site(params._create_urls[i])
        for u in params._permission_urls:
            give_permissions(u)

    params._log.write(
        '{0} | Completed creating {1} site(s).\n'.format(
            get_ts(),
            len(params._create_urls)
        )
    )

test_make_site()