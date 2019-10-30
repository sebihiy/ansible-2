from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import mock

from unittest import TestCase
import json

from ansible.module_utils.identity.user_provisioning.scim import SCIMClient, User


def mocked_scim_requests(*args, **kwargs):
    USERS = [
        {
            "schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id":"test01",
            "externalId":"5e771101-e3cd-4a77-851b-54f5f2668846",
            "meta":{
                "resourceType": None,
                "created":"2019-10-29T04:00:00.000+0000",
                "lastModified":None,
                "location":"http://inspq-6673.inspq.qc.ca:14102/scim/v2/Users/test01",
                "version":None
            },
            "userName":"test01",
            "name":{
                "formatted":None,
                "familyName":"Test1",
                "givenName":"Test1",
                "middleName":None,
                "honorificPrefix":None,
                "honorificSuffix":None
            },
            "displayName":None,
            "nickName":None,
            "profileUrl":None,
            "title":None,
            "userType":None,
            "preferredLanguage":None,
            "locale":None,
            "timezone":None,
            "active":None,
            "password":None,
            "emails":[
                {
                    "value":"test1@test.test",
                    "display":None,
                    "type":None,
                    "primary":None
                }
            ],
            "phoneNumbers":None,
            "ims":None,
            "photos":None,
            "addresses":None,
            "groups":None,
            "entitlements":None,
            "roles":[
                {
                    "value":"100",
                    "display":"FA-SAISIE",
                    "type":None,
                    "primary":None
                }
            ],
            "x509Certificates":None
        },
        {
            "schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id":"test02",
            "externalId":"5e771101-e3cd-4a77-851b-54f5f2668846",
            "meta":{
                "resourceType": None,
                "created":"2019-10-29T04:00:00.000+0000",
                "lastModified":None,
                "location":"http://inspq-6673.inspq.qc.ca:14102/scim/v2/Users/test02",
                "version":None
            },
            "userName":"test02",
            "name":{
                "formatted":None,
                "familyName":"Test2",
                "givenName":"Test2",
                "middleName":None,
                "honorificPrefix":None,
                "honorificSuffix":None
            },
            "displayName":None,
            "nickName":None,
            "profileUrl":None,
            "title":None,
            "userType":None,
            "preferredLanguage":None,
            "locale":None,
            "timezone":None,
            "active":None,
            "password":None,
            "emails":[
                {
                    "value":"test2@test.test",
                    "display":None,
                    "type":None,
                    "primary":None
                }
            ],
            "phoneNumbers":None,
            "ims":None,
            "photos":None,
            "addresses":None,
            "groups":None,
            "entitlements":None,
            "roles":[
                {
                    "value":"100",
                    "display":"FA-SAISIE",
                    "type":None,
                    "primary":None
                }
            ],
            "x509Certificates":None
        },
        {
            "schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id":"test03",
            "externalId":"5e771101-e3cd-4a77-851b-54f3f2668846",
            "meta":{
                "resourceType": None,
                "created":"2019-10-29T04:00:00.000+0000",
                "lastModified":None,
                "location":"http://inspq-6673.inspq.qc.ca:14102/scim/v2/Users/test03",
                "version":None
            },
            "userName":"test03",
            "name":{
                "formatted":None,
                "familyName":"Test3",
                "givenName":"Test3",
                "middleName":None,
                "honorificPrefix":None,
                "honorificSuffix":None
            },
            "displayName":None,
            "nickName":None,
            "profileUrl":None,
            "title":None,
            "userType":None,
            "preferredLanguage":None,
            "locale":None,
            "timezone":None,
            "active":None,
            "password":None,
            "emails":[
                {
                    "value":"test.test3@test.test",
                    "display":None,
                    "type":None,
                    "primary":None
                }
            ],
            "phoneNumbers":None,
            "ims":None,
            "photos":None,
            "addresses":None,
            "groups":None,
            "entitlements":None,
            "roles":[
                {
                    "value":"100",
                    "display":"FA-SAISIE",
                    "type":None,
                    "primary":None
                }
            ],
            "x509Certificates":None
        },        
        {
            "schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id":"test02",
            "externalId":"5e771101-e3cd-4a77-851b-54f5f2668846",
            "meta":{
                "resourceType": None,
                "created":"2019-10-29T04:00:00.000+0000",
                "lastModified":None,
                "location":"http://inspq-6673.inspq.qc.ca:14102/scim/v2/Users/test02",
                "version":None
            },
            "userName":"test02",
            "name":{
                "formatted":None,
                "familyName":"Test2",
                "givenName":"Test2",
                "middleName":None,
                "honorificPrefix":None,
                "honorificSuffix":None
            },
            "displayName":"Test 02",
            "nickName":None,
            "profileUrl":None,
            "title":None,
            "userType":None,
            "preferredLanguage":None,
            "locale":None,
            "timezone":None,
            "active":None,
            "password":None,
            "emails":[
                {
                    "value":"test2@test.test",
                    "display":None,
                    "type":None,
                    "primary":None
                }
            ],
            "phoneNumbers":None,
            "ims":None,
            "photos":None,
            "addresses":None,
            "groups":None,
            "entitlements":None,
            "roles":[
                {
                    "value":"100",
                    "display":"FA-SAISIE",
                    "type":None,
                    "primary":None
                }
            ],
            "x509Certificates":None
        }
    ]        
    class MockResponse:
        def __init__(self, json_data, status_code):
            #self.json_data = json_data
            self.code = status_code
            self.fp = json.dumps(json_data)
            self.json_data = json_data
            self.headers = {
                "dict": {
                    "connection":"close",
                    "content-type":"application/json;charset=UTF-8",
                    "date": "Wed, 30 Oct 2019 12:46:02 GMT",
                    "transfer-encoding": "chunked"
                },
                "headers":['Content-Type: application/json;charset=UTF-8\r\n', 'Transfer-Encoding: chunked\r\n', 'Date: Wed, 30 Oct 2019 12:46:02 GMT\r\n', 'Connection: close\r\n']
            }
                        
        def read(self):
            return self.fp

    if args[0] == 'http://scim.server.url/scim/v2/Users/.search' and kwargs["method"] == 'POST':
        response = {
            "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
            "id": None,
            "externalId": None,
            "meta": None,
            "totalResults": 1,
            "Resources": [ USERS[1] ],
            "startIndex": 1,
            "itemsPerPage": 10
        }
        return MockResponse(
            response
            ,200)
        
    elif args[0] == 'http://scim.server.url/scim/v2/Users/' + USERS[1]["userName"] and kwargs["method"] == 'GET':
        return MockResponse(USERS[1], 200)

    elif args[0] == 'http://scim.server.url/scim/v2/Users' and kwargs["method"] == 'POST':
        return MockResponse(USERS[2], 201)

    elif args[0] == 'http://scim.server.url/scim/v2/Users/' + USERS[0]["userName"] and kwargs["method"] == 'DELETE':
        return MockResponse(None, 204)

    elif args[0] == 'http://scim.server.url/scim/v2/Users/' + USERS[1]["userName"] and kwargs["method"] == 'PUT':
        return MockResponse(USERS[3], 204)
    
    return MockResponse(None, 404)

