node {
   echo 'Hello World**'
   def mvnHome
   def var
   def AWS_ACCESS_KEY_ID
   def AWS_SECRET_ACCESS_KEY
   def GIT_PWD
   def GIT_USER
   def GIT_URL
	   
   AWS_ACCESS_KEY_ID='AKIAIAE32U66OXGDM6YQ'
   AWS_SECRET_ACCESS_KEY='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'
   GIT_PWD='Shalini2018'
   GIT_USER='Shalini1989'
   GIT_URL='https://github.com/Shalini1989/SpringMvcSecurity.git'
   
	
	
   withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: '', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'], usernamePassword(credentialsId: '', passwordVariable: 'GIT_PWD', usernameVariable: 'GIT_USER')]) {
    // some block
}	
   git url: GIT_URL
	  
   mvnHome =  tool 'M3'
   stage('checkout/preparation')
   {  
       sh "rm -rf $WORKSPACE/*"	   
       checkout scm
   }
   stage('build') {
      // some block
	  // Run the maven build
         sh "'${mvnHome}/bin/mvn' -Dmaven.test.failure.ignore clean install"
    }
    stage('Result') {
       archive 'target/*.war'
       junit '**/target/surefire-reports/TEST-*.xml'
    }
    stage('uploadtoRepo'){
       s3Upload consoleLogLevel: 'INFO', dontWaitForConcurrentBuildCompletion: false, entries: [[bucket: 'outputs3jenkins', excludedFile: '', flatten: false, gzipFiles: false, keepForever: false, managedArtifacts: false, noUploadOnFailure: false, selectedRegion: 'us-east-1', showDirectlyInBrowser: false, sourceFile: '**/target/*.war', storageClass: 'STANDARD', uploadFromSlave: false, useServerSideEncryption: false]], pluginFailureResultConstraint: 'FAILURE', profileName: 's3', userMetadata: []    
    }
    stage('Build image') {
        /* This builds the actual image; synonymous to
         * docker build on the command line */
      //  app = docker.build("myimage")
      sh "docker build -t myrepo --rm=true ."
    }
    stage ('Docker push') {
       sh '''
         var=`aws ecr get-login --no-include-email --region us-east-1`
         eval $var
         docker tag myrepo:latest 085396960228.dkr.ecr.us-east-1.amazonaws.com/myrepo:latest
         docker push 085396960228.dkr.ecr.us-east-1.amazonaws.com/myrepo:latest
       '''
    //   docker.withRegistry('https://085396960228.dkr.ecr.us-east-1.amazonaws.com', 'ecr:us-east-1:demo-ecr-credential')
    //   docker.image('myrepo').push('latest')
  }
    
}
