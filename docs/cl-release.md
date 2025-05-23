# CL Release workflow

While CL is an ODK ontology, it has a specific workflow for releases due to its large size and the limitations on standard GitHub releases.

## Requirements

Aside from the standard requirements needed for ODK workflow, `GH` is required. 
Instructions on how to install `GH` can be found [here](https://cli.github.com/manual/installation)

You will need to log in to your GitHub account on `GH` before you can uses it. To do this, enter the following in your terminal:
```
gh auth login
```

You can then follow instructions below for web browser login (or use your prefer means of logging in).
```
% gh auth login
? What account do you want to log into? GitHub.com
? What is your preferred protocol for Git operations? SSH
? Generate a new SSH key to add to your GitHub account? Yes
? Enter a passphrase for your new SSH key (Optional) 
? Title for your SSH key: GitHub SSH
? How would you like to authenticate GitHub CLI? Login with a web browser

! First copy your one-time code: XXXX-XXXX
Press Enter to open github.com in your browser... 
✓ Authentication complete.
- gh config set -h github.com git_protocol ssh
✓ Configured git protocol
✓ Uploaded the SSH key to your GitHub account: /Users/username/.ssh/id_ed25519.pub
✓ Logged in as username
```

## Release Process

The release is done in two parts:
1. Refresh the imports and the components (CellxGene subset, HRA subset and slims)
1. Generate the release artefacts

### Preparation 

1. Ensure that all pull requests to be included in the release are merged
1. Ensure that no other pull requests are merged during the release process
1. Ensure you are on the master branch and have locally the latest changes from master (`git pull`)
1. Ensure you have the latest ODK installed by running `docker pull obolibrary/odkfull`
1. Navigate to the cell-ontology/src/ontology directory (`cd src/ontology`)
1. Delete all temporary files (e.g., outdated plugins) by running `sh run.sh make clean`

### Refresh imports and components

1. Checkout a new branch (e.g. `git checkout -b refresh-imports-sept24`)
1. Run `sh run.sh make refresh-imports`
1. Have a sanity check in the files
1. Create a pull request and add at least a core editor as the reviewer
1. Merge to main branch once reviewed and CI checks have passed

### Generate the release artefacts

1. Ensure you are on the master branch and have locally the latest changes from master (`git pull`)
1. Checkout a new branch (e.g. `git checkout -b 20240904-release`)
1. Run the release using `sh run.sh make cl DEPLOY_GH=false`. This will build all files and copy them to the correct place.
1. Review the release as per the `Review the release` section in [ODK-workflow release document](odk-workflows/ReleaseWorkflow.md#review-the-release)
1. Create a pull request and get a second set of eyes to review it. As CL uses a custom release pipeline, we ask that you get at least one core developer to review it too.
1. Merge to main branch once reviewed and CI checks have passed
1. Deploy release on GitHub by running `make deploy_release GHVERSION="v2022-06-20"` on the release branch (DO NOTE CHANGE TO MAIN BRANCH!), replacing the date with the date of release (NOTE: no `sh run.sh`)
1. This should end with a GitHub release link that looks something like:`https://github.com/obophenotype/cl/releases/tag/untagged-8935f3432525b27a0d84`. Copy the link and paste it in your browser, this should show you a draft release. 
1. Click the edit button (the pencil button on the top right corner) and change the tag to the GHVERSION you entered above (eg v2022-06-20)
1. Change the `TBD.` in the main text to a summary of the main changes in the release if needed. Copy and paste the text and table from the `reports/summary_release.md` file. This file is in `.gitignore` and will only be available to those who have run the release.
1. Scroll down all the way and click the `update release` button. 


