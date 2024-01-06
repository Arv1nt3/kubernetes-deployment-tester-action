# Kubernetes Deployment Tester

[![Test](https://github.com/Arv1nt3/kubernetes-deployment-tester-action/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/Arv1nt3/kubernetes-deployment-tester-action/actions/workflows/test.yml)

>[!CAUTION]
>**This Action is still in development!**

This GitHub Action deploys an application to a Kubernetes-in-Docker (Kind) cluster and performs a simple HTTP test to verify the deployment. It simplifies the process of setting up a Kind cluster, deploying a Kubernetes application, and conducting basic tests to ensure the application's functionality.

## Features

- **Kind Cluster Setup**: Automatically sets up a Kind cluster using [@helm/kind-action](https://github.com/helm/kind-action).
- **Application Deployment**: Deploys your application to the Kind cluster using a Kubernetes deployment configuration.
- **Testing**: Executes a basic test by making an HTTP request to the deployed application.

## Usage

### Pre-requisites
Create a workflow YAML file in your `.github/workflows` directory. An [example workflow](#example-workflow) is available below. For more information, see the GitHub Help Documentation for [Creating a workflow file](https://docs.github.com/en/actions/using-workflows#creating-a-workflow-file).

### Inputs

| Input              | Description                                                                                          | Required | Default  |
|--------------------|------------------------------------------------------------------------------------------------------|----------|----------|
| `image_name`       | The full name of the image (registry/image_name:tag).                                                | Yes      | N/A      |
| `registry_url`     | The URL of the registry.                                                                             | Yes      | `ghcr.io`|
| `registry_username`| The username for the registry.                                                                       | Yes      | N/A      |
| `registry_token`   | Token or password used to connect to the specified container registry.                               | Yes      | N/A      |
| `port`             | The port of the application.                                                                         | No       | `80`     |
| `path`             | The path to test, also used for readiness and liveness probes.                                       | No       | `/`      |
| `initialDelaySeconds` | Number of seconds after the container has started before liveness or readiness probes are initiated. | No | `5`   |
| `periodSeconds`    | How often (in seconds) to perform the probe. Minimum value is 1.                                     | No       | `10`     |

### Example Workflow

```yaml
name: Example Workflow

on: [push]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout Repository
      uses: actions/checkout@v2

    # ... steps to build and push your Docker image ...

    - name: Deploy and Test on Kind Cluster
      uses: Arv1nt3/kubernetes-deployment-tester-action@latest
      with:
        image_name: 'repository/your-username/your-application:tag'
        registry_url: 'ghcr.io'
        registry_username: ${{ github.actor }}
        registry_token: ${{ secrets.GITHUB_TOKEN }}
        port: '80' # optional, defaults to 80
        path: '/' # optional, defaults to /
        initialDelaySeconds: '5' # optional, defaults to 5
        periodSeconds: '10' # optional, defaults to 10
```
This example workflow will deploy your image from [ghcr.io](https://ghcr.io) to a Kind cluster and test it by making an HTTP request to the application's root path. If the request is successful, the workflow will complete successfully. If the request fails, the workflow will fail.

## Contributing

Contributions to this action are welcome! Please feel free to submit issues and pull requests. Thanks!
