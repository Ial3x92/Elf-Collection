# Other Knowledge Sources Archive

**Source identity:** Mixed local archive of external PS4 PKG/PFS references  
**Indexed date:** 2026-05-14  
**Archive date recorded by folder README:** 2026-03-31  
**Artifact folder:** `related-projects/other-knowledge-sources/`

## Executive Summary

This archive is a mixed-source reference set for PS4 package and filesystem reverse engineering. It combines three source families:

- PSDevWiki snapshots for format-oriented reference pages.
- ShadPKG documentation for a modern implementation-focused cryptographic walkthrough.
- A Wololo article that preserves Flatz's fake PKG discussion for historical and exploit-context notes.

The highest-value technical source in the folder is `shadpkg-howworks-raw.md`, which describes the end-to-end PKG and PFS decryption path in implementation terms: PKG header parsing, `entry_keys` and `image_key` handling, RSA-2048 derived keys, AES-128-CBC for metadata blobs, HMAC-SHA256 for PFS keys, AES-128-XTS for PFS sectors, PFSC compressed block handling, and file extraction flow. The strongest format-oriented source is the PSDevWiki PFS page and its local derivative index, which capture block sizing, inode and dirent layout, superroot and `uroot`, and `flat_path_table` behavior.

This folder should be treated as a source archive, not a single coherent upstream project. Traceability matters more than deduplication here. The durable organization therefore keeps primary artifacts, derivative helper files, and provenance metadata separate.

## Scope And Provenance

### Source families

1. **PSDevWiki snapshots**
   - `psdevwiki-pfs.html`
   - `psdevwiki-pkg-files.html`
   - `psdevwiki-pfs-index.md`
   - `psdevwiki-pfs-links.txt`
   - `psdevwiki-pfs-hrefs.txt`

2. **ShadPKG HOWWORKS document**
   - `shadpkg-howworks-raw.md`
   - `shadpkg-howworks-github-blob.html`

3. **Wololo article archive**
   - `wololo-ps4-fpkg-writeup-by-flatz.html`

### Traceability notes

- The folder README records the archive date as 2026-03-31.
- PSDevWiki snapshots preserve permanent revision identifiers through `oldid` links:
  - PFS page: `oldid=296886`
  - PKG files page: `oldid=296676`
- The ShadPKG document declares its own author and date: SeregonWar, 2025-05-23.
- The Wololo HTML embeds `datePublished=2023-10-03` and `dateModified=2023-10-05`.

## Archive Structure

| File or set | What it contributes | Notes |
| --- | --- | --- |
| `psdevwiki-pfs.html` | Full PFS reference snapshot | Best source for page identity, revision traceability, and community-oriented PFS notes |
| `psdevwiki-pfs-index.md` | Compact implementation-focused digest of the PFS page | Useful as a quick PFS format brief |
| `psdevwiki-pfs-links.txt` and `psdevwiki-pfs-hrefs.txt` | Outbound links and href inventory from the same PFS revision | Audit helpers rather than primary technical references |
| `psdevwiki-pkg-files.html` | PKG page snapshot | Useful as a format overview and tool catalog |
| `shadpkg-howworks-raw.md` | Deep PKG/PFS decryption analysis | Best single document here for implementation details |
| `shadpkg-howworks-github-blob.html` | GitHub-rendered copy of the same HOWWORKS document | Redundant in content, useful for preserving rendered page context |
| `wololo-ps4-fpkg-writeup-by-flatz.html` | Historical article snapshot | Contextual source, not the strongest format specification |

## Critical Technical Findings

### 1. The archive separates format structure from cryptographic workflow

The PSDevWiki PFS materials focus on filesystem structure: superblock fields, block-size rules, inode and dirent shape, root discovery, and `flat_path_table`. The ShadPKG HOWWORKS document focuses on how encrypted PKG content is actually decrypted and walked in code-like terms. Together they cover both the data model and the access path.

Evidence:

- `psdevwiki-pfs-index.md` documents block sizes, mode bits, inode fields, dirent layout, superroot and `uroot`, and the hash behavior used by `flat_path_table`.
- `shadpkg-howworks-raw.md` documents the PKG header, entry decryption, `dk3_` derivation, `imgKey`, `ekpfsKey`, `PfsGenCryptoKey`, PFSC parsing, and the extraction process.

### 2. ShadPKG is the strongest implementation-level source in this folder

The HOWWORKS markdown is unusually detailed because it does not stop at naming formats. It explains the sequence of operations, the algorithms involved, and the buffer or offset logic needed to move from PKG container to decrypted file payloads. It includes pseudocode and concrete algorithm choices rather than high-level prose only.

High-value findings from that document include:

