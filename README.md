# Kubernetes Deployment Tester

[![Test](https://github.com/Arv1nt3/kubernetes-deployment-tester-action/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/Arv1nt3/kubernetes-deployment-tester-action/actions/workflows/test.yml)

This GitHub Action deploys an application using a Docker image to a Kubernetes-in-Docker (Kind) cluster and performs a simple HTTP request to verify the deployment.

## Features

- **Kind Cluster Setup**: Automatically sets up a Kind cluster using [@helm/kind-action](https://github.com/helm/kind-action) and uses the same parameters.
- **Application Deployment**: Deploys your application to the Kind cluster using a Kubernetes deployment configuration.
- **Testing**: Executes a basic test by making an HTTP request to the deployed application.

## Usage

### Pre-requisites
Create a workflow YAML file in your `.github/workflows` directory. [Example workflows](#example-workflow) are available below. For more information, see the GitHub Help Documentation for [Creating a workflow file](https://docs.github.com/en/actions/using-workflows#creating-a-workflow-file).

### Inputs

| Input              | Description                                                                                          | Required | Default  |
|--------------------|------------------------------------------------------------------------------------------------------|----------|----------|
| `image_name`       | The full name of the image (registry/image_name:tag).                                                | Yes      | N/A      |
| `use_local_image`       | Set to true to use a local Docker image with 'kind load docker-image', false to pull from registry.                                                | Yes      | `false`      |
| `cluster_config`       | Path to the Kind config file.                                                | No      | N/A      |
| `registry_url`     | The URL of the registry.                                                                             | No      | `ghcr.io`|
| `registry_username`| The username for the registry.                                                                       | No      | N/A      |
| `registry_token`   | Token or password used to connect to the specified container registry.                               | No      | N/A      |
| `command`   | Command to run at container startup. Check [example workflows](#example-workflows) to see the exact format expected.                               | No      | N/A      |
| `args`   | Arguments for the command. Check [example workflows](#example-workflows) to see the exact format expected.                               | No      | N/A      |
| `env_vars`   | Environment variables in YAML format. Check [example workflows](#example-workflows) to see the exact format expected.                               | No      | N/A      |
| `port`             | The port of the application.                                                                         | No       | `80`     |
| `path`             | The path to test, also used for readiness and liveness probes.                                       | No       | `/`      |
| `timeoutSeconds` | Number of seconds to wait for the pod to start. | No | `20`   |
| `initialDelaySeconds` | Number of seconds after the container has started before liveness or readiness probes are initiated. | No | `5`   |
| `periodSeconds`    | How often (in seconds) to perform the probe. Minimum value is 1.                                     | No       | `10`     |

### Example Workflows

#### Using the action with a local image
```yaml
name: Example Workflow with local image

on: [push]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout Repository
      uses: actions/checkout@v2

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3.0.0

    - name: Build image and load locally
      run: |
        docker buildx build \
          --file ./Dockerfile \
          --tag <repo_url>/<username>/<image_name>:<tag> \
          --load \
          .

    - name: Deploy and Test on Kind Cluster
      uses: Arv1nt3/kubernetes-deployment-tester-action@latest
      with:
        image_name: '<repo_url>/<username>/<image_name>:<tag>' # required
        use_local_image: true # required
        cluster-config: './path/to/your/kind/config' # optional
        registry_url: 'ghcr.io' # optional
        registry_username: ${{ github.actor }} # optional
        registry_token: ${{ secrets.GITHUB_TOKEN }}  # optional
        command: 'your-command' # optional
        args: 'your-args' # optional
        env_vars: | # optional
          - name: YOUR_ENV_VAR
            value: "YourValue"
        port: '80' # optional
        path: '/'  # optional
        timeoutSeconds: '20' # optional
        initialDelaySeconds: '5' # optional
        periodSeconds: '10' # optional
```
This example workflow will deploy your image loaded locally to a Kind cluster and test it by making an HTTP request to the application's root path. If the request is successful, the workflow will complete successfully. If the request fails, the workflow will fail.
#### Using the action with a registry image
```yaml
name: Example Workflow with registry image

on: [push]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout Repository
      uses: actions/checkout@v2

    - name: Build image and load locally
      run: |
        docker buildx build \
          --file ./Dockerfile \
          --tag <repo_url>/<username>/<image_name>:<tag> \
          --push \
          .

    - name: Deploy and Test on Kind Cluster
      uses: Arv1nt3/kubernetes-deployment-tester-action@latest
      with:
        image_name: '<repo_url>/<username>/<image_name>:<tag>' # required
        use_local_image: false # required
        cluster-config: './path/to/your/kind/config' # optional
        registry_url: 'ghcr.io' # optional
        registry_username: ${{ github.actor }} # optional
        registry_token: ${{ secrets.GITHUB_TOKEN }}  # optional
        command: 'your-command' # optional
        args: 'your-args' # optional
        env_vars: | # optional
          - name: YOUR_ENV_VAR
            value: "YourValue"
        port: '80' # optional
        path: '/'  # optional
        timeoutSeconds: '20' # optional
        initialDelaySeconds: '5' # optional
        periodSeconds: '10' # optional
```
This example workflow will deploy your image from [ghcr.io](ghcr.io) to a Kind cluster and test it by making an HTTP request to the application's root path. If the request is successful, the workflow will complete successfully. If the request fails, the workflow will fail.
## Contributing

Contributions to this action are welcome! Please feel free to submit issues and pull requests. Thanks!
