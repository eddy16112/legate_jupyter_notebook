#Thanks go to the bash_kernel for how to do this

import json
import os
import sys
import argparse

from jupyter_client.kernelspec import KernelSpecManager
from IPython.utils.tempdir import TemporaryDirectory

kernel_json = {"argv": [sys.executable, "-m", "legate_kernel", "-f", "{connection_file}"],
    "display_name":"LegatePython",
    "language":"python",
}

def install_my_kernel_spec(user=True, prefix=None):
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755)
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(kernel_json, f, sort_keys=True)

        print("Installing IPython kernel spec")
        KernelSpecManager().install_kernel_spec(td, 'legate_python', user=user, prefix=prefix)

def _is_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False

def main(argv=None):
    parser = argparse.ArgumentParser(
        description='Install KernelSpec for LegatePython Kernel'
    )
    prefix_locations = parser.add_mutually_exclusive_group()

    prefix_locations.add_argument(
        '--user',
        help='Install KernelSpec in user home directory',
        action='store_true'
    )
    prefix_locations.add_argument(
        '--sys-prefix',
        help='Install KernelSpec in sys.prefix. Useful in Conda/venv',
        action='store_true',
        dest='sys_prefix'
    )
    prefix_locations.add_argument(
        '--prefix',
        help='Install KernelSpec in this prefix',
        default=None
    )

    args = parser.parse_args(argv)

    user = False
    prefix = None
    if args.sys_prefix:
        prefix = sys.prefix
    elif args.prefix:
        prefix = args.prefix
    elif args.user or not _is_root():
        user = True

    install_my_kernel_spec(user=user, prefix=prefix)

if __name__ == '__main__':
    main()
