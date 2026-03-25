# GitHub Workflow

Use this basic workflow when making changes:

1. Create a new branch for your work.
2. Make your code changes on that branch.
3. Commit and push the branch to GitHub.
4. Merge the branch into the main branch when the work is done.

## Safety Warning

Be careful with unstaged changes.

Before switching branches or pulling, check your work:

```bash
git status
```

If you have unfinished changes, commit them or stash them first.

## 1. Create a Branch

Start from the main branch and make sure it is up to date:

```bash
git checkout main
git pull origin main
```

**Warning:** do not run these commands if you have unstaged changes you want to keep. Check `git status` first.

Create and switch to a new branch:

```bash
git checkout -b your-branch-name
```

Use a clear branch name, for example:

```bash
feature/login-page
fix/navbar-bug
```

## 2. Push Code to the Branch

After making changes, stage and commit them:

```bash
git add .
git commit -m "Describe your changes"
```

Push the branch to GitHub:

```bash
git push -u origin your-branch-name
```

The `-u` links your local branch to the remote branch so future pushes can use:

```bash
git push
```

## 3. Merge the Branch with a Pull Request

When the branch is ready, merge it into `main` using a pull request.

1. Open the repository on GitHub.
2. Create a pull request from `your-branch-name` into `main`.
3. Review the changes.
4. Merge the pull request on GitHub.

## Quick Summary

```bash
git status
git checkout main
git pull origin main
git checkout -b your-branch-name

# make changes

git add .
git commit -m "Describe your changes"
git push -u origin your-branch-name

# when done
# open a pull request on GitHub and merge into main
```
