from json.decoder import JSONDecodeError
from tddtnews.googleAuth import googleAuth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import json

class imageHoster:

    def __init__(self):

        auth = googleAuth()
        #Resource for interacting with API
        self.service = build('drive', 'v3', credentials=auth.get_creds()) 
        
    def upload_image(self, name, path, folder_id):
        
        image = Image(name, path, self.service, folder_id)
        with open("assets\images.json", "r") as f:
            try:
                img_dict = json.load(f)
            except JSONDecodeError:
                img_dict = dict()
        if image.name in img_dict or image.id is None:
            return False
        with open("assets\images.json", "w") as f:
            img_dict[image.name] = image.id
            json.dump(img_dict, f, sort_keys=True)
            return True
    
    def upload_image_dir(self, name, path):
        pass

class Image:
      
    def __init__(self, name, path, service, folder_id):
        self.name = name
        self.path = path
        try:
            file_metadata = {'name': self.name, 'parents':[folder_id]}
            media = MediaFileUpload(self.path)
            file = service.files().create(body=file_metadata,
                                                media_body=media,
                                                fields='id').execute()
            self.id = file.get("id")
        except:
            self.id = None
            
def main():
    host = imageHoster()
    host.upload_image("test1", "images\\bad.jpg", "1lnDKA8Mc9cuQuj0FJImL-ZQlgKm8UCaw")
    host.upload_image("test2", "images\\logo400x400.jpg", "1lnDKA8Mc9cuQuj0FJImL-ZQlgKm8UCaw")