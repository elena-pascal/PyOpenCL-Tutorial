# The simplest possible PyOpenCL program

import pyopencl as cl # access to the OpenCL parallel computation API

import numpy # The tools to create primitive numbers and arrays

context = cl.create_some_context()  # create a Context (one per computer)
queue = cl.CommandQueue(context)  # create a Command Queue (one per processor)
kernel = """__kernel void multiply(__global float* a, __global float* b, __global float* c)
{
    unsigned int i = get_global_id(0);
    c[i] = a[i] * b[i];
}"""  # The kernel is the C-ish code that will run on the GPU

program = cl.Program(context, kernel).build() # Compile the kernel into a Program
# ??? Why doesn't compilation require the name of a specific device ???
flags = cl.mem_flags

a = numpy.random.rand(10).astype(numpy.float32)
b = numpy.random.rand(10).astype(numpy.float32)  # Create two arrays of random floats

a_buffer = cl.Buffer(context, flags.COPY_HOST_PTR, hostbuf=a)
b_buffer = cl.Buffer(context, flags.COPY_HOST_PTR, hostbuf=b)
c_buffer = cl.Buffer(context, flags, b.nbytes)  # Allocate memory ???
# ??? Am I allocating this memory on the host, device, or both ???

program.multiply(queue, a.shape, None, a_buffer, b_buffer, c_buffer)
# call the program with arguments:
# queue - the command queue this program will be sent to
# a.shape - a tuple of the array's dimensions
# None - ???
# a.buffer, b.buffer, c.buffer - the three memory spaces this program deals with

c = numpy.empty_like(a) # Create a correctly-sized array
cl.enqueue_read_buffer(queue, c_buffer, c).wait()  # Execute everything and copy back c

print "a", a
print "b", b
print "c", c  # Print everything, to show the demo worked