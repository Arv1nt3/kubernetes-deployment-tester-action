import os
import yaml

def create_yaml_file(filename, content):
    with open(filename, "w") as file:
        yaml.dump(content, file)

def main():
    # Service Account
    sa = {
        "apiVersion": "v1",
        "kind": "ServiceAccount",
        "metadata": {"name": "test"}
    }
    create_yaml_file("sa.yaml", sa)

    # Cluster Role Binding
    crb = {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "ClusterRoleBinding",
        "metadata": {"name": "test"},
        "subjects": [{"kind": "ServiceAccount", "name": "test", "namespace": "default"}],
        "roleRef": {"kind": "ClusterRole", "name": "cluster-admin", "apiGroup": "rbac.authorization.k8s.io"}
    }
    create_yaml_file("crb.yaml", crb)

    # Deployment
    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": "application", "labels": {"app": "application"}},
        "spec": {
            "replicas": 1,
            "selector": {"matchLabels": {"app": "application"}},
            "template": {
                "metadata": {"labels": {"app": "application"}},
                "spec": {
                    "containers": [{
                        "name": "application",
                        "image": os.environ["INPUT_IMAGE_NAME"],
                        "ports": [{"containerPort": int(os.environ.get("INPUT_PORT", 80))}],
                        "readinessProbe": {
                            "httpGet": {"path": os.environ.get("INPUT_PATH", "/"), "port": int(os.environ.get("INPUT_PORT", 80))},
                            "initialDelaySeconds": int(os.environ.get("INPUT_INITIALDELAYSECONDS", 5)),
                            "periodSeconds": int(os.environ.get("INPUT_PERIODSECONDS", 10))
                        },
                        "livenessProbe": {
                            "httpGet": {"path": os.environ.get("INPUT_PATH", "/"), "port": int(os.environ.get("INPUT_PORT", 80))},
                            "initialDelaySeconds": int(os.environ.get("INPUT_INITIALDELAYSECONDS", 5)),
                            "periodSeconds": int(os.environ.get("INPUT_PERIODSECONDS", 10))
                        },
                        "imagePullSecrets": [{"name": "registry-secret"}]
                    }]
                }
            }
        }
    }

    # Add command and args if provided
    if "INPUT_COMMAND" in os.environ:
        deployment["spec"]["template"]["spec"]["containers"][0]["command"] = [os.environ["INPUT_COMMAND"]]
    if "INPUT_ARGS" in os.environ:
        deployment["spec"]["template"]["spec"]["containers"][0]["args"] = os.environ["INPUT_ARGS"].split(",")

    # Add environment variables if provided
    if "INPUT_ENV_VARS" in os.environ:
        env_vars = [dict(pair.split("=")) for pair in os.environ["INPUT_ENV_VARS"].split(",")]
        deployment["spec"]["template"]["spec"]["containers"][0]["env"] = env_vars

    create_yaml_file("deployment.yaml", deployment)

if __name__ == "__main__":
    main()