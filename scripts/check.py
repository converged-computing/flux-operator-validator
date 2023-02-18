#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import tempfile
import jinja2

here = os.path.dirname(os.path.abspath(__file__))

template_file = os.path.join(here, "template.sh")
if not os.path.exists(template_file):
    sys.exit(f"{template_file} does not exist.")


def read_file(filename):
    with open(filename, "r") as fd:
        content = fd.read()
    return content


template = read_file(template_file)


def write_file(content, filename):
    with open(filename, "w") as fd:
        fd.write(content)


def get_parser():
    parser = argparse.ArgumentParser(
        description="Flux Operator Validator",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("container", help="container to check")
    parser.add_argument(
        "--pre-command",
        dest="pre_command",
        help="script pre-commands to run to setup environment, etc. Would be container->preCommand or container->commands->pre in operator",
    )
    parser.add_argument(
        "--time",
        default=False,
        action="store_true",
        help="check for time requirements",
    )
    parser.add_argument(
        "--debug",
        default=False,
        action="store_true",
        help="print debug info for script",
    )
    return parser


class FluxOperatorValidator:
    """
    Check your Flux Operator container for basic requirements.
    """

    def __init__(self, debug=False):
        self.debug = debug

    def check(self, container, pre_command=None, time=False):
        """
        Basic checks that a container is valid for the Flux Operator

        This script simply populates and runs a validation script, prints the
        output, and reports the return code.
        """
        print(f"⚙️ Pulling {container}")
        subprocess.run(["docker", "pull", container], check=True)

        commands = "" if not time else " time"
        if pre_command and os.path.exists(pre_command):
            pre_command = read_file(pre_command)

            # Get rid of hashbang
            if pre_command.startswith("#!"):
                pre_command = "\n".join(pre_command.split("\n")[1:])

        render = jinja2.Template(template).render(
            {"preCommand": pre_command, "commands": commands}
        )
        if self.debug:
            print(f"\n{render}\n")

        tempdir = tempfile.mkdtemp(prefix="flux-operator-validator-")
        tmpfile = os.path.join(tempdir, "entrypoint.sh")
        write_file(render, tmpfile)
        res = subprocess.run(
            [
                "docker",
                "run",
                "-it",
                "-v",
                f"{tempdir}:/tmp/flux-operator-validator",
                "--entrypoint",
                "/bin/bash",
                container,
                "/tmp/flux-operator-validator/entrypoint.sh",
            ],
            check=True,
        )
        os.remove(tmpfile)
        sys.exit(res.returncode)

        # python .github/scripts/check.py ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0


def main():
    parser = get_parser()

    # If an error occurs while parsing the arguments, the interpreter will exit with value 2
    args, extra = parser.parse_known_args()

    # Show args to the user
    print("    container: %s" % args.container)
    print("   preCommand: %s" % args.pre_command)
    print("         time: %s" % args.time)

    if args.pre_command and not os.path.exists(args.pre_command):
        sys.exit(
            f"preCommand is provided as {args.pre_command} but not does exist as a file."
        )

    cli = FluxOperatorValidator()
    cli.check(args.container, args.pre_command, args.time)


if __name__ == "__main__":
    main()
