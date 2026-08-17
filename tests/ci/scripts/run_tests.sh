#!/bin/bash
set -xo pipefail

MIN_PYTHON="$(python3 tests/ci/scripts/get_min_python_version.py)"
MAX_PYTHON="3.14"

declare -A XDMOD_HOSTS=(
    ["xdmod-main-dev"]="https://xdmod-main-dev"
    ["xdmod-11-0-dev"]="https://xdmod-11-0-dev"
    ["xdmod-11-0"]="https://xdmod-11-0"
)

for py_version in "$MIN_PYTHON" "$MAX_PYTHON"; do

    if command -v pyenv >/dev/null 2>&1; then
        pyenv install -s "$py_version"
        pyenv global "$py_version"
    fi

    python3 -m venv /tmp/venv-$py_version
    source /tmp/venv-$py_version/bin/activate


    python3 -m pip install --upgrade pip setuptools wheel
    python3 -m pip install -e .[report] pytest pytest-cov python-dotenv

    if [ "$py_version" = "$MIN_PYTHON" ] && command -v pyenv >/dev/null 2>&1; then

        min_dependency_versions=$(awk \
            '/install_requires/ {flag=1} flag && !/install_requires/ && NF {print $0} flag && /^\[.*\]$/ {flag=0}' \
            setup.cfg | tr -d '\n' | sed 's/ >= /==/g'
        )
        python3 -m pip install --force-reinstall $min_dependency_versions

    fi

    for xdmod_version in "${!XDMOD_HOSTS[@]}"; do
        host="${XDMOD_HOSTS[$xdmod_version]}"

        timeout 60 bash -c "until curl -k -sf https://$xdmod_version/localhost.crt -o $xdmod_version.crt; do sleep 2; done" \
        || { echo "ERROR: cert never became available for $xdmod_version"; exit 1; }

        rest_token=""
        for attempt in $(seq 1 30); do
            rest_token=$(curl --cacert "$xdmod_version.crt" -sS -X POST -c xdmod.cookie \
                    -d 'username=normaluser&password=normaluser' \
                    "$host/rest/auth/login" | jq -r '.results.token')
            if [ -n "$rest_token" ] && [ "$rest_token" != "null" ]; then
                break
            fi
            echo "waiting for $xdmod_version auth/DB to be ready... (attempt $attempt)"
            sleep 2
        done

        # Error checking for the auth token, if it is empty or null after 30 attempts, exit with an error
        if [ -z "$rest_token" ] || [ "$rest_token" = "null" ]; then
            echo "ERROR: auth never succeeded for $xdmod_version after retries"
            exit 1
        fi

        curl --cacert "$xdmod_version.crt" -sS -X DELETE -b xdmod.cookie "$host/rest/users/current/api/token?token=$rest_token" || true

        api_token=$(curl --cacert "$xdmod_version.crt" -sS -X POST -b xdmod.cookie "$host/rest/users/current/api/token?token=$rest_token" | jq -r '.data.token')

        echo "XDMOD_API_TOKEN=$api_token" > ~/.xdmod-data-token

        REQUESTS_CA_BUNDLE="$xdmod_version.crt" XDMOD_VERSION="$xdmod_version" XDMOD_HOST="$host" \
            python3 -m pytest --cov --cov-branch --cov-append -vvs -o log_cli=true tests/

    done


    deactivate
done
/tmp/venv-$MAX_PYTHON/bin/python3 -m coverage report -m
