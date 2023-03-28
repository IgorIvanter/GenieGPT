# [Bot]: Yes, creating a class to handle the user data and file operations is a good way to encapsulate the functionality and make it reusable. Here's an example implementation:

import pickle
import os


class UserDataProvider:
    def __init__(self, file_path):
        # Define the file path to store the user data
        self.file_path = file_path
        # Create path if it doesn't exist
        if not os.path.exists(os.path.dirname(self.file_path)):
            os.makedirs(os.path.dirname(self.file_path))
        # Create a dictionary to hold the user data
        self.user_data_dict = {}
        # Load the user data from file
        self._load_user_data()

    def _load_user_data(self):
        try:
            with open(self.file_path, 'rb') as f:
                data = pickle.load(f)
                self.user_data_dict.update(data)
        except FileNotFoundError:
            pass

    def _save_user_data(self):
        with open(self.file_path, 'wb') as f:
            pickle.dump(self.user_data_dict, f)

    def update_user_data(self, user_id, has_paid_plan=False, num_requests=0):
        self.user_data_dict[user_id] = {
            "has_paid_plan": has_paid_plan,
            "num_requests": num_requests
        }
        self._save_user_data()

    def get_user_data(self, user_id):
        # Return a copy of the user data (to prevent accidental modification)
        return self.user_data_dict.get(user_id, {}).copy()


# In this implementation, the UserDataProvider class encapsulates all of the functionality for loading and saving user data to the file. The __init__() method loads the user data from the file, while the _load_user_data() method does the actual loading from the file.

# The update_user_data() method updates the user data with the provided has_paid_plan and num_requests values for the given user_id. The updated user data is then saved to the file using the _save_user_data() method.

# The get_user_data() method retrieves the data for the provided user_id and returns a copy of the dictionary to prevent accidental modification.

# By defining all of this functionality within a class, you can create an instance of the UserDataProvider class for each Telegram bot and reuse it throughout your code. For example, you could create and reuse a UserDataProvider instance for each of your bot's commands or handlers.
