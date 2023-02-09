## Bug Fixes

All bug fixes should be sent to the **default** branch. Bug fixes should **never** be sent to the `master` or `main` branch unless they fix features that 
exist in the upcoming major release.

## Minor Features

Minor features that are fully backward compatible with the current release should be sent to the **default** branch.

## Major Features

Major new features or features with breaking changes should always be sent to the `master` or `main` branch, which contains the upcoming major release.

## Pull Request Title 

Pull Request title should contain the sent branch e.g, if repository has `main(master)`, and `1.x` branches, and the current default branch of the 
repository be `1.x`:

- If you are sending pull request to the `1.x` branch, title should start with `[1.x]`, 
- If you are sending pull request to `master` or `main` branch, title should contain `[2.x]`.

## Coding Style

This repository accepts [black](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html) coding style. Don't worry if your code styling isn't perfect! Black-formatter CI will automatically merge any style fixes into the repository after pull requests are merged. 
