#!/bin/bash
set -exo pipefail

loaded_image="$(docker load -i "$XDMOD_VERSION.tar" | sed 's/Loaded image: //')"
docker run -dt --name "$XDMOD_VERSION" -p 8080:443 "$loaded_image"

# generate cert and copy it out
docker exec "$XDMOD_VERSION" bash -c "openssl genrsa -rand /proc/cpuinfo:/proc/filesystems:/proc/interrupts:/proc/ioports:/proc/uptime 2048 > /etc/pki/tls/private/localhost.key"
docker cp tests/ci/scripts/openssl.cnf "$XDMOD_VERSION":/root/openssl.cnf
docker exec "$XDMOD_VERSION" bash -c "openssl req -new -key /etc/pki/tls/private/localhost.key -x509 -sha256 -days 365 -set_serial $RANDOM -out /etc/pki/tls/certs/localhost.crt -config /root/openssl.cnf"
docker exec "$XDMOD_VERSION" bash -c '/root/bin/services restart'
docker cp "$XDMOD_VERSION":/etc/pki/tls/certs/localhost.crt .

# select Python version for this cell (both cells)
pyenv install -s "$PYTHON_VERSION"
pyenv global "$PYTHON_VERSION"

# the min cell needs the system CA bundle for pip to reach pypi
if [ "$PYTHON_VERSION" = "3.8" ]; then
    export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
fi

python3 -m pip install --upgrade pip
python3 -m pip install -e .[report]
python3 -m pip install --upgrade python-dotenv pytest pytest-cov

# force-install the oldest supported dependency versions (min cell only)
if [ "$PYTHON_VERSION" = "3.8" ]; then
    min_dependency_versions=$(awk \
        '/install_requires/ {flag=1} flag && !/install_requires/ && NF {print $0} flag && /^\[.*\]$/ {flag=0}' \
        setup.cfg | tr -d '\n' | sed 's/ >= /==/g'
    )
    python3 -m pip install --force-reinstall $min_dependency_versions
fi

# fetch API token
rest_token=$(curl --cacert "localhost.crt" -sS -X POST -c xdmod.cookie -d 'username=normaluser&password=normaluser' https://localhost:8080/rest/auth/login | jq -r '.results.token')
api_token=$(curl --cacert "localhost.crt" -sS -X POST -b xdmod.cookie "https://localhost:8080/rest/users/current/api/token?token=$rest_token" | jq -r '.data.token')

# write the token where the tests read it
echo "XDMOD_API_TOKEN=$api_token" > ~/.xdmod-data-token

# trust the cert for requests
cat "localhost.crt" >> "$(python3 -c 'import certifi; print(certifi.where())')"

REQUESTS_CA_BUNDLE=localhost.crt XDMOD_HOST="https://localhost:8080" python3 -m pytest --cov --cov-branch -vvs -o log_cli=true tests/

mv .coverage ".coverage.${PYTHON_VERSION}.${XDMOD_VERSION}"