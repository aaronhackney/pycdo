from functools import wraps
from pycdo.helpers import PREFIX_LIST, CDO_REGION, DEVICE_TYPES
from pycdo.errors import DuplicateObjectError
import json
import logging
import requests

logger = logging.getLogger(__name__)


class CDOAPIWrapper(object):
    """This decorator class wraps all API methods of ths client and solves a number of issues. For example, if an
    object already exists when attempting to create an object, raise the custom error 'DuplicateObjectError' and give
    the consumer the opportunity to ignore the error and carry on with other operations in their script.
    """

    def __call__(self, fn):
        @wraps(fn)
        def new_func(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except requests.HTTPError as ex:
                logger.debug(f"CDOAPIWrapper called by {fn.__name__}, but we got an unexpected HTTP response {ex}")
                if ex.response.status_code == 400:
                    error_msg = json.loads(ex.response.text)
                    if error_msg.get("message") == "Duplicate Object":
                        raise DuplicateObjectError
                raise

        return new_func


class CDOBaseClient(object):
    """
    This class is inherited by all CDO classes and is always instantiated and other assets that are needed
    by multiple inherited classes are provided
    """

    def __init__(self, api_token, region, api_version="", verify=""):
        self.base_url = "https://" + CDO_REGION[region]
        self.region = region
        self.http_session = requests.Session()
        self.set_headers(api_token)
        self.verify = verify
        self.api_version = api_version
        self.PREFIX_LIST = PREFIX_LIST
        self.DEVICE_TYPES = DEVICE_TYPES

    def set_headers(self, token):
        """Helper function to set the auth token and accept headers in the API request"""
        if "Authorization" in self.http_session.headers:
            del self.http_session.headers["Authorization"]
        self.http_session.headers["Authorization"] = f"Bearer {token.strip()}"
        self.http_session.headers["Accept"] = "application/json"
        self.http_session.headers["Content-Type"] = "application/json;charset=utf-8"

    @CDOAPIWrapper()
    def get_operation(self, endpoint, params=None, headers="", url=""):
        """
        Get the requested endpoint/resource from the API
        :param endpoint: The path of the resource we are attempting to retrieve
        :param params: Any query parameters that we wish to add to the path
        :param headers: Override the class headers if one presented here
        :param url: Override the class base URL
        :return: dict of the requested data
        """
        if not headers:
            headers = self.http_session.headers
        if url:
            api_response = self.http_session.get(url=url + endpoint, params=params, headers=headers)
        else:
            api_response = self.http_session.get(url=self.base_url + endpoint, params=params, headers=headers)
        api_response.raise_for_status()
        return json.loads(api_response.text)

    @CDOAPIWrapper()
    def post_operation(self, endpoint, json=None, data=None, headers="", url=""):
        """
        Given the project endpoint, create a new object with the given post_data
        :param endpoint: Usually the GUID of the project where we wish to store our new object
        :param data: Data model of the new object with values that we wish to store
        :param json_data: If we are sending json payload (dict), give requests a hint on how to serialize it
        :param headers: Override the headers with one provided here
        :param url: Override the url with one provided here
        :return: the new object that was created
        """
        if not headers:
            headers = self.http_session.headers
        if url:
            api_response = self.http_session.post(url=url + endpoint, data=data, json=json, headers=headers)
        else:
            api_response = self.http_session.post(url=self.base_url + endpoint, data=data, json=json, headers=headers)
        api_response.raise_for_status()
        if api_response.text:
            return api_response.json()

    @CDOAPIWrapper()
    def put_operation(self, endpoint, json=None, data=None, url=""):
        """
        Given the endpoint, modify the object with the given put_data
        :param endpoint: the API endpoint consisting of the GUIDs of the object we wish to modify
        :param data: Data model of the existing object with new values that we wish to store
        :param url: Override the class URL if one is presented here e.g. https://dev.mysite.com
        :return: returns the updated object
        """
        if url:
            api_response = self.http_session.put(url=url + endpoint, json=json, data=data)
        else:
            api_response = self.http_session.put(url=self.base_url + endpoint, json=json, data=data)
        api_response.raise_for_status()
        if api_response.text:
            return api_response.json()

    @CDOAPIWrapper()
    def delete_operation(self, endpoint, headers=None, url=None):
        """
        Given the endpoint, delete the object
        e.g. Delete Projects/c2e66d8d-a9e2-42d0-b4e3-0ddab7cc0462/Credentials/d7bf29d8-3390-4500-b78c-00e8955fcdb7
        :param endpoint: the path to the object we wish to delete.
        :param headers: Override the headers with one provided here
        :param url: Override the url with one provided here
        :return: None
        """
        if not headers:
            headers = self.http_session.headers
        if url:
            api_response = self.http_session.delete(url=url + endpoint, headers=headers)
        else:
            api_response = self.http_session.delete(url=self.base_url + endpoint, headers=headers)
        api_response.raise_for_status()
        logger.warning(f"Deleted {endpoint}")
        if api_response.text:
            return api_response.json()
