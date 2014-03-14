
import string
import random
import os
import subprocess
DEVNULL = open(os.devnull, 'w')

def runcmd(cmd, **kwargs):
    """return decoded string.
    ex:
        runcmd('ls -al')
        runcmd('mkdir abc', stderr=subprocess.DEVNULL)
        # default stderr = fd[2]
        
    Throw:
        subprocess.CalledProcessError
    """
    return subprocess.check_output(
        cmd,
        #shell = True,
        env = {'PATH': '/sbin:/bin:/usr/sbin:/usr/bin'},
        **kwargs
    ).decode().strip()


def runcmd_on_host(host, cmd, **kwargs):
    cmd = ['ssh', '-F', '/home/cloud_prj/hcc/ssh_setting/config', host, cmd]
    return runcmd(cmd, stderr=DEVNULL, **kwargs)


def scp_to_server(host, src_path, dst_path, **kwargs):
    real_dst = '%s:%s' % (host, dst_path)
    cmd = ['scp', '-F', '/home/cloud_prj/hcc/ssh_setting/config', src_path, real_dst]
    return runcmd(cmd, **kwargs)


def scp_from_server(host, src_path, dst_path, **kwargs):
    real_src = '%s:%s' % (host, src_path)
    cmd = ['scp', '-F', '/home/cloud_prj/hcc/ssh_setting/config', real_src, dst_path]
    return runcmd(cmd, **kwargs)


def gen_rand_str(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

