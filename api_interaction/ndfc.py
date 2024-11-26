#!/usr/bin/env python3

import json
import logging
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

LOG = logging.getLogger("__name__")

class Ndfc(object):
    """
    Master Class for NDFC API
    """

    def __init__(self, address:str, credentials:dict=None, api_key:dict=None):
        """Initialises an NDFC API object

        Args:
            address (str): IP Address or FQDN
            credentials (dict, optional): dictionay {"userName":"","userPasswd":"","domain":""}
            api_key (dict, optional): A string to authorize all the API calls. Can be generated from the NDI Web UI
            
        """
        
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        LOG.info("A new NDFC Instance is being started")
        # Attribute initialization
        self._address = address
        self._url = "https://%s//appcenter/cisco/ndfc/api/v1/lan-fabric/rest/" % address
        self._token = None
        self._credentials = credentials
        if api_key:
            # API KEY TAKES PRECEDENCE
            LOG.info("Setting API Key")
            self.token = {"X-Nd-Apikey": api_key["api_key"], "X-Nd-Username": api_key["username"]}
            self.cookie = None
        elif credentials:
            # credentials = {'userName': 'XXX', 'userPasswd': 'XXX', 'domain': 'DefaultAuth'}
            LOG.info("Attempting NDI Auth with credentials")
            self.token = None
            self.get_nd_token(self.credentials)

    def __str__():
        return "This is an NDFC object"

    @property
    def address(self):
        """Get credentials"""
        return self._address

    @address.setter
    def address(self, value):
        """Set the credentials"""
        self._address = value

    @property
    def credentials(self):
        """Get credentials"""
        return self._credentials

    @credentials.setter
    def credentials(self, value):
        """Set the credentials"""
        self._credentials = value

    @property
    def cookie(self):
        """Get cookie"""
        return self._cookie

    @cookie.setter
    def cookie(self, value):
        """Set the cookie"""
        self._cookie = value

    @property
    def token(self):
        """Get token"""
        return self._token

    @token.setter
    def token(self, value):
        """Set the token"""
        self._token = value

    @property
    def url(self):
        """Get url"""
        return self._url

    @url.setter
    def url(self, value):
        """Set the url"""
        self._url = value

    def get_nd_token(self, credentials):
        """
        To be used in case you want to authenticate with user credentials. Token received will be
        used as cookie. No Cookie refresh yet.
        TODO: Add Cookie refresh feature
        :param credentials:
        :return:  Bool()
        """
        auth_url = "https://%s/login" % self.address
        LOG.debug(f"Running Auth query at {auth_url}")
        auth_result = requests.post(auth_url, json=credentials, verify=False)

        if auth_result.status_code == 200:
            self.cookie = {"AuthCookie": auth_result.json()["jwttoken"]}
            LOG.info(f"Authentication succeded")
        else:
            LOG.error(f"Authentication failed, {auth_result.status_code}, {auth_result.text}")
            return  False
        return True

    def generic_get(self, uri_object):
        """
        Get any data
        """
        url = "%s/%s" % (self.url, uri_object)
        LOG.debug(f"GET URL:{url}")
        result = requests.get(url, verify=False, cookies=self.cookie, headers=self.token)
        if 199 < result.status_code < 300:
            LOG.debug(f"GET to {url} completed")
            return True, result.json()
        else:
            LOG.error(f"GET failed, {result.status_code}, {result.text}")
            return False, ""

    def generic_post(self, uri_object, payload=None, files=None):
        """
        Get any data
        """
        url = "%s/%s" % (self.url, uri_object)
        LOG.debug(f"POST URL:{url}")
        result = requests.post(url, verify=False, cookies=self.cookie, headers=self.token, json=payload, files=files)
        if 199 < result.status_code < 300:
            LOG.debug(f"POST to {url} completed")
            return True, result.json()
        else:
            LOG.error(f"POST failed, {result.status_code}, {result.text}")
            return False, ""
    
    def generic_put(self, uri_object, payload=None, files=None):
        """
        PUT API Call
        """
        url = "%s/%s" % (self.url, uri_object)
        LOG.debug(f"PUT URL:{url}")
        result = requests.put(url, verify=False, cookies=self.cookie, headers=self.token, json=payload, files=files)
        if 199 < result.status_code < 300:
            LOG.debug(f"PUT to {url} completed")
            return True, result.json()
        else:
            LOG.error(f"POST failed, {result.status_code}, {result.text}")
            return False, ""

    def generic_delete(self, uri_object):
        """
        :param uri_object:
        :param ig_name:
        :return:
        """
        url = "%s/%s" % (self.url, uri_object)
        LOG.debug(f"DELETE URL:{url}")
        result = requests.delete(url, verify=False, cookies=self.cookie, headers=self.token)
        if 199 < result.status_code < 300:
            LOG.debug(f"DELETE to {url} completed")
            return True, result.json()
        else:
            LOG.error(f"DELETE failed, {result.status_code}, {result.text}")
            return False, ""

    def get_all_the_fabrics(self):
        """
        
        """
        url = "control/fabrics"
        result,data = self.generic_get(url)
        if not result:
            return False
        else:
            return(data)

    def get_all_the_devices(self, fabric):
        """
        
        """
        url = f"control/fabrics/{fabric}/inventory/switchesByFabric"
        result,data = self.generic_get(url)
        if not result:
            return False
        else:
            return(data)
    
    def get_device_missing_configs(self, fabric, device=None):
        """
        
        """
        url = f"control/fabrics/{fabric}/pendingConfig/{device}"
        result,data = self.generic_get(url)
        if not result:
            return False
        else:
            return(data)
    
    def force_calculate_device_diff(self, fabric, devices):
        """
        
        """
        url = f"control/fabrics/{fabric}/config-preview/{devices}?forceShowRun=true&showBrief=false&recomputeMapEnable=false&shRunOptimization=true"
        result,data = self.generic_get(url)
        if not result:
            return False
        else:
            return(data)