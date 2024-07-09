import hashlib
from urllib.parse import urlencode


def get_gravatar_url(email):
    # Set your variables here
    size = 40

    # Encode the email to lowercase and then to bytes
    email_encoded = email.lower().encode("utf-8")

    # Generate the SHA256 hash of the email
    email_hash = hashlib.sha256(email_encoded).hexdigest()

    # Construct the URL with encoded query parameters
    query_params = urlencode({"s": str(size)})
    gravatar_url = f"https://www.gravatar.com/avatar/{email_hash}?{query_params}"

    return gravatar_url
