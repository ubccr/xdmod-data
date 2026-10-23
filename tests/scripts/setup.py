# Install xdmod-data in editable mode and get API tokens for each of the XDMoD
# containers.

import get_config
from pathlib import Path
import warnings
import requests
from requests.exceptions import RequestException
from urllib3.exceptions import InsecureRequestWarning
import tenacity

scratch_dir = Path(__file__).resolve().parent.parent / "scratch"
scratch_dir.mkdir(exist_ok=True)


# Define a function for trying to get the self-signed certificate file from the
# XDMoD web server every second for up to one minute (this is so the web server
# has time to start up before making requests to it).
@tenacity.retry(
    retry=tenacity.retry_if_exception_type(RequestException),
    stop=tenacity.stop_after_attempt(120),
    wait=tenacity.wait_fixed(1),
    reraise=True,
)
def get_certificate_file(container_name):
    filename = f"{scratch_dir}/{container_name}.crt"
    print(f"Saving certificate file from {container_name} to {filename}", flush=True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", InsecureRequestWarning)
        response = requests.get(f"https://{container_name}/localhost.crt", verify=False)
    response.raise_for_status()
    with open(filename, "wb") as cert_file:
        cert_file.write(response.content)
    return filename


for image in get_config.get_xdmod_images():
    container_name = get_config.get_container_name(image, default=image)

    # Open a requests session.
    session = requests.Session()

    # Get the certificate file from the XDMoD container.
    session.verify = get_certificate_file(container_name)

    # Get an auth token.
    print(f"Getting auth token from {container_name}", flush=True)
    response = session.post(
        f"https://{container_name}/rest/auth/login",
        data={"username": "normaluser", "password": "normaluser"},
    )
    response.raise_for_status()
    auth_token = response.json()["results"]["token"]

    # Delete any API token that already exists.
    print(f"Deleting API token on {container_name}", flush=True)
    response = session.delete(
        f"https://{container_name}/rest/users/current/api/token?token={auth_token}"
    )
    if response.status_code not in [200, 404]:
        response.raise_for_status()

    # Create an API token.
    print(f"Creating API token on {container_name}", flush=True)
    response = session.post(
        f"https://{container_name}/rest/users/current/api/token?token={auth_token}"
    )
    response.raise_for_status()

    # Save the API token to a file.
    token_filename = f"{scratch_dir}/{container_name}.token"
    print(f"Saving API token to {token_filename}", flush=True)
    with open(token_filename, "w") as token_file:
        token_file.write(f"XDMOD_API_TOKEN={response.json()['data']['token']}")
