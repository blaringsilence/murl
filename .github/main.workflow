workflow "New workflow" {
  on = "push"
  resolves = ["mariamrf/pypi-publish-action@master"]
}

action "mariamrf/pypi-publish-action@master" {
  uses = "mariamrf/pypi-publish-action@master"
  secrets = ["TWINE_PASSWORD", "TWINE_USERNAME"]
  env = {
    BRANCH = "master"
    PYTHON_VERSION = "3.6.0"
  }
}
