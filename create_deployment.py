import os
import yaml

def get_env_var(env_var, required, default=None):
    value = os.getenv(env_var)
    if required and not value:
        raise ValueError(f"Required environment variable '{env_var}' is missing.")
    return value if value else default

def create_deployment_yaml(image_name, command, args, env_vars, port, path, initial_delay_seconds, period_seconds):
    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": "application",
            "labels": {
                "app": "application"
            }
        },
        "spec": {
            "replicas": 1,
            "selector": {
                "matchLabels": {
                    "app": "application"
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": "application"
                    }
                },
                "spec": {
                    "containers": [{
                        "name": "application",
                        "image": image_name,
                        "ports": [{"containerPort": port}],
                        "command": [command] if command else None,
                        "args": args.split(',') if args else [],
                        "env": yaml.safe_load(env_vars) if env_vars else [],
                        "readinessProbe": {
                            "httpGet": {
                                "path": path,
                                "port": port
                            },
                            "initialDelaySeconds": initial_delay_seconds,
                            "periodSeconds": period_seconds
                        },
                        "livenessProbe": {
                            "httpGet": {
                                "path": path,
                                "port": port
                            },
                            "initialDelaySeconds": initial_delay_seconds,
                            "periodSeconds": period_seconds
                        }
                    }],
                    "imagePullSecrets": [{"name": "registry-secret"}]
                }
            }
        }
    }

    with open('deployment.yaml', 'w') as file:
        yaml.dump(deployment, file)

# Read inputs from environment variables
image_name = get_env_var('INPUT_IMAGE_NAME', True)
command = get_env_var('INPUT_COMMAND', False)
args = get_env_var('INPUT_ARGS', False)
env_vars = get_env_var('INPUT_ENV_VARS', False)
port = int(get_env_var('INPUT_PORT', False, 80))
path = get_env_var('INPUT_PATH', False, "/")
initial_delay_seconds = int(get_env_var('INPUT_INITIALDELAYSECONDS', False, 5))
period_seconds = int(get_env_var('INPUT_PERIODSECONDS', False, 10))

create_deployment_yaml(image_name, command, args, env_vars, port, path, initial_delay_seconds, period_seconds)
