import os
import json
import file_structure
import shutil
import sys
import binascii
import subprocess
import time
import codecs
import urllib2

application_name = sys.argv[1]

current_public_ip = subprocess.check_output('curl ident.me', shell=True)
print("The Public IP is: "+current_public_ip)

config_file_name = 'za_'+application_name+'_config.json'

with open(config_file_name) as config_file:
    config_data = json.load(config_file)

print('The Application Name is: '+ '\033[1m'+'\033[92m'+ config_data["application"]+'\x1b[0m')

directory_name = config_data["application"]+'_codes'

if not os.path.exists(directory_name):
    os.makedirs(directory_name)

if  config_data["run_cd_consecutively"] =='yes':
    text_service_start = file_structure.service_start_cd(current_public_ip,str(config_data["build_job_CI"]),str(config_data["build_job_CD"]))
else:
    text_service_start = file_structure.service_start_ci(current_public_ip,str(config_data["build_job_CI"]))

cwd = os.getcwd()
    
create_file_out=file_structure.create_file("utility.sh",text_service_start)
move_file_out=file_structure.move_file(cwd+'/'+"utility.sh",cwd+'/'+directory_name+'/'+"utility.sh")

copy_folder_out=file_structure.copy_folder(cwd+'/'+"plugins",cwd+'/'+directory_name+'/'+"plugins")

with open(cwd+'/'+'security.groovy', 'r') as groovy_file:
    groovy_content = str(groovy_file.read())

groovy_content = str.replace(groovy_content,"JENKINSFILE_REPO_USER_NAME",str(config_data["repo_credentials"]["user_name"]))
groovy_content = str.replace(groovy_content,"JENKINSFILE_REPO_PWD",str(config_data["repo_credentials"]["password"]))
groovy_content = str.replace(groovy_content,"AWS_ACCESS_KEY_ID_VAL",str(config_data["aws_info"]["AWS_ACCESS_KEY_ID"]))
groovy_content = str.replace(groovy_content,"AWS_SECRET_ACCESS_KEY_VAL",str(config_data["aws_info"]["AWS_SECRET_ACCESS_KEY"]))
groovy_content = str.replace(groovy_content,"AWS_DEFAULT_REGION_VAL",str(config_data["aws_info"]["AWS_DEFAULT_REGION"]))

hex_git_id = binascii.b2a_hex(os.urandom(16))
hex_aws_id = binascii.b2a_hex(os.urandom(16))

groovy_content = str.replace(groovy_content,"RANDOM_GIT_ID",hex_git_id)
groovy_content = str.replace(groovy_content,"RANDOM_AWS_ID",hex_aws_id)

write_groovy_file = file_structure.write_file_in_location("security.groovy",cwd+'/'+directory_name,groovy_content)
print('\033[33m'+'Groovy File Created'+'\x1b[0m')


with open(cwd+'/'+'Dockerfile_template.txt','r') as docker_file:
    docker_content = str(docker_file.read())

docker_content = str.replace(str(docker_content),"SOURCE_YAML", directory_name+'/'+ "jenkins.yaml")
docker_content = str.replace(str(docker_content),"DESTINATION_YAML",str("/var/lib/jenkins/jobs/jenkins.yaml"))




docker_content = str.replace(str(docker_content),"SRC_PROJ_YAML", directory_name+'/'+ "projects.yaml")
docker_content = str.replace(str(docker_content),"DEST_PROJ_YAML",str("/var/lib/jenkins/jobs/projects.yaml"))


docker_content = str.replace(str(docker_content),"SOURCE_INI", directory_name+'/'+ "jenkins_jobs.ini")
docker_content = str.replace(str(docker_content),"DESTINATION_INI",str("/etc/jenkins_jobs/jenkins_jobs.ini"))
docker_content = str.replace(str(docker_content),"UTILITY_TEMPLATE_PATH", directory_name+'/'+ "utility.sh")

write_docker_file = file_structure.write_file_in_location("Dockerfile",cwd+'/'+directory_name,docker_content)


with open(cwd+'/'+'jenkins_job_template.txt', 'r') as jenkins_yaml_file:
    jenkins_yaml_content = str(jenkins_yaml_file.read())

