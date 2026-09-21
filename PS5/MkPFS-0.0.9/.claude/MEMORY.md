# Project Memory

This file is a curated, durable knowledge base for active development and testing in this repository.
Keep entries concise, source-backed, and oriented toward repeatable workflows.

## How To Use This Memory

- Read this file first for high-signal project context before deep investigation.
- Treat this as a navigation layer; use linked source files as the ground truth.
- Prefer adding compact bullets over long prose.
- When behavior changes, update the related section and keep references current.

## Core References

- [PyPI project guidelines](rules/pypi-project-guidelines.md) — packaging checklist, README guidance, and release-validation references.
- [Root agent rules](../AGENTS.md) — canonical coding, testing, and style expectations used by local agent workflows.
- [Claude agent mirror](../CLAUDE.md) — synchronized agent guidance used by local `.claude` workflows.
- Architecture map: keep CLI wiring in [`mkpfs/cli.py`](../mkpfs/cli.py), and keep PFS format/build/inspection logic in [`mkpfs/pfs.py`](../mkpfs/pfs.py).
- Shared modules: constants in [`mkpfs/consts.py`](../mkpfs/consts.py), progress/tree scan in [`mkpfs/pbar.py`](../mkpfs/pbar.py), helpers in [`mkpfs/utils.py`](../mkpfs/utils.py).
- Current CLI surface: `create`, `check` (`verify` alias), `ls`, `info`, `analyze` (`analyse` alias), and `extract`; keep docs and smoke tests aligned.
- CLI smoke test anchor: [`tests/test_main.py`](../tests/test_main.py) validates help output text and should be updated when CLI description text changes.
- Convenience validation script: [`run-tests.sh`](../run-tests.sh) runs `uv sync`, installs pre-commit hooks, runs Ruff format/check with `--fix`, then runs pytest.

## Related Projects Knowledge Base

### ShadowMountPlus

- Repository: https://github.com/drakmor/ShadowMountPlus
- Submodule folder: [related-projects/shadowmountplus](../related-projects/shadowmountplus)
- Maintained research report: [related-projects/ShadowMountPlus.md](../related-projects/ShadowMountPlus.md)

Short summary:

- ShadowMountPlus auto-detects game folders and image files, mounts them, stages metadata, and registers titles for launch.
- Supported image extensions: .ffpkg (ufs), .exfat (exfatfs), .ffpfs (pfs, experimental).
- For .ffpfs, mounting uses LVD attach + pfs nmount options and then validates mounted block size vs chosen sector size.
- Practical compatibility requirements for generated images include image-root layout, valid sce_sys/param.json, and eboot.bin present at image root.

How to inspect this knowledge quickly:

- Start with the report: [related-projects/ShadowMountPlus.md](../related-projects/ShadowMountPlus.md).
- Then inspect original source code under: [related-projects/shadowmountplus](../related-projects/shadowmountplus).
- Priority files for mount and filesystem behavior:
	- [related-projects/shadowmountplus/src/sm_image.c](../related-projects/shadowmountplus/src/sm_image.c)
	- [related-projects/shadowmountplus/include/sm_mount_defs.h](../related-projects/shadowmountplus/include/sm_mount_defs.h)
	- [related-projects/shadowmountplus/src/sm_mount_device.c](../related-projects/shadowmountplus/src/sm_mount_device.c)
	- [related-projects/shadowmountplus/src/sm_scan_tree.c](../related-projects/shadowmountplus/src/sm_scan_tree.c)
	- [related-projects/shadowmountplus/src/sm_scan.c](../related-projects/shadowmountplus/src/sm_scan.c)
	- [related-projects/shadowmountplus/src/sm_gameinfo.c](../related-projects/shadowmountplus/src/sm_gameinfo.c)
	- [related-projects/shadowmountplus/src/sm_install.c](../related-projects/shadowmountplus/src/sm_install.c)
	- [related-projects/shadowmountplus/src/sm_filesystem.c](../related-projects/shadowmountplus/src/sm_filesystem.c)
	- [related-projects/shadowmountplus/src/sm_config_mount.c](../related-projects/shadowmountplus/src/sm_config_mount.c)
	- [related-projects/shadowmountplus/config.ini.example](../related-projects/shadowmountplus/config.ini.example)

