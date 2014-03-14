#!/bin/bash
while [ 1 ]; do
    pool=`cat pool.db`
    size=`echo $pool | awk 'NR==1{print NF}'`
    
    if [ "$size" -ne 7 ]; then
        
        # delete the last server
        id=$(($size-1))
        
        # before delete, lock the db.lock
        while [ "`cat db.lock`" -eq 1 ]; do sleep 1; done
        echo 1 > db.lock
        
        . senv
        echo nova --insecure delete pool$id
        
        echo 0 > db.lock
    fi
    
    echo $pool
    
    sleep 1
done

