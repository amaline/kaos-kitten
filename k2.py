import requests
import getpass
import sys
import random
import time

defaultId=""
defaultPw=""
defaultApiEndpoint="https://api.cloud.gov"

api = str(raw_input("Enter api endpoint [{0}]: ".format(defaultApiEndpoint)) or defaultApiEndpoint)
info = api + "/v2/info"
infoResponse = requests.get(info)
auth=infoResponse.json()['authorization_endpoint']

print 'info endpoint: ', info
print 'auth endpoint: ', auth

id = str(raw_input("Enter user id: ") or defaultId)
p = str(getpass.getpass(stream=sys.stderr) or defaultPw)

oauthTokenResponse = requests.post(
    auth + '/oauth/token?grant_type=password&client_id=cf', 
    data={'username': id, 'password': p, 'client_id': 'cf'},
    auth=('cf', '')
)
authorization = oauthTokenResponse.json()['token_type'] + ' ' + oauthTokenResponse.json()['access_token']
requestHeaders={'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': authorization}
appsResponse = requests.get(api + "/v2/apps",headers=requestHeaders)

resources=appsResponse.json()['resources']


i=0

print
print "Applications"
print "------------"
for app in resources:
    guid = app['metadata']['guid']
    entity=app['entity']
    print "{2})  {0},       guid: {1},      instances: {3}".format(entity['name'],guid,i,entity['instances'])
    i+=1

print

kaosList = str(raw_input("Select applications to inject kaos (separate by space): ") )
kaosArray=list(map(lambda z: resources[int(z)] ,kaosList.split(" ") ))

print

killThisIteration=True;
while True:
    for j in kaosArray:
       name          = j['entity']['name']
       guid          = j['metadata']['guid']
       nbrOfInstances= j['entity']['instances']
       
       instanceReponse = requests.get(api + "/v2/apps/" + guid + "/instances",headers=requestHeaders)
       instances=instanceReponse.json()
       
       print "{0} has {1} instance(s)".format(name,nbrOfInstances)
       print "     ","   ".join(map(lambda z: instances[z]['state'],instances.keys()))

       if killThisIteration:
           killThisIteration=False
           killed=False
           for key in instances.keys():
               if random.randint(1,100) < 20:
                   killResponse = requests.delete(api + "/v2/apps/" + guid + "/instances/" + key,headers=requestHeaders)
                   print "      kill ", key, " response=",killResponse.status_code
                   killed=True
           print
           
           if killed:
               instanceReponse = requests.get(api + "/v2/apps/" + guid + "/instances",headers=requestHeaders)
               instances=instanceReponse.json()
               print "     ","   ".join(map(lambda z: instances[z]['state'],instances.keys()))
       else:
           print "\n     no killing this loop"
           killThisIteration=True
       
    print "\nsleep for one minutes\n"
    time.sleep(60)