### PKGTool

- Repository/source: https://github.com/thesupersonic16/PKGTool
- Artifact folder: [related-projects/pkgtool](../related-projects/pkgtool)
- Deep summary: [related-projects/pkgtool.md](../related-projects/pkgtool.md)

Short summary:

- PKGTool provides a practical parser/extractor for `.pkg` archives through `PKGArchive` and a partial repack writer.
- On-disk table entries are fixed `0x54` bytes and use little-endian integer fields in this implementation.
- Decompression is custom marker/back-reference based (`ReadAndDecompress`) and loops to decompressed size.
- Writer currently leaves CRC unimplemented and writes entries as uncompressed with zeroed compression/attribute block.
- Repack behavior is non-recursive and effectively basename-oriented by default, which matters for faithful recreation tooling.

How to inspect this knowledge quickly:

- Start with summary: [related-projects/pkgtool.md](../related-projects/pkgtool.md)
- Validate against source folder: [related-projects/pkgtool](../related-projects/pkgtool)
- Priority files/pages:
	- [related-projects/pkgtool/PKGTool/PKGArchive.cs](../related-projects/pkgtool/PKGTool/PKGArchive.cs)
	- [related-projects/pkgtool/PKGTool/Program.cs](../related-projects/pkgtool/PKGTool/Program.cs)
	- [related-projects/pkgtool/PKGTool/PKGTool.csproj](../related-projects/pkgtool/PKGTool/PKGTool.csproj)
	- [related-projects/pkgtool/PKGTool.sln](../related-projects/pkgtool/PKGTool.sln)
	- [related-projects/pkgtool/.gitmodules](../related-projects/pkgtool/.gitmodules)
	- [related-projects/pkgtool/HedgeLib/HedgeLib/IO/ExtendedBinary.cs](../related-projects/pkgtool/HedgeLib/HedgeLib/IO/ExtendedBinary.cs)
	- [related-projects/pkgtool/HedgeLib/HedgeLib/Archives/Archive.cs](../related-projects/pkgtool/HedgeLib/HedgeLib/Archives/Archive.cs)
	- [related-projects/pkgtool/HedgeLib/HedgeLib/Archives/ArchiveFile.cs](../related-projects/pkgtool/HedgeLib/HedgeLib/Archives/ArchiveFile.cs)

### LibOrbisPkg

- Repository/source: https://github.com/maxton/LibOrbisPkg
- Artifact folder: [related-projects/liborbispkg](../related-projects/liborbispkg)
- Deep summary: [related-projects/liborbispkg.md](../related-projects/liborbispkg.md)

Short summary:

- LibOrbisPkg is a full PKG and PFS toolkit with reusable library code, GUI and CLI tools, tests, and Binary Template references.
- The PFS implementation includes tree modeling, inode and dirent serialization, flat path table generation, signed outer-image layout, and optional AES-XTS encryption.
- The PKG layer derives developer-controlled keys from Content ID and passcode, exposes fake-PKG EKPFS recovery, and carries the PFS offsets, flags, and digests needed to open nested images.
- PFSC support is asymmetric: the reader handles compressed and direct sectors, while the bundled writer emits header plus full-block mapping for nested `pfs_image.dat` content.
- A notable compatibility detail is the `newCrypt` branch in `PfsGenEncKey`, which is triggered from PKG `pfs_flags` during PFS reads.

How to inspect this knowledge quickly:

