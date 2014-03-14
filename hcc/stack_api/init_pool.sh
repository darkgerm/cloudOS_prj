#!/bin/bash
. senv

for i in 0 1 2 3 4 5 6; do
    nova --insecure boot pool$i \
        --image MPI_Ubuntu_with_key \
        --flavor m1.tiny \
        --key-name HHC \
        --nic net-id=291c9510-945e-470d-9d7f-ecaabff8bbfa
done

cat > pool.db <<EOF
0 0 0 0 0 0 0 
EOF

echo 0 > db.lock

chmod 666 pool.db db.lock

