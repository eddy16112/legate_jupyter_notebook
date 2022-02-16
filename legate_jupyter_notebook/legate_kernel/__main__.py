from ipykernel.kernelapp import IPKernelApp
from .kernel import LegateKernel
IPKernelApp.launch_instance(kernel_class=LegateKernel)