class SCIMTestCase(TestCase):
    access_token = ""
    userToAdd = {
        "schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],
        "id":"test03",
        "externalId":"5e771101-e3cd-4a77-851b-54f3f2668846",
        "meta":{
            "resourceType": None,
            "created":"2019-10-29T04:00:00.000+0000",
            "lastModified":None,
            "location":"http://inspq-6673.inspq.qc.ca:14102/scim/v2/Users/test03",
            "version":None
        },
        "userName":"test03",
        "name":{
            "formatted":None,
            "familyName":"Test3",
            "givenName":"Test3",
            "middleName":None,
            "honorificPrefix":None,
            "honorificSuffix":None
        },
        "displayName":None,
        "nickName":None,
        "profileUrl":None,
        "title":None,
        "userType":None,
        "preferredLanguage":None,
        "locale":None,
        "timezone":None,
        "active":None,
        "password":None,
        "emails":[
            {
                "value":"test.test3@test.test",
                "display":None,
                "type":None,
                "primary":None
            }
        ],
        "phoneNumbers":None,
        "ims":None,
        "photos":None,
        "addresses":None,
        "groups":None,
        "entitlements":None,
        "roles":[
            {
                "value":"100",
                "display":"FA-SAISIE",
                "type":None,
                "primary":None
            }
        ],
        "x509Certificates":None
    }
    testUsers = [
        {
            "schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id":"test01",
            "externalId":"5e771101-e3cd-4a77-851b-54f5f2668846",
            "meta":{
                "resourceType": None,
                "created":"2019-10-29T04:00:00.000+0000",
                "lastModified":None,
                "location":"http://inspq-6673.inspq.qc.ca:14102/scim/v2/Users/test01",
                "version":None
            },
            "userName":"test01",
            "name":{
                "formatted":None,
                "familyName":"Test1",
                "givenName":"Test1",
                "middleName":None,
                "honorificPrefix":None,
                "honorificSuffix":None
            },
            "displayName":None,
            "nickName":None,
            "profileUrl":None,
            "title":None,
            "userType":None,
            "preferredLanguage":None,
            "locale":None,
            "timezone":None,
            "active":None,
            "password":None,
            "emails":[
                {
                    "value":"test1@test.test",
                    "display":None,
                    "type":None,
                    "primary":None
                }
            ],
            "phoneNumbers":None,
            "ims":None,
            "photos":None,
            "addresses":None,
            "groups":None,
            "entitlements":None,
            "roles":[
                {
                    "value":"100",
                    "display":"FA-SAISIE",
                    "type":None,
                    "primary":None
                }
            ],
            "x509Certificates":None
        },
        {
            "schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id":"test02",
            "externalId":"5e771101-e3cd-4a77-851b-54f5f2668846",
            "meta":{
                "resourceType": None,
                "created":"2019-10-29T04:00:00.000+0000",
                "lastModified":None,
                "location":"http://inspq-6673.inspq.qc.ca:14102/scim/v2/Users/test02",
                "version":None
            },
            "userName":"test02",
            "name":{
                "formatted":None,
                "familyName":"Test2",
                "givenName":"Test2",
                "middleName":None,
                "honorificPrefix":None,
                "honorificSuffix":None
            },
            "displayName":None,
            "nickName":None,
            "profileUrl":None,
            "title":None,
            "userType":None,
            "preferredLanguage":None,
            "locale":None,
            "timezone":None,
            "active":None,
            "password":None,
            "emails":[
                {
                    "value":"test2@test.test",
                    "display":None,
                    "type":None,
                    "primary":None
                }
            ],
            "phoneNumbers":None,
            "ims":None,
            "photos":None,
            "addresses":None,
            "groups":None,
            "entitlements":None,
            "roles":[
                {
                    "value":"100",
                    "display":"FA-SAISIE",
                    "type":None,
                    "primary":None
                }
            ],
            "x509Certificates":None
        }
    ]        
    
    def setUp(self):
        TestCase.setUp(self)

    def tearDown(self):
        TestCase.tearDown(self)


    @mock.patch('ansible.module_utils.identity.user_provisioning.scim.open_url', side_effect=mocked_scim_requests)
    def testSearchUser(self, open_url):
        userToSearch = "test02"
        scimClient = SCIMClient(base_url="http://scim.server.url/scim/v2", access_token=self.access_token)
        scimuser = scimClient.searchUserByUserName(userToSearch)
        self.assertEqual(scimuser.userName, userToSearch, scimuser.userName + " is not " + userToSearch)
        
    @mock.patch('ansible.module_utils.identity.user_provisioning.scim.open_url', side_effect=mocked_scim_requests)
    def testGetUserById(self, open_url):
        userToGet = "test02"
        scimClient = SCIMClient(base_url="http://scim.server.url/scim/v2", access_token=self.access_token)
        scimuser = scimClient.getUserById(userToGet)
        self.assertEqual(scimuser.userName, userToGet, scimuser.userName + " is not " + userToGet)

    @mock.patch('ansible.module_utils.identity.user_provisioning.scim.open_url', side_effect=mocked_scim_requests)
    def testCreateUser(self, open_url):
        userToCreate = User.from_json(json.dumps(self.userToAdd))
        scimClient = SCIMClient(base_url="http://scim.server.url/scim/v2", access_token=self.access_token)
        scimuser = scimClient.createUser(userToCreate)
        self.assertEqual(scimuser.userName, userToCreate.userName, scimuser.userName + " is not " + userToCreate.userName)
        
    @mock.patch('ansible.module_utils.identity.user_provisioning.scim.open_url', side_effect=mocked_scim_requests)
    def testDeleteUser(self, open_url):
        userToDelete = User.from_json(json.dumps(self.testUsers[0]))
        scimClient = SCIMClient(base_url="http://scim.server.url/scim/v2", access_token=self.access_token)
        response = scimClient.deleteUser(userToDelete)
        self.assertEqual(response.code, 204, "Create response code incorrect: " + str(response.code))

    @mock.patch('ansible.module_utils.identity.user_provisioning.scim.open_url', side_effect=mocked_scim_requests)
    def testUpdateUser(self, open_url):
        userToUpdate = User.from_json(json.dumps(self.testUsers[1]))
        userToUpdate.displayName = "Test 02"
        scimClient = SCIMClient(base_url="http://scim.server.url/scim/v2", access_token=self.access_token)
        scimuser = scimClient.updateUser(userToUpdate)
        self.assertEqual(scimuser.userName, userToUpdate.userName, scimuser.userName + " is not " + userToUpdate.userName)
