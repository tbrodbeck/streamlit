# ds-bootcamp-mvp
## Simple deployment on OCP
Connect to project:
```sh
oc get projects 
oc project <project name>
```
Deploy app:
```sh
oc new-app https://github.com/tbrodbeck/streamlit --name=$appname
oc expose svc/$appname # Create link to file for pod
```
