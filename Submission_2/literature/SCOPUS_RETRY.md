# Scopus verification retry

A fresh retry tested eight endpoints: Scopus Sources, Elsevier's Scopus content page, the Elsevier abstract API for DORY, SCImago, ACM IMWUT, IEEE Xplore's DORY record, the KIT TinyHAR institutional record, and Crossref's DORY metadata.

All eight failed at the HTTPS proxy tunnel with `403 Forbidden`, before their content could be inspected. The exact URLs and responses are in `scopus_retry_log.json`.

The environment configuration confirms restricted internet access with only GitHub/package-manager presets and no custom research domains. A configuration draft adding the eight checked hostnames was successfully saved, preserving existing presets. **That save has not applied or published the network change.**

## Required next step

Review and save the network changes in Environment settings, then publish the environment. After the changed network policy is active, retry the source and individual-paper checks. Further login or institutional access could still be needed after connectivity is restored; no missing credential is assumed from this proxy error.

The draft adds only:

- `www.scopus.com`
- `www.elsevier.com`
- `api.elsevier.com`
- `www.scimagojr.com`
- `dl.acm.org`
- `ieeexplore.ieee.org`
- `publikationen.bibliothek.kit.edu`
- `api.crossref.org`

## Evidence status

Zero papers are newly verified as Scopus-indexed. The report's existing qualification remains accurate. The block is an access limitation, not evidence that any listed paper is absent from Scopus. A source's title-level coverage and an individual paper's indexed record must remain distinct.

## Retry after user enabled full access

A fresh six-endpoint retry and a separate three-endpoint escalated execution retry were performed after the user reported enabling full access. Command execution was permitted, but all nine HTTPS requests still failed with proxy CONNECT 403 errors. A separate curl check reported `server: envoy` and `CONNECT tunnel failed, response 403`, locating the failure at the environment proxy before Scopus content could be read.

The saved configuration draft now contains the eight research domains. This describes the editable draft, not proof that the running instance has received the policy. Runtime application/publication status could not be established from the available tools. No duplicate draft update or additional credential request was made.

See `full_access_retry_log.json` and `escalated_access_retry_log.json`. No paper indexing status changed.
