import json
import shutil
from distutils.dir_util import copy_tree

def service_start_ci(ec2_ip,build_job_name):
    file_text = "wget http://"+ec2_ip+":8080/jenkins/jnlpJars/jenkins-cli.jar"+'\n'+"sleep 5"+'\n'+"service docker start"+'\n'+"sleep 20"+'\n'+"jenkins-jobs update jobs"+'\n'+"sleep 20"+'\n'+"java -jar jenkins-cli.jar -s http://"+ec2_ip+":8080/jenkins build '"+build_job_name+"' --username admin --password admin"+'\n'+"sleep 5"+'\n'+"java -jar jenkins-cli.jar -s http://"+ec2_ip+":8080/jenkins/ console "+build_job_name+" -f --username admin --password admin"
    return file_text

def service_start_cd(ec2_ip,build_job_name,cd_job_name):
    file_text = "wget http://"+ec2_ip+":8080/jenkins/jnlpJars/jenkins-cli.jar"+'\n'+"sleep 5"+'\n'+"service docker start"+'\n'+"sleep 20"+'\n'+"jenkins-jobs update jobs"+'\n'+"sleep 20"+'\n'+"java -jar jenkins-cli.jar -s http://"+ec2_ip+":8080/jenkins build '"+build_job_name+"' --username admin --password admin"+'\n'+"sleep 5"+'\n'+"java -jar jenkins-cli.jar -s http://"+ec2_ip+":8080/jenkins/ console "+build_job_name+" -f --username admin --password admin"+'\n'+"sleep 20"+'\n'+"java -jar jenkins-cli.jar -s http://"+ec2_ip+":8080/jenkins build '"+cd_job_name+"' --username admin --password admin"+'\n'+"sleep 5"+'\n'+"java -jar jenkins-cli.jar -s http://"+ec2_ip+":8080/jenkins/ console "+cd_job_name+" -f --username admin --password admin"
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
    


