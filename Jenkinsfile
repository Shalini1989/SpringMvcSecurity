node {
    def SERVICE_NAME
    def TASK_FAMILY
    def TASK_REVISION
    def DESIRED_COUNT
    git url: 'https://github.com/debgmail/SpringMvcSecurity.git'
    stage('checkout'){  
       sh "rm -rf $WORKSPACE/*"	   
       checkout scm
    }
    stage('Preparation') { // for display purposes          
      sh "echo '-------preparation start--------------------------'"
      //sh "/var/lib/jenkins/.local/bin/aws s3 cp s3://inputjenkinsbucket/myrepo-default-cluster.json $WORKSPACE/."
      sh "/var/lib/jenkins/.local/bin/aws ecr describe-repositories"
      sh "/var/lib/jenkins/.local/bin/aws ecr get-login --no-include-email >&1"
      sh "docker pull 085396960228.dkr.ecr.us-east-1.amazonaws.com/myrepo:latest"
      sh "echo '-------preparation end--------------------------'"
    }
    stage('Register task')
    {
        sh "/var/lib/jenkins/.local/bin/aws ecs register-task-definition --cli-input-json file://$WORKSPACE/config/myrepo-default-cluster.json"
    }
    stage('Run Service')
    {
        sh '''
           TASK_FAMILY='first-run-task-defination'
           TASK_REVISION=`/var/lib/jenkins/.local/bin/aws ecs describe-task-definition --task-definition myrepo | egrep 'revisio' | tr '/' ' ' | awk '{print $2}'  | sed 's/"$//' ` 
           DESIRED_COUNT='1'
           SERVICE_NAME='ecs-myrepo-service'
           echo `/var/lib/jenkins/.local/bin/aws ecs update-service --cluster default  --service ${SERVICE_NAME} --task-definition myrepo:${TASK_REVISION} --desired-count ${DESIRED_COUNT}`
        '''
    }
}
