# LibOrbisPkg Wiki — Tooling and PKG Crypto Notes

- Canonical source: https://github.com/maxton/LibOrbisPkg.wiki.git
- Canonical wiki home: https://github.com/maxton/LibOrbisPkg/wiki
- Local artifact folder: [related-projects/liborbispkg-wiki](liborbispkg-wiki)
- Indexed on: 2026-05-14
- Source type: wiki/docs snapshot

## Executive Summary

The LibOrbisPkg wiki is a compact documentation layer for the broader LibOrbisPkg ecosystem. Its strongest technical value is not API detail but the project-level split between the reusable library and the two end-user tools, plus a concise PKG cryptography note that explains how fake PKG decryption revolves around passcode-derived keys, RSA-wrapped key material, and the `IMAGE_KEY` and `ENTRY_KEYS` records. For operational use, the wiki gives the clearest user-facing instructions for building a PKG with PkgEditor, while the PkgTool page itself is currently too sparse to stand alone.

## Table of Contents

1. Scope and Identity
2. Wiki Structure and Signal Level
3. Project Surface Area
4. PKG Cryptography Findings
5. PkgEditor Workflow Notes
6. Constraints and Unknowns
7. Practical Reuse Checklist
8. Source Index

## Scope and Identity

This reference covers the GitHub wiki pages for LibOrbisPkg, not the implementation repository itself. The wiki is documentation-oriented and small enough to treat page-by-page.

Primary local pages:

- [related-projects/liborbispkg-wiki/Home.md](liborbispkg-wiki/Home.md)
- [related-projects/liborbispkg-wiki/Library.md](liborbispkg-wiki/Library.md)
- [related-projects/liborbispkg-wiki/PKG-Information.md](liborbispkg-wiki/PKG-Information.md)
- [related-projects/liborbispkg-wiki/PkgEditor.md](liborbispkg-wiki/PkgEditor.md)
- [related-projects/liborbispkg-wiki/PkgTool.md](liborbispkg-wiki/PkgTool.md)

## Wiki Structure and Signal Level

| Page | Primary value | Depth |
| --- | --- | --- |
| [Home.md](liborbispkg-wiki/Home.md) | Top-level map of library vs tools | Light |
| [Library.md](liborbispkg-wiki/Library.md) | Namespace inventory for the reusable library | Light |
| [PKG-Information.md](liborbispkg-wiki/PKG-Information.md) | Highest-value technical material: key derivation, PFS keys, RSA-wrapped records | High |
| [PkgEditor.md](liborbispkg-wiki/PkgEditor.md) | User workflow for GP4, PKG, and SFO creation/editing | Medium |
| [PkgTool.md](liborbispkg-wiki/PkgTool.md) | Confirms a CLI exists, but gives no usable detail beyond that | Very low |

Operationally, this wiki is best treated as a companion reference:

- Start with [PKG-Information.md](liborbispkg-wiki/PKG-Information.md) for cryptographic concepts and fake-PKG-specific handling.
- Use [PkgEditor.md](liborbispkg-wiki/PkgEditor.md) for build-time requirements and GUI workflow assumptions.
- Use [Library.md](liborbispkg-wiki/Library.md) only as a namespace map, not as a stable API contract.

## Project Surface Area

The wiki home page describes LibOrbisPkg as a C# library plus tools for creating, manipulating, and inspecting PS4 PKG files. It explicitly splits the project into three user-facing surfaces:

1. The reusable library.
2. PkgEditor, the GUI tool.
3. PkgTool, the command-line tool.

Source: [related-projects/liborbispkg-wiki/Home.md](liborbispkg-wiki/Home.md)

The library page enumerates the namespaces that define the intended format coverage:

