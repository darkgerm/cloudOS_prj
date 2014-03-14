r"""Hyper Clustering Computing Module.

All the API should use ``uesrname`` to specify which master server is used. If
the username is not shown before, a new master server is established. The
username should matches the pattern ``[a-zA-Z0-9_]+``.

The return value is in the format of Python object. And it must be structued as
following::
    
    {
        'status': return value (describe below),
        'data': different by each API (describe in each API's Return type)
    }
    
=== ===============================================
status code
===================================================
200 OK. (success)
404 Not Found. (file/path not exist)
500 Internal Server Error. (should not happen)
=== ===============================================

API Example ::

    >>> import hcc
    >>> open('/tmp/source.c', 'w').write(r'''#include<stdio.h>
    ... int main() {
    ...     printf("hello world\n");
    ... }
    ... ''')
    >>> 
    >>> hcc.fs_upload('dkg', '/tmp/source.c', 'hello.c')
    { 'status': 200, 'data': None }
    >>> 
    >>> hcc.fs_list('dkg')
    { 'status': 200, 'data': [{'name': 'hello.c', 'size': 62}] }
    >>> 
    >>> hcc.mpi_compile('dkg', 'c', 'hello.c', 'hello')
    { 'status': 200, 'data': {'stdout': '', 'stderr': ''} }
    >>> 
    >>> hcc.fs_list('dkg')
    { 'status': 200, 'data': [{'name': 'hello.c', 'size': 61}, {'name': 'hello', 'size': 8466}] }
    >>> 
    >>> hcc.mpi_run('dkg', 'hello', host=3, np=6)
    { 'status': 200, 'data': {'stdout': 'hello world\n', 'stderr': '', 'time': '0:00.00'} }

.. note::
    The path at localhost should be absolutly. Or you will have some problems
    dealing with your working directory.
    
.. note::
    If status != 200, data will contain some debug message if it can. Check
    it for more information and let me know if this is a bug.

"""

from filesystem import fs_list
from filesystem import fs_upload
from filesystem import fs_download
from filesystem import fs_delete
from mpi import mpi_compile
from mpi import mpi_run

__all__ = [
    'fs_list', 'fs_upload', 'fs_download', 'fs_delete',
    'mpi_compile', 'mpi_run',
]

