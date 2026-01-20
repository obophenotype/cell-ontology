# ID management in CL

## Temporary IDs

“Temporary IDs” are an experimental mechanism to allow editors to mint
new term IDs without worrying about potential conflicting IDs.

This is primarily intended for AI agents, which are likely to open many
PRs in parallel but have to share a single ID range (contrary to human
editors, who all have their own range) and have no way of keeping track
of which IDs are being used in concurrent PRs (again contrary to human
editors, who can rely on Protégé for that).

However temporary IDs are in no way restricted to AI agents, and any
editor could use them if they so want. For example, they could be useful
for an _external_, _occasional_ editor – someone who is not a known
contributor to CL and for whom we may not necessarily want to allocate a
dedicated ID range.

### Editing the ontology with temporary IDs

From an editor’s point of view, all that is needed to use temporary IDs
is to use the `Temporary IDs` range defined in the `cl-idranges.owl`
file.

For editors using Protégé, this means selecting said `Temporary IDs`
range when Protégé asks you to select an ID range policy, just after
having opened the Uberon edit file.

For other editors (including AI agents), this means making sure that
whenever a new ID is needed, it is generated within the range allocated
to `Temporary IDs` (it should normally be `CL:99NNNNN`, but please check
the contents of the `cl-idranges.owl` file, just in case the range is
changed in the future).

### Replacing temporary IDs with definitive IDs

Replacing temporary IDs with definitive IDs is done by invoking the
`allocate-definitive-ids` target:

```sh
sh run.sh make allocate-definitive-ids
```

This will find all temporary IDs within the ontology and replace them
with newly allocated definitive IDs picked from within the `Automation`
range defined in the `cl-idranges.owl` file. All axioms that were
referring to temporary IDs will be automatically re-written so that they
refer to the corresponding newly allocated definitive IDs.

This replacement must be performed at the latest possible stage, just
before a PR is merged. If temporary IDs in a PR are replaced by
definitive IDs, and the PR is then left unmerged for a while, then ID
conflicts may occur when the PR is finally merged.

For convenience, a GitHub Actions workflow is available to perform the
ID replacement step on a PR without requiring a CL maintainer to
check out the PR and invoke the `allocate-definitive-ids` manually. When
a PR containing temporary IDs has been deemed OK for merging, a
maintainer should trigger the `allocate-definitive-ids` GitHub Actions
workflow on the PR’s branch, wait for that workflow to terminate (it
should take a couple of minutes at most), and then _immediately_ merge
the PR.

Of note, the `allocate-definitive-ids` GitHub Actions workflow requires
that a `ID_ALLOCATION_TOKEN` secret exist in the repository, associated
to an account that is allowed to push to the repository.

### Automatic replacement of temporary IDs upon pushing to master

Alternatively, a PR containing temporary IDs can be merged “as is” to
the master branch. This will then trigger an automatic ID replacement
operation (made by the same `allocate-definitive-ids` GitHub Actions
workflow), directly on the master branch.

Compared to the approach above, where the ID replacement is done on the
PR _prior to merging_, this approach has the following advantages:

* it is entirely automated, and does not require any manual intervention
  from a maintainer;
* it eliminates the risk of an ID conflict still occurring between the
  moment IDs are replaced on a PR and the moment the PR is merged.

It has the inconvenient that it lets temporary IDs becoming part of the
history of the master branch, which may make perusing the history more
cumbersome as the history will be “polluted” by commits that do nothing
more than rewriting IDs. With the “replace-before-merging” approach,
such commits can be made invisible if the PR is small enough to allow
for a “squash merge” instead of a normal merge – then only the
definitive IDs will only ever make it to the master branch.

This approach additionally requires that the account associated to the
`ID_ALLOCATION_TOKEN` secret be allowed to push to the repository’s
master branch (bypassing the branch protection normally in place in CL).
