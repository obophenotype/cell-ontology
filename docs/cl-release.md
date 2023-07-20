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

### Preparation 

Preparation:

1. Ensure that all your pull requests are merged into your main (master) branch
1. Make sure that all changes to master are committed to Github (`git status` should say that there are no modified files)
1. Locally make sure you have the latest changes from master (`git pull`)
1. Checkout a new branch (e.g. `git checkout -b release-2021-01-01`)
1. You may or may not want to refresh your imports as part of your release strategy (see [here](UpdateImports.md))(Note: in CL we decouple our imports and releases - we hence advice that you do not update imports)
1. Make sure you have the latest ODK installed by running `docker pull obolibrary/odkfull`

To actually run the release, you:

1. Open a command line terminal window and navigate to the src/ontology directory (`cd cl/src/ontology`)
1. Run the release using `sh run.sh make cl DEPLOY_GH=false`. This will build all files and copy them to the correct place. (Note: the `IMP=false` is used to decouple imports refresh with release)
1. Review the release as per the `review release` section in [ODK-workflow release document](odk-workflows/ReleaseWorkflow.md)
1. Create a pull request and get a second set of eyes to review it. As CL uses a custom release pipeline, we ask that you get at least one core developer to review it too.
1. Merge to main branch once reviewed and CI checks have passed
1. Deploy release on GitHub by running `make deploy_release GHVERSION="v2022-06-20"` on the release branch (DO NOTE CHANGE TO MAIN BRANCH!), replacing the date with the date of release (NOTE: no `sh run.sh`)
Editors note: ODK 1.3.2 will have a feature to run the release from inside the docker container. For now deploy_release has to be run outside.
1. This should end with a GitHub release link that looks something like:
```
https://github.com/obophenotype/cl/releases/tag/untagged-8935f3432525b27a0d84
``` 
Copy the link and paste it in your browser, this should show you a draft release. 
1. Click the edit button (the pencil button on the top right corner) and change the tag to the GHVERSION you entered above (eg v2022-06-20)
1. Change the `TBD.` in the main text to a summary of the main changes in the release if needed.
1. Scroll down all the way and click the `update release` button. 


