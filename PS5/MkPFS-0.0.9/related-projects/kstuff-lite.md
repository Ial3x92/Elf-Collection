# kstuff-lite - Related Source Deep Summary

## Source Identity

- Canonical name: kstuff-lite
- Type: git
- Upstream source:
  - https://github.com/EchoStretch/kstuff-lite
- Local artifact folder: [related-projects/kstuff-lite](related-projects/kstuff-lite)
- Indexed on: 2026-05-30

## Executive Summary

- `kstuff-lite` is a PS5-oriented kernel payload bundle that combines a loader, kernel-side syscall/trap hooks, crypto helpers, and debug support.
- The repo is split into a loader path, a payload path, and reusable support libraries, with build logic that produces `payload.bin` and an optional observability build.
- Its main technical value is the optimized handling of `fpkg`, `FSELF`, `NPDRM`, and mount-related flows, plus a faster crypto stack built around `isa-l_crypto` and BearSSL.

## Scope

- Topic focus: PS5 payload loading, syscall interception, package/PFS crypto, and mount automation.
- Evidence policy: findings are derived from this repository only.
- Included content:
  - top-level README and build scripts
  - `ps5-kstuff-ldr` loader
  - `ps5-kstuff/uelf` syscall and crypto handlers
  - `lib` and `prosper0gdb` build inputs
- Excluded content:
  - upstream project history outside the checked-out source
  - unrelated parent-repo knowledge base entries

## Project Structure

```text
related-projects/kstuff-lite/
├── README.md
├── ci-ps5-kstuff-ldr.sh
├── freebsd-headers/
├── gdb_stub/
├── lib/
├── prosper0gdb/
├── ps5-kstuff/
└── ps5-kstuff-ldr/
```

- High-value files:
  - [related-projects/kstuff-lite/README.md](related-projects/kstuff-lite/README.md)
  - [related-projects/kstuff-lite/ci-ps5-kstuff-ldr.sh](related-projects/kstuff-lite/ci-ps5-kstuff-ldr.sh)
  - [related-projects/kstuff-lite/ps5-kstuff/Makefile](related-projects/kstuff-lite/ps5-kstuff/Makefile)
  - [related-projects/kstuff-lite/ps5-kstuff-ldr/main.c](related-projects/kstuff-lite/ps5-kstuff-ldr/main.c)
  - [related-projects/kstuff-lite/ps5-kstuff/uelf/main.c](related-projects/kstuff-lite/ps5-kstuff/uelf/main.c)
  - [related-projects/kstuff-lite/ps5-kstuff/uelf/pfs_crypto.c](related-projects/kstuff-lite/ps5-kstuff/uelf/pfs_crypto.c)
  - [related-projects/kstuff-lite/ps5-kstuff/uelf/fpkg.c](related-projects/kstuff-lite/ps5-kstuff/uelf/fpkg.c)
  - [related-projects/kstuff-lite/ps5-kstuff/uelf/fself.c](related-projects/kstuff-lite/ps5-kstuff/uelf/fself.c)
  - [related-projects/kstuff-lite/ps5-kstuff/uelf/npdrm.c](related-projects/kstuff-lite/ps5-kstuff/uelf/npdrm.c)

## Supported Formats / Variants

| Variant | Meaning | Status | Evidence |
|---|---|---:|---|
| `payload.bin` | Standard kernel payload build | Supported | [Makefile](related-projects/kstuff-lite/ps5-kstuff/Makefile) |
| `debug-reader.bin` | Observability build gated by `KSTUFF_OBS=1` | Optional | [Makefile](related-projects/kstuff-lite/ps5-kstuff/Makefile) |
| UFS image | Loader mount target detected from source directory | Supported | [ps5-kstuff-ldr/main.c](related-projects/kstuff-lite/ps5-kstuff-ldr/main.c) |
| PFS image | Loader mount target detected from source directory | Supported | [ps5-kstuff-ldr/main.c](related-projects/kstuff-lite/ps5-kstuff-ldr/main.c) |
| exFAT image | Loader mount target detected from source directory | Supported | [ps5-kstuff-ldr/main.c](related-projects/kstuff-lite/ps5-kstuff-ldr/main.c) |
| `fpkg` crypto requests | PFS crypto mailbox path | Supported | [uelf/fpkg.c](related-projects/kstuff-lite/ps5-kstuff/uelf/fpkg.c) |
| `FSELF` handling | SELF/FSELF mailbox and trap handling | Supported | [uelf/fself.c](related-projects/kstuff-lite/ps5-kstuff/uelf/fself.c) |
| NPDRM mailbox handling | Debug RIF validation and decrypt path | Supported | [uelf/npdrm.c](related-projects/kstuff-lite/ps5-kstuff/uelf/npdrm.c) |

