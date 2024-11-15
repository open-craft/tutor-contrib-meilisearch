Meilisearch for Open edX (Tutor Plugin)
=======================================

This is a plugin for `Tutor <https://docs.tutor.edly.io>`_ 18 (Open edX "Redwood" release) that provides Meilisearch to the platform, so it can be used as a search engine to power content search.

⭐️ This plugin isn't needed with Tutor 19+ (Open edX Sumac+), as `Meilisearch functionality is now built in <https://github.com/overhangio/tutor/pull/1141>`_. ⭐️ 

Installation
------------

Currently, you need to clone this repo from GitHub then install it into your tutor virtual environment with::

    pip install -e ./tutor-contrib-meilisearch

Then, to enable this plugin, run::

    tutor plugins enable meilisearch

If you have an already running platform, initialize this plugin with a command like the following::

    tutor [local|dev|k8s] do init --limit=meilisearch

Or use ``tutor [local|dev|k8s] launch -I`` to re-launch the platform (takes much longer).

Configuration
-------------

- ``MEILISEARCH_INDEX_PREFIX`` (default: ``"tutor_"``)
- ``MEILISEARCH_PUBLIC_HOST`` (default: ``"meilisearch.{{ LMS_HOST }}"``)
- ``MEILISEARCH_DOCKER_IMAGE`` (default: ``"docker.io/getmeili/meilisearch:v1.8``)
- ``MEILISEARCH_MASTER_KEY`` The master key. Only required to generate the API key (default: auto-generated).
- ``MEILISEARCH_API_KEY`` The API key (or tenant key) to use for this Open edX instance (default: auto-generated using the master key).

These values can be modified with ``tutor config save --set PARAM_NAME=VALUE`` commands.

Upgrading
---------
If you upgrade this plugin or change the ``MEILISEARCH_DOCKER_IMAGE`` setting, you may get a new version of Meilisearch.
In that case, the ``meilisearch`` Docker service will fail to start because the index format is from an older version.
For large instances, you can follow the `Meilisearch update procedure <https://www.meilisearch.com/docs/learn/update_and_migration/updating#updating-a-self-hosted-meilisearch-instance>`_
(basically, dump the index contents to a file, upgrade it, then restore from the data dump file). For development and
smaller installations, the easier way is to follow this procedure::

    tutor [local|dev] stop meilisearch
    cd "$(tutor config printroot)/data/meilisearch"
    mv data.ms "data.ms.$(date +%Y-%m-%d)"
    tutor config save
    tutor [local|dev] start -d meilisearch
    tutor [local|dev] do init --limit=meilisearch

TODO
----

Currently, this plugin always deploys a new instance of Meilisearch. It should be modified to support using an existing external instance if desired.

DNS records
-----------

For production use, it is assumed that the ``MEILISEARCH_PUBLIC_HOST`` DNS record points to your server.

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

This work is licensed under the terms of the `GNU Affero General Public License (AGPL) <https://github.com/open-craft/tutor-contrib-meilisearch/blob/master/LICENSE.txt>`_.