| Namespace | Documented responsibility |
| --- | --- |
| `LibOrbisPkg.GP4` | GP4 project handling |
| `LibOrbisPkg.PKG` | PKG file handling |
| `LibOrbisPkg.PFS` | PFS image handling |
| `LibOrbisPkg.PlayGo` | PlayGo `chunk.dat` and manifest handling |
| `LibOrbisPkg.Rif` | `license.dat` and `license.info` handling |
| `LibOrbisPkg.SFO` | SFO file handling |
| `LibOrbisPkg.Util` | Crypto, keys, file I/O helpers, and related utilities |

Source: [related-projects/liborbispkg-wiki/Library.md](liborbispkg-wiki/Library.md)

One explicit caveat matters for any downstream reuse: the wiki states that the API is not yet stable and is “kind of clunky.” That makes the page useful for capability discovery, but weak as a compatibility guarantee.

## PKG Cryptography Findings

The technically important page is [related-projects/liborbispkg-wiki/PKG-Information.md](liborbispkg-wiki/PKG-Information.md). Its claims are documentation-level rather than code-level, but they capture the key mental model the project authors used.

### Derived keys

The page states that PKG contents use keys derived from a developer-specified passcode plus the content ID. These are labeled `dk0` through `dk6`, produced by hashing the content ID, passcode, and an integer index with SHA-256.

Documented uses:

- `dk1` is the EKPFS value and is used to derive PFS encryption and signing keys.
- `dk2` generates the AES IV/key for encrypting `license.info` in the PKG entry filesystem.
- `dk3` generates the AES IV/key for encrypting `IMAGE_KEY`, `license.dat`, and the PKG header signature.
- The page explicitly says the uses of the other derived keys are not known.

Source: [related-projects/liborbispkg-wiki/PKG-Information.md](liborbispkg-wiki/PKG-Information.md)

### PFS key generation

The wiki describes PFS key generation as HMAC-SHA256 over a PFS key seed plus an index, keyed by `dk1` / EKPFS:

- Index `1` generates the XTS tweak and data keys.
- Index `2` generates the HMAC-SHA256 signing key.

This is the clearest direct statement in the wiki about how PKG-level secrets are converted into PFS-level keys.

Source: [related-projects/liborbispkg-wiki/PKG-Information.md](liborbispkg-wiki/PKG-Information.md)

### ENTRY_KEYS and IMAGE_KEY roles

The wiki distinguishes two important records:

1. `ENTRY_KEYS`
2. `IMAGE_KEY`

For `ENTRY_KEYS`, the page says six derived keys are RSA-encrypted and stored there, with their digests, while the passcode is stored in place of `dk0` and also gets its own RSA key slot. The page further notes that only public moduli are known for most of these RSA keys, except RSA key 3 where both public and private keys are known.

For `IMAGE_KEY`, the page says EKPFS (`dk1`) is RSA-encrypted with the “mount-image” public key and stored in `IMAGE_KEY`, and then that entry itself is encrypted with `dk3`.

Source: [related-projects/liborbispkg-wiki/PKG-Information.md](liborbispkg-wiki/PKG-Information.md)

### Fake PKG decryption conditions

The page provides a practical decryption summary for the PFS image inside a PKG. It states that decrypting the PFS of a PKG requires any one of the following:

1. RSA key 0.
2. RSA key 1.
3. The mount-image RSA key.
4. The passcode.
5. The EKPFS.
6. The XTS data and tweak keys.

It also claims that items 1 through 3 would be sufficient to decrypt any PKG, while items 4 through 6 would only decrypt a specific PKG. For fake PKGs, the wiki says the mount-image key is replaced with a generated fake-PKG key, which is why PkgEditor and PkgTool can decrypt fake PKGs without needing the original passcode or license.

Source: [related-projects/liborbispkg-wiki/PKG-Information.md](liborbispkg-wiki/PKG-Information.md)

### Authentication note

The page ends by stating that PKG authentication uses SHA-256, HMAC-SHA256, and RSA to detect tampering. The local snapshot does not expand that section further, so this should be treated as a high-level claim only.

