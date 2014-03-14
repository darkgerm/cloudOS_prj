
from __future__ import unicode_literals
from subprocess import CalledProcessError

import utils
import stack_api


def mpi_compile(username, type, src_path, exe_path='a.out'):
    """
    Compile the source code. The source will be compiled by
    ``mpicc -Wall -Wextra -O3 $src_path -o $exe_path -lm``
    (if type is 'cpp', use mpic++ instead)
    
    :param username: Name of the user.
    :param type: Source type (``c`` or ``cpp``).
    :param src_path: Source path.
    :param exe_path: Outfile path. (default: ``a.out``).
    :rtype: ``{'stdout': string of stdout, 'stderr': string of stderr}``
    """
    ret = {'status': 100, 'data': {}}
    
    nova = stack_api.get_nova('dkg')
    server = stack_api.get_server_by_name(nova, username)
    host = server.addresses['CloudOS_2013'][0]['addr']
    
    # compile
    cmd = (
        '{cc} -Wall -Wextra -O3 {src_path} -o {exe_path} -lm'
        ' > /tmp/stdout 2> /tmp/stderr'
    ).format(
        cc = 'mpic++' if type == 'cpp' else 'mpicc',
        src_path = src_path,
        exe_path = exe_path,
    )
    
    try:
        msg = utils.runcmd_on_host(host, cmd)
    except CalledProcessError:
        #ret['status'] = 500
        #ret['data'] = 'runcmd on host error.' + cmd
        #return ret
        pass  #we assume the cmd is always right, or we can't get compile error.
    
    # get result
    stdout = '/tmp/stdout-' + utils.gen_rand_str(6)
    stderr = '/tmp/stdout-' + utils.gen_rand_str(6)
    try:
        msg = utils.scp_from_server(host, '/tmp/stdout', stdout)
        msg = utils.scp_from_server(host, '/tmp/stderr', stderr)
    except CalledProcessError:
        ret['status'] = 500
        ret['data'] = msg
        return ret
    
    # prepare for return
    ret['data']['stdout'] = open(stdout).read()
    ret['data']['stderr'] = open(stderr).read()
    utils.runcmd(['rm', '-f', stdout, stderr])
    
    ret['status'] = 200
    return ret


def mpi_run(username, exe_path, host_num, np, args=''):
    """
    Execute the binary code. The code will be executed by
    ``mpiexec -hostfile $host_you_selected -n $np $exe_path $args``
    
    :param username: Name of the user.
    :param exe_path: Executable file path.
    :param host_num: (int) Number of host that want to use.
    :param np: (int) Number of process that want ot use. (mpiexec -n <np>)
    :param args: (string) Argument for execution.
    :rtype: ``{'stdout': string of stdout, 'stderr': string of stderr, 'time': 'mm:ss.xx'}``
    
    .. note:: ``args`` is not check if it can inject command. Need to fix
        in the future :(
    """
    ret = {'status': 100, 'data': {}}
    
    nova = stack_api.get_nova('dkg')
    server = stack_api.get_server_by_name(nova, username)
    host = server.addresses['CloudOS_2013'][0]['addr']
    localhost = server
    
    
    # alloc servers from pool
    servers = []
    pool_info = stack_api.get_pool(nova)
    ptr = 0
    while len(servers) < host_num - 1:      # 'localhost' is counted in.
        
        if ptr >= len(pool_info):       # run out of pool, open a new one
            new_pool_name = 'pool%d' % (ptr, )
            
            # user get_server_by_name to create a new pool
            server = stack_api.get_server_by_name(nova, new_pool_name)
            pool_info.append({
                'server': server,
                'status': 0
            })
            
        # pool_info[ptr] must be available
        
        if pool_info[ptr]['status'] == 0:
            servers.append(pool_info[ptr]['server'])
            pool_info[ptr]['status'] = 1                # lock, in use
            
        ptr += 1
    
    stack_api.write_pool_status(pool_info)
    
    
    # generate /tmp/hosts file
    hosts_file = '/tmp/hosts-' + utils.gen_rand_str(6)
    f = open(hosts_file, 'w')
    f.write(localhost.addresses['CloudOS_2013'][0]['addr'] + '\n')
    for server in servers:
        f.write(server.addresses['CloudOS_2013'][0]['addr'] + '\n')
    f.close()
    
    
    # copy hosts file to server
    try:
        msg = utils.scp_to_server(host, hosts_file, '/tmp/hosts')
    except CalledProcessError:
        ret['status'] = 500
        ret['data'] = 'scp hosts to server error.'
        return ret
    
    
    # prepare executable for servers
    exe_file = '/tmp/exe-' + utils.gen_rand_str(6)
    try:
        msg = utils.scp_from_server(host, exe_path, exe_file)
    except CalledProcessError:
        ret['status'] = 500
        ret['data'] = 'scp exe from server error.'
        return ret
    
    for server in servers:
        serverip = server.addresses['CloudOS_2013'][0]['addr']
        done = False
        while not done:
            try:
                msg = utils.scp_to_server(serverip, exe_file, exe_path)
                done = True
            except CalledProcessError:
                # it must be success = =
                continue
                #ret['status'] = 500
                #ret['data'] = 'scp exe from server error.'
                #return ret
    
    
    # execute
    cmd = (
        'mpiexec -hostfile /tmp/hosts -n {np} ./{exe_path} {args}'
        ' > /tmp/stdout 2> /tmp/stderr'
    ).format(
        np = np,
        exe_path = exe_path,
        args = args,
    )
    
    try:
        msg = utils.runcmd_on_host(host, cmd)
    except CalledProcessError:
        #ret['status'] = 500
        #ret['data'] = 'runcmd on host error.' + cmd
        #return ret
        pass  #we assume the cmd is always right, or we can't get compile error.
    
    
    # unlock servers
    pool_info = stack_api.get_pool(nova)
    for server in servers:
        pool_num = int(server.name[4:])     # 'pool5'
        pool_info[pool_num]['status'] = 0
    
    stack_api.write_pool_status(pool_info)
    
    
    # get result
    stdout_file = '/tmp/stdout-' + utils.gen_rand_str(6)
    stderr_file = '/tmp/stdout-' + utils.gen_rand_str(6)
    time_file = '/tmp/time-' + utils.gen_rand_str(6)
    try:
        msg = utils.scp_from_server(host, '/tmp/stdout', stdout_file)
        msg = utils.scp_from_server(host, '/tmp/stderr', stderr_file)
        #msg = utils.scp_from_server(host, '/tmp/time', time_file)
    except CalledProcessError:
        ret['status'] = 500
        ret['data'] = msg
        return ret
    
    
    # prepare for return
    ret['data']['stdout'] = open(stdout_file).read()
    ret['data']['stderr'] = open(stderr_file).read()
    ret['data']['time'] = 'no use now'
    utils.runcmd(['rm', '-f', hosts_file, stdout_file, stderr_file, time_file])
    
    ret['status'] = 200
    return ret

