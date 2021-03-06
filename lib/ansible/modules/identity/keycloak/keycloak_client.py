#!/usr/bin/python
# -*- coding: utf-8 -*-
# (c) 2017, Philippe Gauthier INSPQ <philippe.gauthier@inspq.qc.ca>
#
# This file is not part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
author: "Philippe Gauthier (philippe.gauthier@inspq.qc.ca"
module: keycloak_client
short_description: Configure a client in Keycloak
description:
    - This module creates, removes or update Keycloak client.
version_added: "2.3"
options:
    url:
        description:
            - The url of the Keycloak server.
        default: http://localhost:8080/auth    
        required: true    
    username:
        description:
            - The username to logon to the master realm.
        required: true
    password:
        description:
            - The password for the user to logon the master realm.
        required: true
    realm:
        description:
            - The name of the realm in which is the client.
        required: true
    clientId:
        description:
            - OIDC Client ID for the client.
        required: true
    rootUrl:
        description:
            - The root URL of the client Application.
        required: false
    name:
        description:
            - Name for the client application.
        required: false
    description:
        description:
            - Description of the client Application.
        required: false
    adminUrl:
        description:
            - URL for the admin module for the Application.
        required: false
    enabled:
        description:
            - enabled.
        default: True
        required: false
    clientAuthenticatorType:
        description: 
            - client Authenticator Type.
        required: false
    redirectUris:
        description:
            - List of redirect URIs.
        required: true
    webOrigins:
        description:
            - List of allowed CORS origins.
        required: false
    consentRequired:
        description:
            - consent Required.
        required: false
    standardFlowEnabled:
        description:
            - standard Flow Enabled.
        required: false
    implicitFlowEnabled:
        description:
            - implicitFlowEnabled. 
        required: false
    directAccessGrantsEnabled:
        description:
            - Direct Access Grants Enabled.
        required: false
    serviceAccountsEnabled:
        description:
            - service Accounts Enabled.
        required: false
    authorizationServicesEnabled:
        description:
            - authorization Services Enabled.
        required: false
        default: true
    protocol:
        description:
            - Protocol.
        required: false
    bearerOnly:
        description:
            - bearer Only access type.
        required: false
    publicClient:
        description:
            - Public client access type.
        required: false
    roles:
        description:
            - List of roles for the client
        required: false
    protocolMappers:
        description:
            - List of protocol mappers for the client
        required: false
    state:
        description:
            - Control if the client must exists or not
        choices: [ "present", "absent" ]
        default: present
        required: false
    force:
        description:
            - If yes, allows to remove client and recreate it.
        choices: [ "yes", "no" ]
        default: "no"
        required: false
notes:
    - module does not modify clientId.
'''

EXAMPLES = '''
    - name: Create a client client1 with default settings.
      keycloak_client:
        url: http://localhost:8080
        username: admin
        password: password
        realm: master
        name: client1
        description: Client App 1
        rootUrl: http://localhost:8081/app
        redirectUris:
          - http://localhost:8081/*
        webOrigins:
          - "*"
        roles: 
          - name: "groupName"
            description: "Role1"
            composite: true
            composites:
              - Id: existinqClient
                name: role1ofclient
        protocolMappers:
          - name: MapperName
            protocol: openid-connect
            protocolMapper: oidc-usermodel-attribute-mapper
            consentRequired: false
            config:
              multivalued: false
              userinfo.token.claim: true
              user.attribute: attributeName
              id.token.claim: true
              access.token.claim: true
              claim.name: nameOfTheClaim
              jsonType.label: String
        state: present

    - name: Re-create client1
      keycloak_client:
        url: http://localhost:8080
        username: admin
        password: password
        realm: master
        name: client1
        description: Client App 1
        rootUrl: http://localhost:8081/app
        redirectUris:
          - http://localhost:8081/*
        webOrigins:
          - "*"
        roles: 
          - name: "groupName"
            description: "Role1"
            composite: true
            composites:
              - Id: existinqClient
                name: role1ofclient
        protocolMappers:
          - name: MapperName
            protocol: openid-connect
            protocolMapper: oidc-usermodel-attribute-mapper
            consentRequired: false
            config:
              multivalued: false
              userinfo.token.claim: true
              user.attribute: attributeName
              id.token.claim: true
              access.token.claim: true
              claim.name: nameOfTheClaim
              jsonType.label: String
        state: present
        force: yes

    - name: Remove client1.
      keycloak_client:
        url: http://localhost:8080
        username: admin
        password: admin
        realm: master
        name: client1
        state: absent
