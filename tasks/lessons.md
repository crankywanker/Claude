# Lessons Learned

## Never overwrite `.git/config` when forking another project into a repo

**Pattern:** Forking Shopify Dawn into an existing repo via `cp -r /tmp/dawn-src/. .`
silently merged Dawn's `.git/` over the existing `.git/`. This:
- Replaced the project's `remote.origin.url` with Dawn's (pointing at
  `Shopify/dawn.git`)
- Reset the fetch refspec to `+refs/heads/main:refs/remotes/origin/main`,
  which broke tracking-ref updates for all non-`main` branches —
  including the working branch — and caused the stop hook's
  "unpushed commits" warning to fire even after a successful push
- Almost destroyed the original branch had `HEAD` been overwritten

**Rule for next time:** When pouring an upstream snapshot into a repo,
remove the source's `.git` first:
```sh
git clone --depth 1 <upstream> /tmp/src
rm -rf /tmp/src/.git
cp -r /tmp/src/. .
```
Or use `rsync -a --exclude=.git /tmp/src/ ./` to be explicit.

If it's too late and `.git/config` is already merged:
1. `git remote set-url origin <correct-url>`
2. `git config --unset-all remote.origin.fetch`
3. `git config --add remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'`
4. `git fetch origin` to repopulate tracking refs

## Verify deferred environment dependencies before claiming done

The Shopify CLI was not in PATH at session start but was installable via
`npm install -g @shopify/cli`. Don't assume "tool not available" — try
installing the standard package first.

## When the task is bounded by claim language, encode the rule in code

Compliance for Blue Copper Labs prohibits drug claims in default copy.
A simple grep gate (`treat|cure|heal|stimulate|regrow|reverse damage|
clinically proven to`) catches violations. The catch: the *required*
FDA disclaimer uses these verbs in negation form ("not intended to
diagnose, treat, cure..."). Both can be true: the grep flags candidates,
a human confirms each match is either copy that needs rewriting or the
required negation form.