- Start with summary: [related-projects/liborbispkg.md](../related-projects/liborbispkg.md)
- Validate against source folder: [related-projects/liborbispkg](../related-projects/liborbispkg)
- Priority files/pages:
	- [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs](../related-projects/liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs)
	- [related-projects/liborbispkg/LibOrbisPkg/PFS/PfsReader.cs](../related-projects/liborbispkg/LibOrbisPkg/PFS/PfsReader.cs)
	- [related-projects/liborbispkg/LibOrbisPkg/PFS/PfsStructs.cs](../related-projects/liborbispkg/LibOrbisPkg/PFS/PfsStructs.cs)
	- [related-projects/liborbispkg/LibOrbisPkg/Util/Crypto.cs](../related-projects/liborbispkg/LibOrbisPkg/Util/Crypto.cs)
	- [related-projects/liborbispkg/LibOrbisPkg/PFS/FlatPathTable.cs](../related-projects/liborbispkg/LibOrbisPkg/PFS/FlatPathTable.cs)
	- [related-projects/liborbispkg/LibOrbisPkg/PFS/FSTree.cs](../related-projects/liborbispkg/LibOrbisPkg/PFS/FSTree.cs)
	- [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSCReader.cs](../related-projects/liborbispkg/LibOrbisPkg/PFS/PFSCReader.cs)
	- [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSCWriter.cs](../related-projects/liborbispkg/LibOrbisPkg/PFS/PFSCWriter.cs)
	- [related-projects/liborbispkg/LibOrbisPkg/PKG/Pkg.cs](../related-projects/liborbispkg/LibOrbisPkg/PKG/Pkg.cs)
	- [related-projects/liborbispkg/LibOrbisPkg/PKG/Entry.cs](../related-projects/liborbispkg/LibOrbisPkg/PKG/Entry.cs)
	- [related-projects/liborbispkg/PkgTool/Program.cs](../related-projects/liborbispkg/PkgTool/Program.cs)
	- [related-projects/liborbispkg/LibOrbisPkgTests/PfsReaderTests.cs](../related-projects/liborbispkg/LibOrbisPkgTests/PfsReaderTests.cs)
	- [related-projects/liborbispkg/LibOrbisPkgTests/PkgBuildTest.cs](../related-projects/liborbispkg/LibOrbisPkgTests/PkgBuildTest.cs)

### LibOrbisPkg Wiki

- Repository/source: https://github.com/maxton/LibOrbisPkg.wiki.git
- Artifact folder: [related-projects/liborbispkg-wiki](../related-projects/liborbispkg-wiki)
- Deep summary: [related-projects/liborbispkg-wiki.md](../related-projects/liborbispkg-wiki.md)

Short summary:

- The wiki is a compact orientation layer for the LibOrbisPkg library plus the PkgEditor and PkgTool frontends.
- Its highest-value page is the PKG crypto note covering passcode-derived keys, EKPFS, PFS key derivation, and `ENTRY_KEYS` / `IMAGE_KEY` roles.
- The PkgEditor page captures user-facing PKG build requirements such as the 36-character content ID format and the required `Image0/sce_sys/param.sfo`.
- The library page is best used as a namespace and capability map, not a stable API contract.
- The PkgTool wiki page is currently only a placeholder and should not be treated as authoritative CLI documentation.

How to inspect this knowledge quickly:

- Start with summary: [related-projects/liborbispkg-wiki.md](../related-projects/liborbispkg-wiki.md)
- Validate against snapshot folder: [related-projects/liborbispkg-wiki](../related-projects/liborbispkg-wiki)
- Priority files/pages:
	- [related-projects/liborbispkg-wiki/PKG-Information.md](../related-projects/liborbispkg-wiki/PKG-Information.md)
	- [related-projects/liborbispkg-wiki/PkgEditor.md](../related-projects/liborbispkg-wiki/PkgEditor.md)
	- [related-projects/liborbispkg-wiki/Library.md](../related-projects/liborbispkg-wiki/Library.md)
	- [related-projects/liborbispkg-wiki/Home.md](../related-projects/liborbispkg-wiki/Home.md)
  - [related-projects/liborbispkg-wiki/PkgTool.md](../related-projects/liborbispkg-wiki/PkgTool.md)
  - [related-projects/liborbispkg-wiki/manifest.md](../related-projects/liborbispkg-wiki/manifest.md)

### kstuff-lite

- Repository/source: https://github.com/EchoStretch/kstuff-lite
- Artifact folder: [related-projects/kstuff-lite](../related-projects/kstuff-lite)
- Deep summary: [related-projects/kstuff-lite.md](../related-projects/kstuff-lite.md)

Short summary:

- kstuff-lite is a PS5 payload bundle with a loader, kernel syscall hooks, mount automation, and crypto helpers.
- The loader can mount UFS, PFS, or exFAT images from a source directory and falls back to the raw folder path if mounting fails.
- `KSTUFF_OBS=1` enables observability artifacts and shared-area snapshot support.
- The crypto stack focuses on `fpkg`, `FSELF`, and debug NPDRM handling, with small caches for repeated HMAC and XTS work.