'''

RETURN = '''
ansible_facts:
  description: JSON representation for the client.
  returned: on success
  type: dict
stderr:
  description: Error message if it is the case
  returned: on error
  type: str
rc:
  description: return code, 0 if success, 1 otherwise.
  returned: always
  type: bool
changed:
  description: Return True if the operation changed the client on the keycloak server, false otherwise.
  returned: always
  type: bool
'''
import requests
import json
import urllib
from ansible.module_utils.keycloak_utils import *
from __builtin__ import isinstance    

def main():
    module = AnsibleModule(
        argument_spec = dict(
            url=dict(type='str', required=True),
            username=dict(type='str', required=True),
            password=dict(required=True),
            realm=dict(type='str', required=True),
            clientId=dict(type='str', required=True),
            rootUrl=dict(type='str'),
            name=dict(type='str'),
            description = dict(type='str'),
            adminUrl=dict(type='str'),
            enabled=dict(type='bool',default=True),
            clientAuthenticatorType = dict(type='str'),
            redirectUris = dict(type='list'),
            webOrigins = dict(type='list'),
            consentRequired = dict(type='bool'),
            standardFlowEnabled = dict(type='bool'),
            implicitFlowEnabled = dict(type='bool'),
            directAccessGrantsEnabled = dict(type='bool'),
            serviceAccountsEnabled = dict(type='bool'),
            authorizationServicesEnabled = dict(type='bool', default=True),
            protocol = dict(type='str'),
            bearerOnly = dict(type='bool'),
            publicClient = dict(type='bool'),
            roles = dict(type='list'),
            protocolMappers = dict(type='list'),
            state=dict(choices=["absent", "present"], default='present'),
            force=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )
    params = module.params.copy()
    params['force'] = module.boolean(module.params['force'])
    
    result = client(params)
    
    if result['rc'] != 0:
        module.fail_json(msg='non-zero return code', **result)
    else:
        module.exit_json(**result)
    
    
def client(params):
    url = params['url']
    username = params['username']
    password = params['password']
    realm = params['realm']
    state = params['state']
    force = params['force']
    newClientRoles = None
    newClientProtocolMappers = None
    newComposites = None
    #newRoleRepresentation = None
    
    # Créer un représentation du client recu en paramètres
    newClientRepresentation = {}
    newClientRepresentation["clientId"] = params['clientId'].decode("utf-8")
    if "rootUrl" in params and params['rootUrl'] is not None:
        newClientRepresentation["rootUrl"] = params['rootUrl'].decode("utf-8")
    if "name" in params and params['name'] is not None:
        newClientRepresentation["name"] = params['name'].decode("utf-8")
    if "description" in params and params['description'] is not None:
        newClientRepresentation["description"] = params['description'].decode("utf-8")
    if "adminUrl" in params and params['adminUrl'] is not None:
        newClientRepresentation["adminUrl"] = params['adminUrl'].decode("utf-8")
        
    if "enabled" in params:
        newClientRepresentation["enabled"] = params['enabled']
    if "clientAuthenticatorType" in params and params['clientAuthenticatorType'] is not None:
        newClientRepresentation["clientAuthenticatorType"] = params['clientAuthenticatorType'].decode("utf-8")
    if "redirectUris" in params and params['redirectUris'] is not None:
        newClientRepresentation["redirectUris"] = params['redirectUris']
    if "webOrigins" in params and params['webOrigins'] is not None:
        newClientRepresentation["webOrigins"] = params['webOrigins']
    if "consentRequired" in params:
        newClientRepresentation["consentRequired"] = params['consentRequired']   
    if "standardFlowEnabled" in params:
        newClientRepresentation["standardFlowEnabled"] = params['standardFlowEnabled']
    if "implicitFlowEnabled" in params:
        newClientRepresentation["implicitFlowEnabled"] = params['implicitFlowEnabled']
    if "directAccessGrantsEnabled" in params:
        newClientRepresentation["directAccessGrantsEnabled"] = params['directAccessGrantsEnabled']
    if 'authorizationServicesEnabled' in params:
        newClientRepresentation["authorizationServicesEnabled"] = params['authorizationServicesEnabled']
        if newClientRepresentation["authorizationServicesEnabled"]:
            newClientRepresentation["serviceAccountsEnabled"] = True
        elif "serviceAccountsEnabled" in params:
            newClientRepresentation["serviceAccountsEnabled"] = params['serviceAccountsEnabled']
    if "protocol" in params and params['protocol'] is not None:
        newClientRepresentation["protocol"] = params['protocol'].decode("utf-8")
    if "bearerOnly" in params:
        newClientRepresentation["bearerOnly"] = params['bearerOnly']
    if "publicClient" in params:
        newClientRepresentation["publicClient"] = params['publicClient']
    if 'roles' in params and params['roles'] is not None:
        newClientRoles = params['roles']
    if 'protocolMappers' in params and params['protocolMappers'] is not None:
        newClientProtocolMappers = params['protocolMappers']
    composites = []
    Repsonse = []
    
    clientSvcBaseUrl = url + "/auth/admin/realms/" + realm + "/clients/"
    
    rc = 0
    result = dict()
    changed = False

    try:
        headers = loginAndSetHeaders(url, username, password)
    except Exception, e:
        result = dict(
            stderr   = 'login: ' + str(e),
            rc       = 1,
            changed  = changed
            )
        return result
    try: 
        # Vérifier si le client existe sur le serveur Keycloak
        getResponse = requests.get(clientSvcBaseUrl, headers=headers, params={'clientId': newClientRepresentation["clientId"]})
    except Exception, e:
        result = dict(
            stderr   = 'first client get: ' + str(e),
            rc       = 1,
            changed  = changed
            )
        return result
        
    if len(getResponse.json()) == 0: # Le client n'existe pas
        # Creer le client
        
        if (state == 'present'): # Si le status est présent
            try:
                # Stocker le client dans un body prêt a être posté
                data=json.dumps(newClientRepresentation)
                # Créer le client
                postResponse = requests.post(clientSvcBaseUrl, headers=headers, data=data)
                # Obtenir le nouveau client créé
                getResponse = requests.get(clientSvcBaseUrl, headers=headers, params={'clientId': newClientRepresentation["clientId"]})
                clientRepresentation = getResponse.json()[0]
                # Créer les rôles
                if newClientRoles is not None:
                    for newClientRole in newClientRoles:
                        newRoleRepresentation = {}
                        newRoleRepresentation["name"] = newClientRole['name'].decode("utf-8")
                        if "description" in newClientRole and newClientRole['description'] is not None:
                            newRoleRepresentation["description"] = newClientRole['description'].decode("utf-8")
                        newRoleRepresentation["composite"] = newClientRole['composite'] if "composite" in newClientRole else False
                        #data=json.dumps(newClientRole)
                        data=json.dumps(newRoleRepresentation)
                        postResponse = requests.post(clientSvcBaseUrl + clientRepresentation['id'] + '/roles', headers=headers, data=data)
                        # rôle composites
                        if 'composites' in newClientRole and newClientRole['composites'] is not None:
                            newComposites = newClientRole['composites']
                            getResponse=requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/roles', headers=headers)
                            newCompositeToCreate = []
                            if getResponse.status_code == 404:
                                raise Exception("Role just created not found: " + str(newComposites))
                            else:# rôle composites update
                                roles = getResponse.json()
                                for newComposite in newComposites:
                                    for role in roles:
                                        if role['name'] == newComposite['name']:
                                            newComposite['id'] = role['id']
                                            newCompositeToCreate.append(newComposite)
                                # rôle composites
                                data=json.dumps(newCompositeToCreate)
                                postResponse = requests.post(clientSvcBaseUrl + clientRepresentation['id'] + '/roles/'+ newClientRole['name'] +'/composites', headers=headers, data=data)
                                getResponse = requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/roles/'+ newClientRole['name'] +'/composites', headers=headers)
                                composites.append(getResponse.text)
                # Créer les protocols mappers
                if newClientProtocolMappers is not None:
                    for newClientProtocolMapper in newClientProtocolMappers:
                        data=json.dumps(newClientProtocolMapper)
                        postResponse = requests.post(clientSvcBaseUrl + clientRepresentation['id'] + '/protocol-mappers/models', headers=headers, data=data)
                # Obtenir la version finale du nouveau client créé
                getResponse = getResponse = requests.get(clientSvcBaseUrl, headers=headers, params={'clientId': newClientRepresentation["clientId"]})
                clientRepresentation = getResponse.json()[0]
                # Obtenir le ClientSecret
                getResponse = requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/client-secret', headers=headers)
                clientSecretRepresentation = getResponse.json()
                # Obtenir les rôles pour le client
                getResponse = requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/roles', headers=headers)
                clientRolesRepresentation = getResponse.json()
                changed = True
                fact = dict(
                    client = clientRepresentation,
                    clientSecret = clientSecretRepresentation,
                    composites = composites,
                    clientRoles = clientRolesRepresentation)
                
                result = dict(
                    ansible_facts = fact,
                    rc = 0,
                    changed = changed
                    )
            except requests.exceptions.RequestException, e:
                fact = dict(
                    client = newClientRepresentation)
                result = dict(
                    ansible_facts= fact,
                    stderr   = 'post client: ' + newClientRepresentation["clientId"] + ' erreur: ' + str(e),
                    rc       = 1,
                    changed  = changed
                    )
            except ValueError, e:
                fact = dict(
                    client = newClientRepresentation)
                result = dict(
                    ansible_facts = fact,
                    stderr   = 'post client: ' + newClientRepresentation["clientId"] + ' erreur: ' + str(e),
                    rc       = 1,
                    changed  = changed
                    )
        elif state == 'absent': # Sinon, le status est absent
            result = dict(
                stdout   = newClientRepresentation["clientId"] + ' absent',
                rc       = 0,
                changed  = changed
            )
                
    else:  # Le client existe déjà
        clientRepresentation = getResponse.json()[0]
        try:
            if (state == 'present'): # si le status est présent
                if force: # Si l'option force est sélectionné
                    # Supprimer le client existant
                    deleteResponse = requests.delete(clientSvcBaseUrl + clientRepresentation["id"], headers=headers)
                    changed = True
                    # Stocker le client dans un body prêt a être posté
                    data=json.dumps(newClientRepresentation)
                    # Créer le nouveau client
                    postResponse = requests.post(clientSvcBaseUrl, headers=headers, data=data)
                else: # Si l'option force n'est pas sélectionné
                    excludes = []
                    if "webOrigins" in newClientRepresentation and len(newClientRepresentation['webOrigins']) == 0:
                        excludes.append("webOrigins")
                    # Comparer les clients
                    if (isDictEquals(newClientRepresentation, clientRepresentation, excludes)): # Si le nouveau client n'introduit pas de modification au client existant
                        # Ne rien changer
                        changed = False
                    else: # Si le client doit être modifié
                        # Stocker le client dans un body prêt a être posté
                        data=json.dumps(newClientRepresentation)
                        # Mettre à jour le client sur le serveur Keycloak
                        updateResponse = requests.put(clientSvcBaseUrl + clientRepresentation["id"], headers=headers, data=data)
                        changed = True
                # Obtenir le nouveau client créé
                getResponse = getResponse = requests.get(clientSvcBaseUrl, headers=headers, params={'clientId': newClientRepresentation["clientId"]})
                clientRepresentation = getResponse.json()[0]
                # Traiter les rôles
                if newClientRoles is not None:
                    # Obtenir la liste des rôles existant pour le client
                    getResponse = requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/roles', headers=headers)
                    clientRoles = getResponse.json()
                    for newClientRole in newClientRoles:
                        data=json.dumps(newClientRole)
                        clientRoleFound = False
                        # Vérifier si le rôle a créer existe déjà pour le client
                        for clientRole in clientRoles:
                            if (clientRole['name'] == newClientRole['name']):
                                clientRoleFound = True
                                break
                        # Si le rôle existe pour le client
                        if clientRoleFound:
                            # Obtenir la définition du rôle    
                            getResponse = requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/roles/' + newClientRole['name'], headers=headers)
                            clientRole = getResponse.json()
                            # Comparer le rôle existant avec celui envoyé
                            excludes = []
                            if "composites" in newClientRole:
                                excludes.append("composites")
                            if not isDictEquals(newClientRole, clientRole,excludes):
                                # S'il est différent, le modifier
                                changed = True
                                newRoleRepresentation = {}
                                newRoleRepresentation["name"] = newClientRole['name'].decode("utf-8")
                                newRoleRepresentation["description"] = newClientRole['description'].decode("utf-8")
                                newRoleRepresentation["composite"] = newClientRole['composite'] if "composite" in newClientRole else False
                                #data=json.dumps(newClientRole)
                                data=json.dumps(newRoleRepresentation)
                                putResponse=requests.put(clientSvcBaseUrl + clientRepresentation['id'] + '/roles/' + newClientRole['name'], headers=headers, data=data)
                                # rôle composites
                                if 'composites' in newClientRole and newClientRole['composites'] is not None:
                                    newComposites = newClientRole['composites']
                                    #ID of composite role by name
                                    getResponse=requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/roles', headers=headers)
                                    #getResponse=requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/roles/' + newComposites['name'], headers=headers)
                                    newCompositeToCreate = []
                                    if getResponse.status_code == 404:
                                        raise Exception("Role just created not found: " + str(newComposites))
                                    else:# rôle composites update
                                        roles = getResponse.json()
                                        for newComposite in newComposites:
                                            for role in roles:
                                                if role['name'] == newComposite['name']:
                                                    newComposite['id'] = role['id']
                                                    newCompositeToCreate.append(newComposite)
                                        # rôle composites
                                        data=json.dumps(newCompositeToCreate)
                                        delResponse = requests.delete(clientSvcBaseUrl + clientRepresentation['id'] + '/roles/'+ newClientRole['name'] +'/composites', headers=headers, data=data)
                                        putResponse = requests.post(clientSvcBaseUrl + clientRepresentation['id'] + '/roles/'+ newClientRole['name'] +'/composites', headers=headers, data=data)
                                        getResponse = requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/roles/'+ newClientRole['name'] +'/composites', headers=headers)
                                        composites.append(getResponse.text)
                        else: # Si le rôle n'existe pas pour ce client
                            changed = True
                            # Créer le rôle
                            newRoleRepresentation = {}
                            newRoleRepresentation["name"] = newClientRole['name'].decode("utf-8")
                            newRoleRepresentation["description"] = newClientRole['description'].decode("utf-8")
                            newRoleRepresentation["composite"] = newClientRole['composite'] if "composite" in newClientRole else False
                            #data=json.dumps(newClientRole)
                            data=json.dumps(newRoleRepresentation)
                            postResponse = requests.post(clientSvcBaseUrl + clientRepresentation['id'] + '/roles', headers=headers, data=data)
                            # rôle composites
                            if 'composites' in newClientRole and newClientRole['composites'] is not None:
                                newComposites = newClientRole['composites']
                                #ID of composite role by name
                                getResponse=requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/roles', headers=headers)
                                #getResponse=requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/roles/' + newComposites['name'], headers=headers)
                                newCompositeToCreate = []
                                if getResponse.status_code == 404:
                                    raise Exception("Role just created not found: " + str(newComposites))
                                else:# rôle composites update
                                    roles = getResponse.json()
                                    for newComposite in newComposites:
                                        for role in roles:
                                            if role['name'] == newComposite['name']:
                                                newComposite['id'] = role['id']
                                                newCompositeToCreate.append(newComposite)
                                    data=json.dumps(newCompositeToCreate)
                                    postResponse = requests.post(clientSvcBaseUrl + clientRepresentation['id'] + '/roles/'+ newClientRole['name'] +'/composites', headers=headers, data=data)
                                    getResponse = requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/roles/'+ newClientRole['name'] +'/composites', headers=headers)
                                    composites.append(getResponse.text)
                # Traiter les protocol Mappers
                if newClientProtocolMappers is not None:
                    # Obtenir la liste des mappers existant pour le client
                    getResponse = requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/protocol-mappers/models', headers=headers)
                    clientMappers = getResponse.json()
                    for newClientProtocolMapper in newClientProtocolMappers:
                        clientMapperFound = False
                        # Vérifier si le mapper a créer existe déjà pour le client
                        for clientMapper in clientMappers:
                            if (clientMapper['name'] == newClientProtocolMapper['name']):
                                clientMapperFound = True
                                break
                        # Si le mapper existe pour le client
                        if clientMapperFound:
                            if not isDictEquals(newClientProtocolMapper, clientMapper):
                                # S'il est différent, le modifier
                                changed = True
                                newClientProtocolMapper["id"] = clientMapper["id"]
                                data=json.dumps(newClientProtocolMapper)
                                putResponse=requests.put(clientSvcBaseUrl + clientRepresentation['id'] + '/protocol-mappers/models/' + clientMapper['id'], headers=headers, data=data)
                        else: # Si le mapper n'existe pas pour ce client
                            changed = True
                            # Créer le mapper
                            data=json.dumps(newClientProtocolMapper)
                            postResponse = requests.post(clientSvcBaseUrl + clientRepresentation['id'] + '/protocol-mappers/models', headers=headers, data=data)
                # Obtenir la version finale du client modifié
                getResponse = getResponse = requests.get(clientSvcBaseUrl, headers=headers, params={'clientId': newClientRepresentation["clientId"]})
                clientRepresentation = getResponse.json()[0]
                # Obtenir le ClientSecret
                getResponse = requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/client-secret', headers=headers)
                clientSecretRepresentation = getResponse.json()
                # Obtenir les rôles
                getResponse = requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/roles', headers=headers)
                clientRolesRepresentation = getResponse.json()
                fact = dict(
                    client = clientRepresentation,
                    clientSecret = clientSecretRepresentation,
                    composites = composites,
                    clientRoles = clientRolesRepresentation)
                result = dict(
                    ansible_facts = fact,
                    rc = 0,
                    changed = changed
                    )
                    
            elif state == 'absent': # Le status est absent
                # Supprimer le client
                deleteResponse = requests.delete(clientSvcBaseUrl + clientRepresentation['id'], headers=headers)
                changed = True
                result = dict(
                    stdout   = 'deleted',
                    rc       = 0,
                    changed  = changed
                )
        except requests.exceptions.RequestException, e:
            result = dict(
                stderr   = 'put or delete client: ' + newClientRepresentation['clientId'] + ' error: ' + str(e),
                rc       = 1,
                changed  = changed
                )
        except ValueError, e:
            result = dict(
                stderr   = 'put or delete client: ' + newClientRepresentation['clientId'] + ' error: ' + str(e),
                rc       = 1,
                changed  = changed
                )
    return result
        
# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
