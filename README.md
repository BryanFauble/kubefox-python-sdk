# Purpose
This is a WIP implementation of the KIT SDK for python. Most of this code is AI generated
based off the golang KIT SDK.


# Quickstart
- Create a virtual env with your preferred tool, ie: `pipenv shell`
- Install: `pip install .` or `pipenv install`
- Start the broker in debug mode in <https://github.com/xigxog/kubefox>
- Set up the require tokens (Below in the notes section) - UNSURE IF THIS IS NEEDED YET
- Run `implementing_kit.py`


# Linting/vscode extensions
- Black linter
- isort

# Notes:


Auto-generate files from .proto
python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. protobuf_msgs.proto
python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. broker_svc.proto


Running the python script locally and taking the hello-world creds:
sudo mkdir -p /var/run/secrets/kubernetes.io/serviceaccount/ && sudo chown ${USER}:${USER} /var/run/secrets/kubernetes.io/serviceaccount/
kubectl create token -n kubefox-debug hello-world-frontend-976e059 > /var/run/secrets/kubernetes.io/serviceaccount/token