## Architecture / Flow

1. `ci-ps5-kstuff-ldr.sh` prepares the tree, validates `PS5_PAYLOAD_SDK`, and builds the payload side first, then the loader side. [ci script](related-projects/kstuff-lite/ci-ps5-kstuff-ldr.sh)
2. `ps5-kstuff/Makefile` assembles the kernel payload, helper objects, embedded payload binary, and optional `debug-reader` artifacts. [Makefile](related-projects/kstuff-lite/ps5-kstuff/Makefile)
3. `ps5-kstuff-ldr/main.c` maps the embedded payload, applies segment protections, calls the payload entry point, then mounts titles and watches USB changes. [loader](related-projects/kstuff-lite/ps5-kstuff-ldr/main.c)
4. `ps5-kstuff/uelf/main.c` routes intercepted syscalls to specialized handlers for `mprotect`, mount syscalls, ELF/SELF paths, and debug-related call flows. [uelf main](related-projects/kstuff-lite/ps5-kstuff/uelf/main.c)
5. `pfs_crypto.c`, `fpkg.c`, `fself.c`, and `npdrm.c` implement the crypto and file-format logic used by the payload runtime. [crypto handlers](related-projects/kstuff-lite/ps5-kstuff/uelf/pfs_crypto.c)

## Important Constants / Config / Paths

- Build flags:
  - `KSTUFF_OBS` toggles observability support and `debug-reader.bin`. [Makefile](related-projects/kstuff-lite/ps5-kstuff/Makefile)
  - `PROSPER0GDB_OPT`, `PAYLOAD_OPT`, and `UELF_OPT` tune optimization levels. [Makefile](related-projects/kstuff-lite/ps5-kstuff/Makefile)
  - `UELF_ARCH = -march=znver2 -mtune=znver2` pins the helper build to Zen 2. [Makefile](related-projects/kstuff-lite/ps5-kstuff/Makefile)
- Paths and runtime markers:
  - `/data/.kstuff_noautomount` disables automatic title mounting. [loader](related-projects/kstuff-lite/ps5-kstuff-ldr/main.c)
  - `/user/app` is the scan root for auto-mounted titles. [loader](related-projects/kstuff-lite/ps5-kstuff-ldr/main.c)
  - `/system_ex/app/<title_id>` is the bind-mount destination. [loader](related-projects/kstuff-lite/ps5-kstuff-ldr/main.c)
  - `mount.lnk` points from a title directory to the mounted source path. [loader](related-projects/kstuff-lite/ps5-kstuff-ldr/main.c)
- Crypto/cache sizes:
  - `PFS_HMAC_SHA256_CACHE_SLOTS = 2`
  - `PFS_XTS_KEY_CACHE_SLOTS = 2`
  - `SHARED_AREA_SIZE = 8192`
  - `SHARED_FAKE_KEY_SLOTS = 63` [headers](related-projects/kstuff-lite/ps5-kstuff/uelf/pfs_crypto.h), [shared area](related-projects/kstuff-lite/ps5-kstuff/uelf/shared_area.h)

## Layout and Validation Rules

