
from __future__ import unicode_literals
from subprocess import CalledProcessError

import utils
import stack_api


def fs_list(username):
    """
    List files in filesystem.
    
    :param username: Name of the user.
    :rtype: list of ``{'name': name, 'size': size in Bytes}``
    """
    ret = {'status': 100, 'data': []}
    
    nova = stack_api.get_nova('dkg')
    server = stack_api.get_server_by_name(nova, username)
    host = server.addresses['CloudOS_2013'][0]['addr']
    
    # $5 field is size, $9 field is name.
    try:
        flist = utils.runcmd_on_host(host, "ls -l | awk 'NR>1{print $5, $9}'")
    except CalledProcessError:
        ret['status'] = 500
        return ret
    
    for file in flist.split('\n'):
        args = file.split(' ')
        if len(args) < 2: continue
        ret['data'].append({
            'name': args[1],
            'size': args[0],
        })
    
    ret['status'] = 200
    return ret


def fs_upload(username, src_path, dst_path):
    """
    Upload file to server.
    
    :param username: Name of the user.
    :param src_path: Path to the file at localhost.
    :param dst_path: Path to the file at the server.
    :rtype: None
    """
    ret = {'status': 100, 'data': None}
    
    nova = stack_api.get_nova('dkg')
    server = stack_api.get_server_by_name(nova, username)
    host = server.addresses['CloudOS_2013'][0]['addr']
    
    try:
        msg = utils.scp_to_server(host, src_path, dst_path)
    except CalledProcessError:
        ret['status'] = 500
        ret['data'] = 'scp to server error.'
        return ret
    
    ret['status'] = 200
    return ret


def fs_download(username, src_path, dst_path):
    """
    Download file from server.
    
    :param username: Name of the user.
    :param src_path: Path to the file at the server.
    :param dst_path: Path to the file at localhost.
    :rtype: None
    """
    ret = {'status': 100, 'data': None}
    
    nova = stack_api.get_nova('dkg')
    server = stack_api.get_server_by_name(nova, username)
    host = server.addresses['CloudOS_2013'][0]['addr']
    
    try:
        msg = utils.scp_from_server(host, src_path, dst_path)
    except CalledProcessError:
        ret['status'] = 500
        ret['data'] = 'scp to server error.'
        return ret
    
    ret['status'] = 200
    return ret


def fs_delete(username, path):
    """
    Delete file from server. It will still return 200 OK if file not exists.
    
    :param username: Name of the user.
    :param path: Path to the file at the server.
    :rtype: None
    """
    ret = {'status': 100, 'data': None}
    
    nova = stack_api.get_nova('dkg')
    server = stack_api.get_server_by_name(nova, username)
    host = server.addresses['CloudOS_2013'][0]['addr']
    
    try:
        msg = utils.runcmd_on_host(host, 'rm -f ' + path)
    except CalledProcessError:
        ret['status'] = 500
        ret['data'] = 'runcmd on host error.'
        return ret
    
    ret['status'] = 200
    return ret