- PKG headers are big-endian and expose table offsets, content ID, PFS image offsets, cache sizing, and digests.
- NPDRM-related entries are decrypted through SHA256-derived IV material and AES-128-CBC.
- PFS `dataKey` and `tweakKey` are derived from `ekpfsKey` plus a 16-byte seed using HMAC-SHA256.
- PFS content is decrypted with AES-128-XTS and then may pass through PFSC block decompression.
- PFSC logical blocks use a sector map and optional zlib decompression before logical file data is reconstructed.

### 3. The PSDevWiki PFS page remains the clearest format summary source

The archived PFS page and its local markdown digest identify format properties that are easy to lose when working only from implementation code:

- PFS is described as UFS-like.
- Block size is configurable, constrained to power-of-two values, and varies by use case.
- The superroot contains both the real root (`uroot`) and the `flat_path_table` structure.
- Dirents are 8-byte aligned and encode inode, type, name length, entry size, and null-terminated name.
- The page explicitly ties encrypted PFS to XTS-AES-128 and notes package-image-key context.

### 4. The PKG wiki page is complementary, not sufficient on its own

The PKG files page is useful for orientation and tool discovery, but it is not the deepest source in this archive. It should be used as a broad reference page that points to format topics and tooling, then paired with the ShadPKG and PFS materials for actual implementation work.

### 5. The Wololo article is best treated as historical context

The archived Wololo article preserves a fake PKG writeup attributed to Flatz and is useful for scene context, exploit framing, and FPKG-specific discussion. It is not the primary authority for filesystem layout or decryption flow compared with the ShadPKG document and the PSDevWiki PFS snapshot.

## Duplication And Derivative Relationships

- `shadpkg-howworks-github-blob.html` and `shadpkg-howworks-raw.md` are the same underlying document in two formats.
- `psdevwiki-pfs-index.md`, `psdevwiki-pfs-links.txt`, and `psdevwiki-pfs-hrefs.txt` are local derivatives of `psdevwiki-pfs.html`.
- The archive is intentionally not deduplicated to a single file per source because rendered context, raw content, and derivative indexes each serve different verification needs.

## Constraints And Caveats

- PSDevWiki is reverse-engineering documentation and should be verified against real samples or independent implementations when edge-case compatibility matters.
- The HOWWORKS markdown is a technical analysis document tied to specific source code fragments and current author understanding; it is strong evidence, not a normative specification.
- The Wololo article republishes or contextualizes scene research and should not be treated as the sole basis for low-level format behavior.
- The folder was archived on 2026-03-31, so upstream projects or wiki pages may have changed since capture.

## Practical Reuse Checklist

1. Start with `shadpkg-howworks-raw.md` when the task involves PKG decryption flow, key derivation, PFSC, or extraction order.
2. Start with `psdevwiki-pfs-index.md` and `psdevwiki-pfs.html` when the task involves PFS on-disk structures, header fields, inode or dirent layout, or `flat_path_table` rules.
3. Use `psdevwiki-pkg-files.html` for PKG page orientation and tool cross-references.
4. Use `source-manifest.md` when a source must be refreshed or re-exported.
5. Revalidate any compatibility-affecting claim against the permanent PSDevWiki revision or the ShadPKG raw markdown before depending on it.

## Source Index

### Local artifact folder

- `related-projects/other-knowledge-sources/`

### Local files

- `related-projects/other-knowledge-sources/README.md`
- `related-projects/other-knowledge-sources/source-manifest.md`
- `related-projects/other-knowledge-sources/psdevwiki-pfs.html`
- `related-projects/other-knowledge-sources/psdevwiki-pfs-index.md`
- `related-projects/other-knowledge-sources/psdevwiki-pfs-links.txt`
- `related-projects/other-knowledge-sources/psdevwiki-pfs-hrefs.txt`
- `related-projects/other-knowledge-sources/psdevwiki-pkg-files.html`
- `related-projects/other-knowledge-sources/shadpkg-howworks-raw.md`
- `related-projects/other-knowledge-sources/shadpkg-howworks-github-blob.html`
- `related-projects/other-knowledge-sources/wololo-ps4-fpkg-writeup-by-flatz.html`

### Upstream source list

- [psdevwiki.com/ps4/PFS](https://www.psdevwiki.com/ps4/PFS)
- [psdevwiki.com/ps4/PKG_files](https://www.psdevwiki.com/ps4/PKG_files)
- [github.com/seregonwar/ShadPKG/blob/main/docs/HOWWORKS.md](https://github.com/seregonwar/ShadPKG/blob/main/docs/HOWWORKS.md)
- [raw.githubusercontent.com/seregonwar/ShadPKG/main/docs/HOWWORKS.md](https://raw.githubusercontent.com/seregonwar/ShadPKG/main/docs/HOWWORKS.md)
- [wololo.net/ps4-fpkg-writeup-by-flatz](https://wololo.net/ps4-fpkg-writeup-by-flatz/)