'''jenkins_yaml_content = str.replace(jenkins_yaml_content,"JENKINS_JOB_NAME",str(config_data["build_job_name"]))'''
jenkins_yaml_content = str.replace(jenkins_yaml_content,"JENKINS_JOB_DESCRIPTION",str(config_data["build_job_description"]))
jenkins_yaml_content = str.replace(jenkins_yaml_content,"JENKINS_FILE_URL",str(config_data["jenkins_file_url"]))
jenkins_yaml_content = str.replace(jenkins_yaml_content,"JENKINS_GIT_CREDENTIALS",hex_git_id)

write_yaml_file = file_structure.write_file_in_location("jenkins.yaml",cwd+'/'+directory_name,jenkins_yaml_content)

with open(cwd+'/'+'jenkins_auth_template.txt', 'r') as jenkins_auth_file:
    jenkins_auth_content = str(jenkins_auth_file.read())

jenkins_yaml_content = str.replace(jenkins_auth_content,"EC2_PUBLICIP",current_public_ip)
write_ini_auth_file = file_structure.write_file_in_location("jenkins_jobs.ini",cwd+'/'+directory_name,jenkins_yaml_content)


with open(cwd+'/'+'jenkins_project_template.txt', 'r') as jenkins_proj_file:
     jenkins_proj_content = str(jenkins_proj_file.read())

jenkins_proj_content = str.replace(jenkins_proj_content,"JENKINS_JOB_CI",str(config_data["build_job_CI"]))
jenkins_proj_content = str.replace(jenkins_proj_content,"JENKINS_JOB_CD",str(config_data["build_job_CD"]))



write_yaml_file = file_structure.write_file_in_location("projects.yaml",cwd+'/'+directory_name,jenkins_proj_content)




print('\033[33m'+'Jenkins Configuration Setup Completed'+'\x1b[0m')

print('\033[43m'+'Creating Docker Image ....'+'\x1b[0m')
time.sleep(5)
build_image_cmd = "sudo docker build -t mavenenv:latest -f "+directory_name+"/Dockerfile ."
build_image = subprocess.call(build_image_cmd, shell=True)
print('\033[42m'+'Docker Image Created with Name: '+'mavenenv:latest'+'\x1b[0m')

print('\033[45m'+'Creating Container ....'+'\x1b[0m')
time.sleep(5)
initiate_container_cmd = "sudo docker run -d --privileged -e AWS_ACCESS_KEY_ID="+str(config_data["aws_info"]["AWS_ACCESS_KEY_ID"])+" -e AWS_SECRET_ACCESS_KEY="+str(config_data["aws_info"]["AWS_SECRET_ACCESS_KEY"])+" -e AWS_DEFAULT_REGION="+str(config_data["aws_info"]["AWS_DEFAULT_REGION"])+" -p 8080:8080 mavenenv:latest"
container_id = subprocess.check_output(initiate_container_cmd, shell=True)
print('\033[42m'+"Container Created with ID: "+container_id+'\x1b[0m')

print('\033[44m'+'Launching Jenkins and Executing Jenkins Build ....'+'\x1b[0m')
time.sleep(3)
execute_pipeline_cmd = "sudo docker exec -ti "+str.replace(container_id,'\n','')+" sh utility.sh"
print("Utility run command: "+execute_pipeline_cmd)
time.sleep(20)
execute_pipeline = subprocess.call(execute_pipeline_cmd, shell=True)
print('\033[93m'+"Build Job Completed. Confirming Build Job Status ..."+'\x1b[0m')

build_confirm_url = "http://"+current_public_ip+":8080/jenkins/job/"+str(config_data["build_job_CI"])+"/lastBuild/api/json"
try:
    fRead = urllib2.urlopen(build_confirm_url, None, 30);
except:
    raise
jsonResponse = json.loads(fRead.read());
fRead.close();
jobStatus = jsonResponse["result"]

if jobStatus == 'SUCCESS':
    print('\033[42m'+"Build Job Completed: "+'\033[1m'+"SUCCESSFULLY"+'\x1b[0m')
else:
    print('\033[41m'+"Build Job Completed: "+'\033[1m'+"IN ERROR"+'\x1b[0m')
