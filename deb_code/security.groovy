#!groovy

import jenkins.model.*
import hudson.security.*
import jenkins.security.s2m.AdminWhitelistRule
import com.cloudbees.plugins.credentials.impl.*;
import com.cloudbees.plugins.credentials.*;
import com.cloudbees.plugins.credentials.domains.*;
import com.cloudbees.jenkins.plugins.awscredentials.AWSCredentialsImpl
import jenkins.*
import hudson.*
import hudson.model.*
import jenkins.model.*

def instance = Jenkins.getInstance()

def hudsonRealm = new HudsonPrivateSecurityRealm(false)
hudsonRealm.createAccount("admin", "admin")
instance.setSecurityRealm(hudsonRealm)

def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
instance.setAuthorizationStrategy(strategy)
instance.save()

Jenkins.instance.getInjector().getInstance(AdminWhitelistRule.class).setMasterKillSwitch(false)

Credentials c = (Credentials) new UsernamePasswordCredentialsImpl(CredentialsScope.GLOBAL,"fea9daab76622804c537776c31d278bb", "GITHUB", "JENKINSFILE_REPO_USER_NAME", "Shalini2018")

Credentials c1  = (Credentials) new AWSCredentialsImpl(
CredentialsScope.GLOBAL,
"179ed1451138ed0b9a8e9667efe5e9b6", // id
"AKIAIAE32U66OXGDM6YQ", // accessKey
"6RpWi1pWT55GcFrTlfxGQvCPNAq9O4zg/7OkFJgg", // secretKey
"AWS Credentials"
)

SystemCredentialsProvider.getInstance().getStore().addCredentials(Domain.global(), c) 
SystemCredentialsProvider.getInstance().getStore().addCredentials(Domain.global(), c1)

a=Jenkins.instance.getExtensionList(hudson.tasks.Maven.DescriptorImpl.class)[0];
b=(a.installations as List);
b.add(new hudson.tasks.Maven.MavenInstallation("M3", "/usr/share/apache-maven", []));
a.installations=b
a.save()

instance = Jenkins.getInstance()
globalNodeProperties = instance.getGlobalNodeProperties()
envVarsNodePropertyList = globalNodeProperties.getAll(hudson.slaves.EnvironmentVariablesNodeProperty.class)

envVars = null
if ( envVarsNodePropertyList == null || envVarsNodePropertyList.size() == 0 ) {
  newEnvVarsNodeProperty = new hudson.slaves.EnvironmentVariablesNodeProperty();
  globalNodeProperties.add(newEnvVarsNodeProperty)
  envVars = newEnvVarsNodeProperty.getEnvVars()
} else {
  envVars = envVarsNodePropertyList.get(0).getEnvVars()  
}
envVars.put("AWS_ACCESS_KEY_ID", "AKIAIAE32U66OXGDM6YQ")
envVars.put("AWS_SECRET_ACCESS_KEY","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")
envVars.put("AWS_DEFAULT_REGION","us-east-1")
instance.save()

