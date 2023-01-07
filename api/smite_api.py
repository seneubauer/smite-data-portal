# import dependencies
from datetime import datetime
from enum import Enum
import hashlib
import requests
import json

# define enumerations
class response_types(Enum):
    json = "json"
    xml = "xml"

class languages(Enum):
    english = 1
    german = 2
    french = 3
    chinese = 5
    spanish = 7
    spanish_la = 9
    portuguese = 10
    russian = 11
    polish = 12
    turkish = 13

class method_types(Enum):
    ping = "ping"
    create_session = "createsession"
    get_gods = "getgods"
    get_god_alt_abilities = "getgodaltabilities"
    get_items = "getitems"
    get_player = "getplayer"
    get_match_details = "getmatchdetails"

class service_method_types(Enum):
    test_session = "testsession"
    get_data_used = "getdataused"
    get_hirez_server_status = "gethirezserverstatus"
    get_patch_info = "getpatchinfo"

# define the smite api class
class smite_api:
    
    # object initialization
    def __init__(self, dev_id:int, auth_key:str) -> None:
        self.dev_id = dev_id
        self.auth_key = auth_key
        self.base_url = "https://api.smitegame.com/smiteapi.svc"
    
    # ping the hi-rez api server
    def ping_server(self) -> str:
        url = f"{self.base_url}/ping{response_types.json.value}".encode("utf-8")
        return requests.get(url).json()
    
    # get the current utc time as a string timestamp
    def get_timestamp(self) -> str:
        self.dt_now = datetime.utcnow()
        return self.dt_now.strftime("%Y%m%d%H%M%S")
    
    # create a new signature
    def create_signature(self, method:str, timestamp:str) -> str:
        return hashlib.md5(f"{self.dev_id}{method}{self.auth_key}{timestamp}".encode("utf-8")).hexdigest()
    
    # create a new session
    def create_session(self) -> dict:
        
        # url parameters
        timestamp = self.get_timestamp()
        signature = self.create_signature(method_types.create_session.value, timestamp)
        url = f"{self.base_url}/{method_types.create_session.value}{response_types.json.value}/{self.dev_id}/{signature}/{timestamp}".encode("utf-8")
        
        # request the smite api server
        result = requests.get(url)
        result_json = json.loads(result.text)
        
        # remember the session id, but only if the session was successfully created
        if result_json["ret_msg"] == "Approved":
            self.is_connected = True
            self.session_id = result_json["session_id"]
        else:
            self.is_connected = False
        
        # return the results
        return result_json

    # get all items
    def get_all_items(self) -> dict:
        if self.is_connected:
            
            # url parameters
            timestamp = self.get_timestamp()
            signature = self.create_signature(method_types.get_items.value, timestamp)
            url = f"{self.base_url}/{method_types.get_items.value}{response_types.json.value}/{self.dev_id}/{signature}/{self.session_id}/{timestamp}/{languages.english.value}".encode("utf-8")
            
            # request the smite api server
            result = requests.get(url)
            
            # return the results
            return json.loads(result.text)
        else:
            return { "Error": "service not connected" }
    
    # get all gods
    def get_all_gods(self) -> dict:
        if self.is_connected:
            
            # url parameters
            timestamp = self.get_timestamp()
            signature = self.create_signature(method_types.get_gods.value, timestamp)
            url = f"{self.base_url}/{method_types.get_gods.value}{response_types.json.value}/{self.dev_id}/{signature}/{self.session_id}/{timestamp}/{languages.english.value}".encode("utf-8")
            
            # request the smite api server
            result = requests.get(url)
            
            # return the results
            return json.loads(result.text) 
        else:
            return { "Error": "service not connected" }
    
    # get all gods alt abilities
    def get_all_gods_alt_abilities(self) -> dict:
        if self.is_connected:
            
            # url parameters
            timestamp = self.get_timestamp()
            signature = self.create_signature(method_types.get_god_alt_abilities.value, timestamp)
            url = f"{self.base_url}/{method_types.get_god_alt_abilities.value}{response_types.json.value}/{self.dev_id}/{signature}/{self.session_id}/{timestamp}/{languages.english.value}".encode("utf-8")
            
            # request the smite api server
            result = requests.get(url)
            
            # return the results
            return json.loads(result.text) 
        else:
            return { "Error": "service not connected" }
    
    # retrieve various information about the current session
    def get_session_information(self, method:service_method_types) -> dict:
        if self.is_connected:
            
            # url parameters
            timestamp = self.get_timestamp()
            signature = self.create_signature(method.value, timestamp)
            url = f"{self.base_url}/{method.value}{response_types.json.value}/{self.dev_id}/{signature}/{self.session_id}/{timestamp}".encode("utf-8")
            
            # request the smite api server
            result = requests.get(url)
            
            # return the results
            return json.loads(result.text)
        else:
            return { "Error": "service not connected" }