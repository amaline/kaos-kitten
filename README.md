# kaos-kitten
Simple python script to inject kaos into cloud foundry applications in order to demonstrate cf resiliency

The script prompts for api endpoint, userid and password and queries the Cloud Foundry API for information on applications.
Selecting an application will cause a twenty percent chance that any instance in the application will be killed every two minutes.

The script loops every minute to show current status of application instances.

Ctrl-C to terminate

Example execution
```
amaline:~/workspace/kaos-kitten (master) $ python k2.py
Enter api endpoint [https://api.cloud.gov]: 
info endpoint:  https://api.cloud.gov/v2/info
auth endpoint:  https://login.cloud.gov
Enter user id: cloudfoundry@user.id
Password: 

Applications
------------
0)  app-a,       guid: 2fe0dada-cda2-495f-8979-4fc3836456b3,      instances: 2
1)  app-b,       guid: 3fcb037b-f607-4baf-85e7-074e3be8a675,      instances: 1
2)  app-c,       guid: 9355de32-5c19-4742-97fd-652acc1edc31,      instances: 1
3)  app-d,       guid: 4dc279c3-ed2e-42dd-b0fe-f510b243790e,      instances: 3
4)  app-e,       guid: 9585fe37-30dc-4086-8362-30c28716893e,      instances: 1
5)  app-f,       guid: cb5ee6bd-a045-46e8-929a-e3d1f99d952e,      instances: 3
6)  app-g,       guid: 99e1c6e4-b9e5-44c3-b33f-06e50eff8c6e,      instances: 1
7)  app-h,       guid: 499c7a3b-762b-498b-8a68-2b7c642264d0,      instances: 3

Select applications to inject kaos (separate by space): 7

app-h has 3 instance(s)
      RUNNING   RUNNING   RUNNING
      kill  2  response= 204

      RUNNING   RUNNING   DOWN

sleep for one minutes

app-h has 3 instance(s)
      RUNNING   RUNNING   DOWN

     no killing this loop

sleep for one minutes

app-h has 3 instance(s)
      RUNNING   RUNNING   RUNNING
```
