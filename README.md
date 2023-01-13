# !!THIS WORKFLOW IS DEPRECATED! SEE https://github.com/nrkno/github-action-vault-to-k8s-config FOR NEW WAY TO AUTHENTICATE


# github-workflow-vault-github-kubernetes-auth

Reusable GitHub workflow for automaticly authenticate to vault and get kubernetes credentials dynamicaly

## Usage

Reference this repository for a workflow job.

```yaml
jobs:
  ga-vault-k8s-auth:
    name: Github Actions to vault to kubernetes auth
    uses: nrkno/github-workflow-vault-github-kubernetes-auth/.github/workflows/workflow.yaml@v1
    with:
      # Working directory of this workflow
      # Default: .
      working-directory: .
      # Where should this job run
      # default: self-hosted
      runs-on: self-hosted
      # List of file to ignore (will be deleted before running steps)
      # Default: ""
      ignore-files: ""
      # Vault settings
      # Export vault-token as environemtn variable.
      vault-export-token: true
      # Vault role to use for authentication
      # Default: No default
      # required field!
      vault-role: ""
      # How long will ServiceAccount live
      # Default: "10m"
      vault-serviceaccount-ttl: "10m"
      # Should this be a clusterrolebinding?'
      # Default: false
      vault-cluster-role-binding: false
      ## Kubernetes settings
      # Name of cluster in which ServiceAccount will be created
      # Default: No default
      # required field!
      kubernetes-cluster-name: ""
      # Name of namespace to create ServiceAccount
      # Default: No default
      # required field!
      kubernetes-namespace: ""
      # name of template file for kube-config file
      # Default: config.tmpl
      kubernetes-config-template: config.tmpl
      # name of kube-config file
      # Default: config
      kubernetes-config: config
      # Name of script used for templating config file
      # Default: templating.py
      kubernetes-templating-script: templating.py
```

## Automatic ServiceAccounts from vault in selected kubernetes cluster

This workflow will create a ServiceAccount in provided cluster in `kubernetes-cluster-name` in the namespace set in `kubernetes-namespace`.  
In orderfor that to work, you first need to add these access definitions to Vault. This is done in [plattform-terraform-vault-config](https://github.com/nrkno/plattform-terraform-vault-config) repo.
Example:
```yaml
---
# Access to github-repo some-app
github_applications:
  some-app-github:
    prod:
      # Specify which repo and event/branch and so forth.
      github_subject: 'repo:nrkno/some-app:*'
      # Secret specific to this app will be available on secret/applications/some-app-github/prod
      application_secrets:
        access: read-only
      # Access to read Cluster specific information about selected cluster
      vault_application_shared_secret_paths:
        - access: read-only
          # set correct cluster after kuberntes-config/.
          path: kubernetes-config/name-of-cluster-to-use
      # This will create a serviceaccount on name-of-cluster-to-use in the namespace some-app with "edit" role
      kubernetes_roles:
        - role_name: edit
          allowed_namespaces:
            - some-app
          kubernetes_clusters:
            - name-of-cluster-to-use
```   

## Developing

The workflow definition resides in [.github/workflows/workflow.yaml](./.github/workflows/workflow.yaml).

## References

- https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#onworkflow_callinputs
- https://docs.github.com/en/actions/using-workflows/reusing-workflows
