#!/bin/bash

set -e

# $1: FILE
# $2: PARAMETER
# $3: USERNAME
# $4: PASSWORD
# $5: GROUP

newgrp $5 << EOF
       htpasswd -$2 $1 $3 $4
EOF
