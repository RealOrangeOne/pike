from subprocess import check_output


def test():
    check_output(["./scripts/test.sh"])


def fix():
    check_output(["./scripts/fix.sh"])


def build():
    check_output(["./scripts/build.sh"])