- The loader first tries to detect a UFS, PFS, or exFAT image inside the source directory, then falls back to the directory itself if mounting fails. [loader](related-projects/kstuff-lite/ps5-kstuff-ldr/main.c)
- `bind_mount_title` skips a title that already has `sce_sys` mounted, unmounts partial state, creates `/system_ex/app/<title_id>`, and binds the chosen source there. [loader](related-projects/kstuff-lite/ps5-kstuff-ldr/main.c)
- `scan_and_mount_titles` honors the no-automount marker before scanning `/user/app`. [loader](related-projects/kstuff-lite/ps5-kstuff-ldr/main.c)
- `fpkg` crypto emulation accepts only recognized fake-key HMAC/XTS message shapes and rejects non-fake key handles. [fpkg](related-projects/kstuff-lite/ps5-kstuff/uelf/fpkg.c)
- `FSELF` parsing validates the header layout, distinguishes PS4 and PS5 style authinfo, and lazily loads authinfo only when needed. [fself](related-projects/kstuff-lite/ps5-kstuff/uelf/fself.c)
- `NPDRM` handling accepts mailbox cmd 5 and 6 flows, verifies the debug RIF hash, and only decrypts the secret on the cmd 6 path. [npdrm](related-projects/kstuff-lite/ps5-kstuff/uelf/npdrm.c)

## Technical Findings

1. The project is organized as a loader plus a kernel payload, not as a single monolithic binary.
   - Evidence: [ci-ps5-kstuff-ldr.sh](related-projects/kstuff-lite/ci-ps5-kstuff-ldr.sh), [ps5-kstuff/Makefile](related-projects/kstuff-lite/ps5-kstuff/Makefile), [ps5-kstuff-ldr/main.c](related-projects/kstuff-lite/ps5-kstuff-ldr/main.c)
2. The loader supports auto-mounting of images and can be disabled with a filesystem marker.
   - Evidence: [ps5-kstuff-ldr/main.c](related-projects/kstuff-lite/ps5-kstuff-ldr/main.c)
3. `uelf/main.c` is the dispatch hub for the payload, routing kernel activity into mount, ELF/SELF, NPDRM, and crypto handlers.
   - Evidence: [uelf/main.c](related-projects/kstuff-lite/ps5-kstuff/uelf/main.c)
4. `pfs_crypto.c` caches HMAC and XTS state in small ring buffers and preserves the old key split behavior expected by the payload.
   - Evidence: [pfs_crypto.c](related-projects/kstuff-lite/ps5-kstuff/uelf/pfs_crypto.c), [pfs_crypto.h](related-projects/kstuff-lite/ps5-kstuff/uelf/pfs_crypto.h)
5. `fpkg.c` coalesces adjacent XTS crypto messages and short-circuits unsupported message shapes, which is the main performance win in the package path.
   - Evidence: [fpkg.c](related-projects/kstuff-lite/ps5-kstuff/uelf/fpkg.c)
6. `fself.c` caches parsed headers and the active context snapshot, then defers authinfo loading until a caller asks for it.
   - Evidence: [fself.c](related-projects/kstuff-lite/ps5-kstuff/uelf/fself.c)
7. `npdrm.c` is wired to a debug RIF flow, not a generic NPDRM implementation, and its error handling is explicitly split by mailbox command.
   - Evidence: [npdrm.c](related-projects/kstuff-lite/ps5-kstuff/uelf/npdrm.c)
8. The build stack replaces broad crypto dependencies with a minimal `isa-l_crypto` path and a PS5-specific adapter.
   - Evidence: [build_isal_crypto.sh](related-projects/kstuff-lite/ps5-kstuff/build_isal_crypto.sh), [Makefile](related-projects/kstuff-lite/ps5-kstuff/Makefile)

## Compatibility and Behavior Notes

- The loader expects a working PS5 payload SDK via `PS5_PAYLOAD_SDK` before it can build. [ci script](related-projects/kstuff-lite/ci-ps5-kstuff-ldr.sh)
- `KSTUFF_OBS=1` changes the build surface by emitting observability artifacts and enabling shared-area snapshot support. [Makefile](related-projects/kstuff-lite/ps5-kstuff/Makefile), [shared_area.h](related-projects/kstuff-lite/ps5-kstuff/uelf/shared_area.h), [kekcall.c](related-projects/kstuff-lite/ps5-kstuff/uelf/kekcall.c)
- The payload uses PS4 and PS5 specific syscall IDs in `fself.h`, so the behavior is firmware and platform sensitive. [fself.h](related-projects/kstuff-lite/ps5-kstuff/uelf/fself.h)
- The loader’s mount behavior is intentionally permissive: if image detection or mounting fails, it falls back to the original folder path. [loader](related-projects/kstuff-lite/ps5-kstuff-ldr/main.c)

