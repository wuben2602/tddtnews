from tddtnews.googleAuth import googleAuth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import json

class imageHoster:

    def __init__(self):

        auth = googleAuth()
        #Resource for interacting with API
        self.service = build('drive', 'v3', credentials=auth.get_creds()) 
        
    def upload_image(self, name, path):
        
        image = Image(name, path, self.service)
        #print(image.name, image.path, image.id)
        with open("assets\images.json", "r+") as f:
            img_dict = json.load(f)
            if image.name in img_dict or image.id is None:
                return False
            else:
                f.truncate(0)
                img_dict[image.name] = image.id
                json.dump(img_dict, f, sort_keys=True)
                return True
    
    def upload_image_dir(self, name, path):
        pass

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
            self.id = file.get("id")
        except:
            self.id = None
            
def main():
    host = imageHoster()