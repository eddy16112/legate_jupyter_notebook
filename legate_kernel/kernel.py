from ipykernel.kernelbase import Kernel
from pexpect import replwrap, EOF
import pexpect 

__version__ = '0.1.5'

class LegateKernel(Kernel):
    implementation = 'legate_kernel'
    implementation_version = __version__

    banner = "Legate iPython Kernel"
    language = 'python'
    language_version = __version__
    language_info = {'name': 'legate_python',
                     'mimetype': 'text/x-python',
                     'codemirror_mode': {
                        'name': 'ipython',
                        'version': 3
                        },
                     'pygments_lexer': 'ipython3',
                     'nbconvert_exporter': 'python',
                     'file_extension': '.py'}

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self._start_legate()

    def _start_legate(self):
        cmd = "legate"
        #cmd = "ch-run --set-env=/var/tmp/bburnett/ch-image/img/testing/ch/environment /var/tmp/bburnett/ch-image/img/testing/ -- /legate/bin/legate --cpus 16 --gpus 1 --sysmem 10000 --fbmem 15000"
        #cmd = "python"
        #replwrap documentation
        #https://pexpect.readthedocs.io/en/stable/api/replwrap.html
        self.legate_proc = pexpect.spawn(cmd, encoding='utf-8', echo=False)
        self.legate_python = replwrap.REPLWrapper(self.legate_proc, '>>> ', None, continuation_prompt='... ')
        #self.legate_python = replwrap.REPLWrapper(cmd, ">>> ", 'import sys; sys.ps1={0!r}; sys.ps2={1!r}')

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        status = 'ok'
        """
        jupyter sends results in the form of
        'line1\nline2:\n    line2continuation\nline3'
        need to make sure a newline is entered at the end
        so the replwrapper knows to enter the command.
        if there are two newline chars it doesn't hurt
        so I'm being lazy and not checking.
        """
        output = self.legate_python.run_command(code + '\r\n')
        #Check and make sure the pexpect didn't die
        if self.legate_python.child.exitstatus == None and self.legate_python.child.signalstatus == None:
            status = 'error'
        if not silent:
            stream_content = {'name': 'stdout', 'text': output}
            #stream_content = {'name': 'stdout', 'text': repr(code)} #debug
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': status,
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
                }

if __name__ == "__main__":
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=LegateKernel)
