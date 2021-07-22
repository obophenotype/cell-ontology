# Introduction to Continuous Integration Workflows with ODK

Historically, most repos have been using Travis CI for continuous integration testing and building, but due to
runtime restrictions, we recently switched a lot of our repos to GitHub actions. You can set up your repo with CI by adding 
this to your configuration file (src/ontology/cl-odk.yaml):

```
ci:
  - github_actions
```

When [updateing your repo](RepoManagement.md), you will notice a new file being added: `.github/workflows/qc.yml`.

This file contains your CI logic, so if you need to change, or add anything, this is the place!

