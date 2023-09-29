import json

class DB:
    def fetch():
        json_data=json.load(open("accounts.json", "r"))
        return json_data

    def check_exist(phone_number):
        json_data = json.load(open("accounts.json", "r"))
        if f"{phone_number}.session" in json_data.keys():
            return True
        return False
      
    def add_account(phone_number, password, session_string):
        if not DB.check_exist(phone_number):
            json_data = json.load(open("accounts.json", "r"))
            json_data[f"{phone_number}.session"] = {"phone_number": phone_number, "password": password,"session_string": session_string}
            with open("accounts.json","w") as file:
                file.write(json.dumps(json_data, indent=4, ensure_ascii=False))
                file.close()
            
    def get_creds():
        json_data = json.load(open('config.json', 'r'))
        return [json_data["api_id"], json_data["api_hash"]]