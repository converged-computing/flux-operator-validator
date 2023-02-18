#!/bin/bash
# Sanity check a container for the operator

set -eEu -o pipefail

# A pre command script
{% if preCommand %}{{ preCommand }}{% endif %}

container="{{ container }}"
printf "Container: ${container}\n"

# Return code if valid or not
valid=0

# Active user must be root
user=$(whoami)
if [[ "${user}" != "root" ]]; then
    echo "🔴️ Active user must be root, found ${user}"
    valid=1
else
    echo "🟢️ Found active user ${user}"
fi

commands="sudo flux{{ commands }}"

# sudo and flux must be installed
for command in ${commands}; do
    has_command=$(which ${command} || echo not-installed)
    if [[ "${has_command}" == "not-installed" ]]; then
      echo "🔴️ ${command} not found"
      valid=1
    else
      echo "🟢️ ${command} is installed"
    fi
done

# Return code will fail or succeed
exit ${valid}