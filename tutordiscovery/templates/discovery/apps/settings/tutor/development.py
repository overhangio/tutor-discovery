from ..devstack import *

{% include "discovery/apps/settings/partials/common.py" %}

# The following urls should be accessible from the outside by a discovery web user in
# order to use the /login endpoint
SOCIAL_AUTH_EDX_OIDC_PUBLIC_URL_ROOT = "http://localhost:8000/oauth2"
SOCIAL_AUTH_EDX_OIDC_LOGOUT_URL = "http://localhost:8000/logout"
BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL = SOCIAL_AUTH_EDX_OIDC_URL_ROOT
SOCIAL_AUTH_EDX_OIDC_KEY = "{{ DISCOVERY_OAUTH2_KEY_DEV }}"