Source: [related-projects/liborbispkg-wiki/PKG-Information.md](liborbispkg-wiki/PKG-Information.md)

## PkgEditor Workflow Notes

The wiki's strongest operational guidance is on [related-projects/liborbispkg-wiki/PkgEditor.md](liborbispkg-wiki/PkgEditor.md), which outlines the intended GUI workflow for GP4-driven package creation and SFO editing.

### Build-time requirements documented by the wiki

- PKG contents and layout are defined by GP4 project files.
- A content ID is required, must be exactly 36 characters, and must match the pattern `XXXXXX-YYYY00000_00-ZZZZZZZZZZZZZZZZ`.
- A passcode is required, though the page says that for fake PKGs it does not prevent file access.
- DLC packages require an entitlement key, with an all-zero default.
- Every PKG needs a `param.sfo` under `Image0/sce_sys`.

Source: [related-projects/liborbispkg-wiki/PkgEditor.md](liborbispkg-wiki/PkgEditor.md)

### Editing/build workflow described by the wiki

The page documents these steps and assumptions:

1. Create or open a GP4 project.
2. Add folders/files through the right-side file view.
3. Create or open an SFO file and place it under `Image0/sce_sys`.
4. Optionally set volume timestamp and creation date behavior.
5. Use `Build PKG` to emit the package.

It also notes two additional user-facing behaviors:

- `Build PFS` exists but is described as mainly for debugging.
- Opening an existing PKG allows browsing entries, opening `PARAM_SFO`, and extracting files from the Files tab.

Source: [related-projects/liborbispkg-wiki/PkgEditor.md](liborbispkg-wiki/PkgEditor.md)

## Constraints and Unknowns

The wiki has real value, but its limits are clear:

1. The library page does not document concrete class APIs or stable signatures.
2. The cryptography page gives design notes but not field layouts or implementation references.
3. The PkgTool page is only a placeholder sentence, so it is not sufficient for CLI behavior or argument documentation.
4. The PKG authentication section is incomplete in the snapshot and should not be over-interpreted.
5. Several key-usage claims are explicitly marked unknown by the wiki itself.

## Practical Reuse Checklist

Use this wiki effectively by treating it as a fast orientation layer:

1. Read [Home.md](liborbispkg-wiki/Home.md) to understand the library/tool split.
2. Read [Library.md](liborbispkg-wiki/Library.md) to map namespaces to file-format responsibilities.
3. Read [PKG-Information.md](liborbispkg-wiki/PKG-Information.md) for the key-derivation and fake-PKG decryption model.
4. Read [PkgEditor.md](liborbispkg-wiki/PkgEditor.md) for GP4, content ID, `param.sfo`, and GUI build assumptions.
5. Do not rely on [PkgTool.md](liborbispkg-wiki/PkgTool.md) for CLI details; inspect the implementation repository when you need exact command behavior.

## Source Index

### Local snapshot

- [related-projects/liborbispkg-wiki/manifest.md](liborbispkg-wiki/manifest.md)
- [related-projects/liborbispkg-wiki/Home.md](liborbispkg-wiki/Home.md)
- [related-projects/liborbispkg-wiki/Library.md](liborbispkg-wiki/Library.md)
- [related-projects/liborbispkg-wiki/PKG-Information.md](liborbispkg-wiki/PKG-Information.md)
- [related-projects/liborbispkg-wiki/PkgEditor.md](liborbispkg-wiki/PkgEditor.md)
- [related-projects/liborbispkg-wiki/PkgTool.md](liborbispkg-wiki/PkgTool.md)

### Upstream wiki pages

- https://github.com/maxton/LibOrbisPkg/wiki
- https://github.com/maxton/LibOrbisPkg/wiki/Library
- https://github.com/maxton/LibOrbisPkg/wiki/PKG-Information
- https://github.com/maxton/LibOrbisPkg/wiki/PkgEditor
- https://github.com/maxton/LibOrbisPkg/wiki/PkgTool
