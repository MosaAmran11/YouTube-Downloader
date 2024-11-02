import winreg as reg


class Paths:
    registry_folder_names: [str, str] = {
        'Downloads': '{374DE290-123F-4565-9164-39C4925E467B}',
        'Saved Games': '{4C5C32FF-BB9D-43B0-B5B4-2D72E54EAAA4}',
        'Contacts': '{56784854-C6CB-462B-8169-88E350ACB882}',
        'Searches': '{7D1D3A04-DEBB-4115-95CF-2F29DA2920DA}',
        'Documents': 'Personal',
        'Music': 'My Music',
        'Pictures': 'My Pictures',
        'Videos': 'My Video'
    }

    def __init__(self):
        pass

    @classmethod
    def get_referenced_folder(cls, folder_name: str):
        try:
            # Open the registry key for the current user
            with reg.OpenKey(reg.HKEY_CURRENT_USER,
                             r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as registry_key:
                # Read the value for the Downloads folder
                folder_path, regtype = reg.QueryValueEx(registry_key, folder_name)
                return folder_path
        except FileNotFoundError:
            original_folder_name: str = next(
                (key for key, val in cls.registry_folder_names.items() if val == folder_name), None)
            print(f"{original_folder_name} folder entry not found in the registry.")
            return None


