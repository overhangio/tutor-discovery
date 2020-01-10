from ..production import *

{% include "discovery/apps/settings/partials/common.py" %}

# The following urls should be accessible from the outside by a discovery web user in
# order to use the /login endpoint
SOCIAL_AUTH_EDX_OIDC_PUBLIC_URL_ROOT = "{% if ACTIVATE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}/oauth2"
SOCIAL_AUTH_EDX_OIDC_LOGOUT_URL = "{% if ACTIVATE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}/logout"
BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL = SOCIAL_AUTH_EDX_OIDC_URL_ROOT
SOCIAL_AUTH_EDX_OIDC_KEY = "{{ DISCOVERY_OAUTH2_KEY }}"

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
