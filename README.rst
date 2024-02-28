Meilisearch for Open edX (Tutor Plugin)
=======================================

This is a plugin for `Tutor <https://docs.tutor.edly.io>`_ that provides Meilisearch to the platform, so it can be used as a search engine to power content search.

Installation
------------

Currently, you need to clone this repo from GitHub then install it into your tutor virtual environment with::

    pip install -e ./tutor-meilisearch

Then, to enable this plugin, run::

    tutor plugins enable meilisearch

If you have an already running platform, initialize this plugin with a command like the following::

    tutor [local|dev|k8s] do init --limit=meilisearch

Or use ``tutor [local|dev|k8s] launch -I`` to re-launch the platform (takes much longer).

Configuration
-------------

- ``MEILISEARCH_INDEX_PREFIX`` (default: ``"tutor_"``)
- ``MEILISEARCH_PUBLIC_HOST`` (default: ``"meilisearch.{{ LMS_HOST }}"``)
- ``MEILISEARCH_DOCKER_IMAGE`` (default: ``"docker.io/getmeili/meilisearch:v1.6``)
- ``MEILISEARCH_MASTER_KEY`` The master key. Only required to generate the API key (default: auto-generated).
- ``MEILISEARCH_API_KEY`` The API key (or tenant key) to use for this Open edX instance (default: auto-generated using the master key).

These values can be modified with ``tutor config save --set PARAM_NAME=VALUE`` commands.

TODO
----

Currently, this plugin always deploys a new instance of Meilisearch. It should be modified to support using an existing external instance if desired.

DNS records
-----------

For production use, it is assumed that the ``MEILISEARCH_PUBLIC_HOST`` DNS record points to your server. We don't yet know whether it will be required to make this endpoint public or not (does the LMS/CMS proxy all calls to Meilisearch or do browsers make calls directly?).

In development mode, Meilisearch is available at http://meilisearch.local.edly.io:7700.

Web UI
------

The Meilisearch web UI can be accessed at http(s)://<MEILISEARCH_PUBLIC_HOST>. For development, this is usually http://meilisearch.local.edly.io:7700/

An API key for accessing the UI can be obtained with::

  tutor config printvalue MEILISEARCH_API_KEY

Troubleshooting
---------------

TBD

License
-------

This work is licensed under the terms of the `GNU Affero General Public License (AGPL) <https://github.com/open-craft/tutor-meilisearch/blob/master/LICENSE.txt>`_.
