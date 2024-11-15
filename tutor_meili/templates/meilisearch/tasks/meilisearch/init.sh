{% if MEILISEARCH_MASTER_KEY %}
# Create the API key using the master key.
# The result is actually deterministic:
# https://www.meilisearch.com/docs/learn/security/master_api_keys#using-the-master-key-to-manage-api-keys
curl -X GET -H 'Authorization: Bearer {{ MEILISEARCH_MASTER_KEY }}' 'http://{{ MEILISEARCH_HOST }}/keys/{{ MEILISEARCH__INTERNAL_API_KEY_UID }}' | grep api_key_not_found && curl \
  -X POST 'http://{{ MEILISEARCH_HOST }}/keys' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer {{ MEILISEARCH_MASTER_KEY }}' \
  --data-binary '{
    "uid": "{{ MEILISEARCH__INTERNAL_API_KEY_UID }}",
    "description": "Open edX key for {{ LMS_HOST }}",
    "actions": ["*"],
    "indexes": ["{{ MEILISEARCH_INDEX_PREFIX }}*"],
    "expiresAt": null
  }' || echo key already exists
{% endif %}