How to inspect this knowledge quickly:

- Start with summary: [related-projects/kstuff-lite.md](../related-projects/kstuff-lite.md)
- Validate against source folder: [related-projects/kstuff-lite](../related-projects/kstuff-lite)
- Priority files:
  - [related-projects/kstuff-lite/README.md](../related-projects/kstuff-lite/README.md)
  - [related-projects/kstuff-lite/ci-ps5-kstuff-ldr.sh](../related-projects/kstuff-lite/ci-ps5-kstuff-ldr.sh)
  - [related-projects/kstuff-lite/.gitmodules](../related-projects/kstuff-lite/.gitmodules)
  - [related-projects/kstuff-lite/ps5-kstuff/Makefile](../related-projects/kstuff-lite/ps5-kstuff/Makefile)
  - [related-projects/kstuff-lite/ps5-kstuff-ldr/main.c](../related-projects/kstuff-lite/ps5-kstuff-ldr/main.c)
  - [related-projects/kstuff-lite/ps5-kstuff/uelf/main.c](../related-projects/kstuff-lite/ps5-kstuff/uelf/main.c)
  - [related-projects/kstuff-lite/ps5-kstuff/uelf/pfs_crypto.c](../related-projects/kstuff-lite/ps5-kstuff/uelf/pfs_crypto.c)
  - [related-projects/kstuff-lite/ps5-kstuff/uelf/fpkg.c](../related-projects/kstuff-lite/ps5-kstuff/uelf/fpkg.c)
  - [related-projects/kstuff-lite/ps5-kstuff/uelf/fself.c](../related-projects/kstuff-lite/ps5-kstuff/uelf/fself.c)
  - [related-projects/kstuff-lite/ps5-kstuff/uelf/npdrm.c](../related-projects/kstuff-lite/ps5-kstuff/uelf/npdrm.c)

### Other Knowledge Sources

- Repository/source: mixed local archive from PSDevWiki, ShadPKG docs, and Wololo
- Artifact folder: [related-projects/other-knowledge-sources](../related-projects/other-knowledge-sources)
- Deep summary: [related-projects/other-knowledge-sources.md](../related-projects/other-knowledge-sources.md)

Short summary:

- This archive combines permanent PSDevWiki snapshots, a detailed ShadPKG HOWWORKS markdown, and a Wololo article preserving Flatz's FPKG writeup.
- The ShadPKG markdown is the strongest implementation-level source here for PKG decryption, PFS key derivation, AES-XTS, PFSC block handling, and extraction flow.
- The PSDevWiki PFS snapshot and its local derivative index are the clearest structure-oriented references for headers, inode and dirent layout, `uroot`, and `flat_path_table` behavior.
- Provenance and re-export details are tracked inside the folder README and `source-manifest.md`, including archive date, publication or revision identity, and upstream URLs.

How to inspect this knowledge quickly:

- Start with summary: [related-projects/other-knowledge-sources.md](../related-projects/other-knowledge-sources.md)
- Validate against archive folder: [related-projects/other-knowledge-sources](../related-projects/other-knowledge-sources)
- Priority files/pages:
	- [related-projects/other-knowledge-sources/shadpkg-howworks-raw.md](../related-projects/other-knowledge-sources/shadpkg-howworks-raw.md)
	- [related-projects/other-knowledge-sources/psdevwiki-pfs-index.md](../related-projects/other-knowledge-sources/psdevwiki-pfs-index.md)
	- [related-projects/other-knowledge-sources/psdevwiki-pfs.html](../related-projects/other-knowledge-sources/psdevwiki-pfs.html)
	- [related-projects/other-knowledge-sources/psdevwiki-pkg-files.html](../related-projects/other-knowledge-sources/psdevwiki-pkg-files.html)
	- [related-projects/other-knowledge-sources/source-manifest.md](../related-projects/other-knowledge-sources/source-manifest.md)

## Update Standard

- Keep each entry factual, short, and tied to concrete source links.
- Prefer stable paths over temporary artifacts.
- Do not store scratch notes here; use tmp for transient work.
