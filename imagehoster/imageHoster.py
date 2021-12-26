from json.decoder import JSONDecodeError
from tddtnews.googleAuth import googleAuth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import json

class ImageHoster:

    def __init__(self):

        auth = googleAuth()
        #Resource for interacting with API
        self.service = build('drive', 'v3', credentials=auth.get_creds()) 
        
    def upload_image(self, name, path) -> bool:
        
        image = Image(name, path, self.service)
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

class Image:
      
    def __init__(self, name, path, service):
        self.name = name
        self.path = path
        try:
            file_metadata = {'name': self.name}
            media = MediaFileUpload(self.path)
            file = service.files().create(body=file_metadata,
                                                media_body=media,
                                                fields='id').execute()
            permissions = { "role": "reader", "type": "anyone" }
            self.id = file.get("id")
            service.permissions().create(fileId=self.id, body=permissions).execute()
        except:
            self.id = None
            
def main():
    host = ImageHoster()
    host.upload_image("logo", r"C:\Users\Benjamin\Desktop\Projects\Python\TDDTNews\images\logo400x400.jpg")