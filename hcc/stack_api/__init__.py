# -*- coding: UTF-8 -*-
import os
import time
import traceback
from datetime import datetime

import novaclient.v1_1.client as nvclient
import novaclient.exceptions

from credentials import get_nova_creds

POOLDB = '/home/cloud_prj/hcc/stack_api/pool.db'
DBLOCK = '/home/cloud_prj/hcc/stack_api/db.lock'

def get_nova(who):
    creds = get_nova_creds(who)
    nova = nvclient.Client(insecure=True, **creds)
    return nova


def get_server_by_name(nova, name):
    """If name not found, create a new one."""
    try:
        server = nova.servers.find(name=name)
        
    except novaclient.exceptions.NotFound:
        server = nova.servers.create(
            name = name,
            image = nova.images.find(name='MPI_Ubuntu_with_key'),
            flavor = nova.flavors.find(name='m1.tiny'),
            key_name = 'HHC',
            nics = [{'net-id': '291c9510-945e-470d-9d7f-ecaabff8bbfa'}],  # CloudOS_2013
        )

        # wait for server ready
        while server.status == 'BUILD':
            server = nova.servers.get(server.id)
            time.sleep(1)

    return server


def get_pool(nova):
    while int(open(DBLOCK).read()) == 1:
        print 'db locked. sleep 1 sec.'
        time.sleep(1)
    open(DBLOCK, 'w').write('1')
    
    pool = []
    
    status = map(int, open(POOLDB).read().strip().split(' '))
    for i,st in enumerate(status):
        pool.append({
            'server': nova.servers.find(name='pool%d' % (i,)),
            'status': st,
        })
        
    return pool


def write_pool_status(pool_info):
    status = [pool['status'] for pool in pool_info]
    open(POOLDB, 'w').write(' '.join(map(str, status)))
    open(DBLOCK, 'w').write('0')

