import json
from secret_stuff import private_folder

class KnownUserManager:
    def __init__(self, known_user_file:str) -> None:
        self.file_name = private_folder + known_user_file
        self.local_list = KnownUserManager.load_user(self.file_name)

    # New User
    def add_user(self, new_user) -> None:
        self.local_list.append(new_user)
        self.save_users()
    
    # Check if alredy know the user
    def is_known_user(self, user) -> bool:
        for saved_user in self.local_list:
            if saved_user.same_user(user):
                return True
        
        return False

    def load_user(file_name) -> list:
        local_list = []

        # Json file with all the known users
        users_in_file = open(file_name, 'r').readlines()

        entrire_file = ""
        for line in users_in_file:
            entrire_file = entrire_file + (line.replace("\n", '').replace('  ', ''))

        if entrire_file != "":
            all_user = json.loads(entrire_file)
            for user in all_user:
                local_list.append(UserInfo(user['id'], user['name']))

        return local_list

    # Save all knwon user in the json file
    def save_users(self) -> None:
        users_in_file = open(self.file_name, 'w')

        json_users = []
        for user in self.local_list:
            json_users.append(user.user_to_table())

        users_in_file.write(json.dumps(json_users, indent=2))

        users_in_file.close()

class UserInfo:
    def __init__(self, id:int, name:str) -> None:
        self.id = id
        self.name = name

    # Check if self and other are the same user
    def same_user(self, other) -> bool:
        return self.id == other.id

    # Create a dictionary
    def user_to_table(self) -> dict:
        return { 
            'id': self.id, 
            'name': self.name
        }

    # Json string
    def user_to_json(self) -> str:
        return json.dumps(self.user_to_table())