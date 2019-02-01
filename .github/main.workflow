workflow "New workflow" {
  on = "push"
  resolves = ["mariamrf/py-package-publish-action@master"]
}

action "mariamrf/py-package-publish-action@master" {
  uses = "mariamrf/py-package-publish-action@master"
  secrets = ["TWINE_PASSWORD", "TWINE_USERNAME"]
  env = {
    BRANCH = "master"
    PYTHON_VERSION = "3.6.0"
  }
}