## Constraints and Caveats

- The nested `BearSSL` submodule referenced by `ps5-kstuff` was not fully retrievable in this environment through recursive update, because the upstream server rejected a pinned object. The top-level `kstuff-lite` submodule is present, but nested dependency checkout may need manual repair on another machine. [submodule metadata](related-projects/kstuff-lite/.gitmodules)
- The repo carries several performance-oriented paths that trade readability for speed, especially in the crypto and syscall dispatch code.
- `README.md` is a change summary, not a build guide, so the Makefiles and scripts are the authoritative source for build behavior. [README](related-projects/kstuff-lite/README.md), [Makefile](related-projects/kstuff-lite/ps5-kstuff/Makefile), [ci script](related-projects/kstuff-lite/ci-ps5-kstuff-ldr.sh)

## Actionable Checklist

1. Start with the loader and `ci-ps5-kstuff-ldr.sh` to understand how the payload is built and deployed.
2. Read `ps5-kstuff/uelf/main.c` and then follow the specialized handlers for `fpkg`, `fself`, `npdrm`, and PFS crypto.
3. Validate the nested submodule state before trying to reproduce the full build on a fresh machine.

## Source Index

- Local folder root: [related-projects/kstuff-lite](related-projects/kstuff-lite)
- Key local sources:
  - [related-projects/kstuff-lite/README.md](related-projects/kstuff-lite/README.md)
  - [related-projects/kstuff-lite/.gitmodules](related-projects/kstuff-lite/.gitmodules)
  - [related-projects/kstuff-lite/ci-ps5-kstuff-ldr.sh](related-projects/kstuff-lite/ci-ps5-kstuff-ldr.sh)
  - [related-projects/kstuff-lite/ps5-kstuff/Makefile](related-projects/kstuff-lite/ps5-kstuff/Makefile)
  - [related-projects/kstuff-lite/ps5-kstuff-ldr/main.c](related-projects/kstuff-lite/ps5-kstuff-ldr/main.c)
  - [related-projects/kstuff-lite/ps5-kstuff/uelf/main.c](related-projects/kstuff-lite/ps5-kstuff/uelf/main.c)
  - [related-projects/kstuff-lite/ps5-kstuff/uelf/pfs_crypto.c](related-projects/kstuff-lite/ps5-kstuff/uelf/pfs_crypto.c)
  - [related-projects/kstuff-lite/ps5-kstuff/uelf/fpkg.c](related-projects/kstuff-lite/ps5-kstuff/uelf/fpkg.c)
  - [related-projects/kstuff-lite/ps5-kstuff/uelf/fself.c](related-projects/kstuff-lite/ps5-kstuff/uelf/fself.c)
  - [related-projects/kstuff-lite/ps5-kstuff/uelf/npdrm.c](related-projects/kstuff-lite/ps5-kstuff/uelf/npdrm.c)
  - [related-projects/kstuff-lite/ps5-kstuff/uelf/kekcall.c](related-projects/kstuff-lite/ps5-kstuff/uelf/kekcall.c)
  - [related-projects/kstuff-lite/ps5-kstuff/uelf/pfs_crypto.h](related-projects/kstuff-lite/ps5-kstuff/uelf/pfs_crypto.h)
  - [related-projects/kstuff-lite/ps5-kstuff/uelf/shared_area.h](related-projects/kstuff-lite/ps5-kstuff/uelf/shared_area.h)
- Upstream references:
  - https://github.com/EchoStretch/kstuff-lite

## Reindex Notes

- Previous index date: n/a
- Delta summary:
  - Added the `kstuff-lite` git submodule and recorded it in `.gitmodules`.
  - Added the related-project deep summary and memory entry.
  - Nested `BearSSL` checkout needs follow-up on a machine that can fetch the pinned upstream object.
