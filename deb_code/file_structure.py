import json
import shutil
from distutils.dir_util import copy_tree

def service_start():
    file_text = "service docker start"+'\n'+"jenkins-jobs update jobs"
    return file_text

def create_file(file_name,file_content):
    with open(file_name, 'w') as file_to_write:
        file_to_write.write(file_content)
    return 'Yes'

def move_file(file_name,move_to_path):
    shutil.move(file_name,move_to_path)
    return 'Yes'

def copy_file(file_name,move_to_path):
    shutil.copyfile(file_name,move_to_path)
    return 'Yes'

def copy_folder(folder_name,move_to_path):
    copy_tree(folder_name, move_to_path)
    return 'Yes'

def write_file_in_location(file_name,file_path,file_content):
    file_detail = file_path+'/'+file_name
    with open(file_detail, "w") as text_file:
        text_file.write(file_content)
    


