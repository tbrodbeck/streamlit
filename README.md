# ds-bootcamp-mvp
## Simple deployment on OCP
```sh
oc get projects 
oc project <project name>
oc new-app <github url from browser> --name=<appname>
oc expose svc/<appname> # Create link to file for pod
```
