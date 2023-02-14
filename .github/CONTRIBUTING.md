## Bug Reports

If you could, send pull requests, not bug reports. If you file a bug report, your issue should contain a title and a clear description of the issue. You should also include as much relevant information as possible and a code sample that demonstrates the issue.

## Which Branch?

All bug fixes should be sent to the **default** branch. Bug fixes should **never** be sent to the `master` or `main` branch unless they fix features that exist in the upcoming major release.

Minor features that are fully backward compatible with the current release should be sent to the **default** branch.

Major new features or features with breaking changes should always be sent to the `master` or `main` branch, which contains the upcoming major release.

## Coding Style

This repository accepts [black](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html) coding style. Don't worry if your code styling isn't perfect! Black-formatter CI will automatically merge any style fixes into the repository after pull requests are merged. 
