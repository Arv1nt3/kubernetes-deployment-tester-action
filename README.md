# Kubernetes Deployment Tester

[![Test](https://github.com/Arv1nt3/kubernetes-deployment-tester-action/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/Arv1nt3/kubernetes-deployment-tester-action/actions/workflows/test.yml)

This GitHub Action deploys an application to a Kubernetes-in-Docker (Kind) cluster and makes a simple HTTP request to check if the application is up and running correctly. It's designed to simplify the process of setting up a Kind cluster, deploying a Kubernetes application, and executing a basic test to ensure the application is running as expected.

## Features

- **Kind Cluster Setup**: Automatically sets up a Kind cluster using. Uses [@helm/kind-action](https://github.com/helm/kind-action) to create the Kind cluster.
- **Application Deployment**: Deploys your application to the Kind cluster using a Kubernetes deployment configuration.
- **Testing**: Performs a basic test by making an HTTP request to the deployed application.

## Usage

### Pre-requisites
Create a workflow YAML file in your `.github/workflows` directory. An [example workflow](#example-workflow) is available below. For more information, reference the GitHub Help Documentation for [Creating a workflow file](https://docs.github.com/en/actions/using-workflows#creating-a-workflow-file).

### Inputs

| Input         | Description                                         | Required | Default |
|---------------|-----------------------------------------------------|----------|---------|
| `image-name`  | Full image name (repository/image_name:tag).              | Yes      | N/A     |
| `app-port`    | Application port.                                   | Yes      | N/A     |
| `github-token`| GitHub token, you can use the default token: `secrets.GITHUB_TOKEN`. | Yes | N/A |
| `timeout`     | Time to wait until testing the pod.                 | No       | `20s`   |

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
      uses: Arv1nt3/kubernetes-deployment-tester-action@v1.1.1
      with:
        image-name: 'repository/your-username/your-application:tag'
        app-port: '80'
        github-token: ${{ secrets.GITHUB_TOKEN }}
        timeout: '30s' # optional, 20s by default
```

## Contributing

Contributions to this action are welcome! Please feel free to submit issues and pull requests. Thanks!
