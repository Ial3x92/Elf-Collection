# LibOrbisPkg — PKG/PFS Implementation Reference

- Canonical source: https://github.com/maxton/LibOrbisPkg
- Local artifact folder: [related-projects/liborbispkg](liborbispkg)
- Indexed on: 2026-05-14
- Pinned commit: `643477263b2644e0803e0f58b8726ea4e3f3b7d4`
- Source type: git repository
- Additional source checked: https://github.com/maxton/LibOrbisPkg/wiki/PKG-Information

## Executive Summary

LibOrbisPkg is a broad PS4 packaging toolkit rather than a single-purpose PFS builder. The repository combines a reusable library, GUI and CLI tools, tests, and Binary Template reference files for PKG, PFS, PFSC, SFO, and related formats. For PFS work specifically, this repository is much more complete than a minimal parser or extractor: it contains a full filesystem tree model, inode and dirent serializers, block layout logic, signed outer-image generation, optional AES-XTS encryption, PFSC wrapping for nested `pfs_image.dat`, and read paths that reconstruct signed non-contiguous file layouts. Source: [related-projects/liborbispkg/README.md](liborbispkg/README.md), [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs](liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs), [related-projects/liborbispkg/LibOrbisPkg/PFS/PfsReader.cs](liborbispkg/LibOrbisPkg/PFS/PfsReader.cs).

The repository also matters because it ties PFS creation to PKG metadata and key derivation instead of treating PFS as an isolated format. The PKG layer derives developer-controlled keys from Content ID and passcode, exposes fake-PKG EKPFS recovery, carries outer-PFS offsets and digests in the package header, and feeds those values into the PFS builder and reader flows. Source: [related-projects/liborbispkg/LibOrbisPkg/Util/Crypto.cs](liborbispkg/LibOrbisPkg/Util/Crypto.cs), [related-projects/liborbispkg/LibOrbisPkg/PKG/Pkg.cs](liborbispkg/LibOrbisPkg/PKG/Pkg.cs), [related-projects/liborbispkg/PkgTool/Program.cs](liborbispkg/PkgTool/Program.cs).

## Table of Contents

1. Repository Surface
2. Relevant Modules and Artifacts
3. PFS Build Pipeline
4. PFS Read Pipeline
5. Binary Structures, Flags, and Layout Rules
6. Flat Path Table and Collision Handling
7. PFSC Wrapping Behavior
8. PKG Key Derivation and PFS Integration
9. Verified Corrections and Caveats
10. Practical Reuse Checklist
11. Priority Source Index

## Repository Surface

Top-level repo contents show three distinct layers:

1. User-facing tools and apps:
   - `PkgEditor/` WinForms UI
   - `PkgTool/` CLI tool
   - corresponding `*.Core` projects for a reduced/core-targeted surface
2. Library implementation:
   - `LibOrbisPkg/` for PKG, PFS, SFO, GP4, PlayGo, utilities, and crypto helpers
3. Validation and reverse-engineering aids:
   - `LibOrbisPkgTests/`
   - Binary Template files like `PS4PKG.bt`, `PS4PFS.bt`, `PFSC.bt`, `SFO.bt`, and `CollisionResolver.bt`

The main solution includes the full desktop and test surface, while `LibOrbisPkg.Core.sln` narrows that to `LibOrbisPkg.Core` and `PkgTool.Core`. Source: [related-projects/liborbispkg/LibOrbisPkg.sln](liborbispkg/LibOrbisPkg.sln), [related-projects/liborbispkg/LibOrbisPkg.Core.sln](liborbispkg/LibOrbisPkg.Core.sln), [related-projects/liborbispkg](liborbispkg).

## Relevant Modules and Artifacts

### High-value implementation files

PFS construction and reading:

- [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs](liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs)
- [related-projects/liborbispkg/LibOrbisPkg/PFS/PfsReader.cs](liborbispkg/LibOrbisPkg/PFS/PfsReader.cs)
- [related-projects/liborbispkg/LibOrbisPkg/PFS/PfsStructs.cs](liborbispkg/LibOrbisPkg/PFS/PfsStructs.cs)
- [related-projects/liborbispkg/LibOrbisPkg/PFS/PfsProperties.cs](liborbispkg/LibOrbisPkg/PFS/PfsProperties.cs)
- [related-projects/liborbispkg/LibOrbisPkg/PFS/FSTree.cs](liborbispkg/LibOrbisPkg/PFS/FSTree.cs)
- [related-projects/liborbispkg/LibOrbisPkg/PFS/FlatPathTable.cs](liborbispkg/LibOrbisPkg/PFS/FlatPathTable.cs)
- [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSCReader.cs](liborbispkg/LibOrbisPkg/PFS/PFSCReader.cs)
- [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSCWriter.cs](liborbispkg/LibOrbisPkg/PFS/PFSCWriter.cs)
- [related-projects/liborbispkg/LibOrbisPkg/PFS/XtsDecryptReader.cs](liborbispkg/LibOrbisPkg/PFS/XtsDecryptReader.cs)

Crypto and PKG linkage:

- [related-projects/liborbispkg/LibOrbisPkg/Util/Crypto.cs](liborbispkg/LibOrbisPkg/Util/Crypto.cs)
- [related-projects/liborbispkg/LibOrbisPkg/Util/XtsBlockTransform.cs](liborbispkg/LibOrbisPkg/Util/XtsBlockTransform.cs)
- [related-projects/liborbispkg/LibOrbisPkg/PKG/Pkg.cs](liborbispkg/LibOrbisPkg/PKG/Pkg.cs)
- [related-projects/liborbispkg/LibOrbisPkg/PKG/Entry.cs](liborbispkg/LibOrbisPkg/PKG/Entry.cs)
- [related-projects/liborbispkg/LibOrbisPkg/PKG/PkgBuilder.cs](liborbispkg/LibOrbisPkg/PKG/PkgBuilder.cs)

Operational entry points and tests:

- [related-projects/liborbispkg/PkgTool/Program.cs](liborbispkg/PkgTool/Program.cs)
- [related-projects/liborbispkg/LibOrbisPkgTests/PfsReaderTests.cs](liborbispkg/LibOrbisPkgTests/PfsReaderTests.cs)
- [related-projects/liborbispkg/LibOrbisPkgTests/PkgBuildTest.cs](liborbispkg/LibOrbisPkgTests/PkgBuildTest.cs)

Specification aids:

- [related-projects/liborbispkg/PS4PFS.bt](liborbispkg/PS4PFS.bt)
- [related-projects/liborbispkg/PFSC.bt](liborbispkg/PFSC.bt)
- [related-projects/liborbispkg/PS4PKG.bt](liborbispkg/PS4PKG.bt)

## PFS Build Pipeline

The build path is centered on `PfsBuilder`, which performs a full filesystem-to-image transformation rather than streaming files in ad hoc order.

### Setup phase

`PfsBuilder.Setup()` does the following in order:

1. Prepares the header with block size, read-only flag, mode bits, `UnknownIndex = 1`, and a seed only when signing or encryption are enabled.
2. Collects all directories and files from the root FS tree.
3. Filters out some `sce_sys` files whose names map to known PKG entry IDs, so the PFS filesystem model deliberately excludes some metadata that is instead represented as PKG entries.
4. Creates the special superroot structure.
5. Builds directory and file inodes.
6. Creates the flat path table and optional collision resolver.
7. Computes final block allocation.

Source: [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs](liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs).

### Special root structure

The builder always creates a superroot that contains:

- `flat_path_table`
- `collision_resolver` when path-hash collisions exist
- `uroot`

The actual content tree is mounted under `uroot`, and the caller-provided root directory is renamed to `uroot` during setup. Source: [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs](liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs).

### Output ordering

`WriteData()` writes the image in this order:

1. PFS header
2. inode blocks
3. superroot dirents
4. the synthetic `flat_path_table` file
5. optional synthetic `collision_resolver` file
6. the rest of the filesystem nodes

That is not just conceptual ordering: the synthetic files are inserted into `allNodes` immediately before the final write loop. Source: [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs](liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs).

### Signed vs unsigned layout logic

`CalculateDataBlockLayout()` has two distinct code paths:

- Signed images use `DinodeS32`, maintain separate stacks for data-block signatures and final/indirect signatures, allocate explicit signature-bearing indirect blocks, and insert two special blocks after the flat path table: one empty block and one non-encrypted block tracked through `emptyBlock`.
- Unsigned images use `DinodeD32`, allocate direct data blocks linearly, and either reserve an empty block after the flat path table or write a collision resolver in that region.

This split is central to compatibility. Signed outer images are not just unsigned layouts plus HMACs; the inode shape and the indirect pointer representation differ materially. Source: [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs](liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs), [related-projects/liborbispkg/LibOrbisPkg/PFS/PfsStructs.cs](liborbispkg/LibOrbisPkg/PFS/PfsStructs.cs).

### Signing and encryption execution modes

The builder supports two write targets:

- `WriteImage(Stream)` for single-threaded write, sign, and encrypt
- `WriteImage(MemoryMappedFile, long offset)` for a memory-mapped path that parallelizes data-block signing and XTS encryption

The memory-mapped path signs ordinary data blocks in parallel, then signs indirect/final blocks afterward because those signatures depend on the already-written block-signature records. Source: [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs](liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs).

## PFS Read Pipeline

`PfsReader` is the counterpart to the builder and does more than simple contiguous extraction.

### Header and inode selection

The reader loads the first `0x400` bytes as a `PfsHeader`, then chooses inode format based on the signed flag:

- signed: `DinodeS32`, size `0x2C8`
- unsigned: `DinodeD32`, size `0xA8`

Source: [related-projects/liborbispkg/LibOrbisPkg/PFS/PfsReader.cs](liborbispkg/LibOrbisPkg/PFS/PfsReader.cs), [related-projects/liborbispkg/LibOrbisPkg/PFS/PfsStructs.cs](liborbispkg/LibOrbisPkg/PFS/PfsStructs.cs).

### Encrypted-read behavior

If the encrypted mode bit is set, `PfsReader` requires either:

- `ekpfs`, or
- both explicit tweak and data keys.

When `ekpfs` is provided, the reader derives XTS keys with `Crypto.PfsGenEncKey(ekpfs, hdr.Seed, newCrypt)` where `newCrypt` is driven by PKG `pfs_flags` bit `0x2000000000000000`. That `newCrypt` branch is an important behavior detail because it changes the key derivation path by first HMACing the seed with EKPFS before generating the encryption key. Source: [related-projects/liborbispkg/LibOrbisPkg/PFS/PfsReader.cs](liborbispkg/LibOrbisPkg/PFS/PfsReader.cs), [related-projects/liborbispkg/LibOrbisPkg/Util/Crypto.cs](liborbispkg/LibOrbisPkg/Util/Crypto.cs).

### Directory loading

`LoadDir()` walks directory blocks, reads `PfsDirent` entries until an entry size of zero, creates files immediately, and defers recursive directory loading so directory nodes can be added after the current block has been scanned. It then requires a `uroot` directory to exist at the superroot level. Source: [related-projects/liborbispkg/LibOrbisPkg/PFS/PfsReader.cs](liborbispkg/LibOrbisPkg/PFS/PfsReader.cs).

### Non-contiguous signed file handling

`LoadFile()` contains logic for signed images whose block pointers are not contiguous. It reconstructs block indices from the signed inode’s direct and indirect block-signature records. If an unsigned image appears to need non-contiguous block resolution, the reader throws because that layout is treated as invalid for unsigned images. Source: [related-projects/liborbispkg/LibOrbisPkg/PFS/PfsReader.cs](liborbispkg/LibOrbisPkg/PFS/PfsReader.cs).

### File saving and PFSC decompression

`PfsReader.File.Save()` can optionally wrap the file view in `PFSCReader` when `decompress = true` and `size != compressed_size`, which is how nested `pfs_image.dat` content can be expanded to raw PFS bytes. Source: [related-projects/liborbispkg/LibOrbisPkg/PFS/PfsReader.cs](liborbispkg/LibOrbisPkg/PFS/PfsReader.cs).

## Binary Structures, Flags, and Layout Rules

### PfsHeader

Verified header behaviors:

- `Version = 1`
- `Magic = 20130315`
- `BlockSize` defaults to `0x10000`
- `Mode` combines signed, 64-bit, encrypted, and `UnknownFlagAlwaysSet`
- `InodeBlockSig` is a `DinodeS64`-shaped record embedded in the header region
- `UnknownIndex` is written at `0x36C` only when a seed is present
- when no seed is present, the writer instead writes a fallback marker at `0x368`

The reader always reads 16 bytes from `0x370` into `Seed`, so code that treats “no seed” as semantically absent should account for that implementation detail. Source: [related-projects/liborbispkg/LibOrbisPkg/PFS/PfsStructs.cs](liborbispkg/LibOrbisPkg/PFS/PfsStructs.cs).

### Inode structures

Verified inode sizes and pointer model:

| Type | Size | Notes |
|------|------|-------|
| `DinodeD32` | `0xA8` | unsigned 32-bit image inode |
| `DinodeS32` | `0x2C8` | signed 32-bit image inode |
| `DinodeS64` | `0x310` | signed 64-bit structure used in header signature region |

Common inode model includes:

- 12 direct block slots
- 5 indirect block slots
- timestamps, UID/GID, block count, and size / compressed-size fields

Verified flags present in code:

- `compressed = 0x1`
- `readonly = 0x10`
- `internal = 0x20000`

Source: [related-projects/liborbispkg/LibOrbisPkg/PFS/PfsStructs.cs](liborbispkg/LibOrbisPkg/PFS/PfsStructs.cs).

### Dirents

`PfsDirent` entries carry inode number, type, name length, and entry size. Types used by the builder/reader include file, directory, dot, and dot-dot entries. The builder pads dirent sizes to keep 8-byte alignment, and when writing directories it jumps to the next block if there is not enough room for a maximum-size dirent at the end of the current block. Source: [related-projects/liborbispkg/LibOrbisPkg/PFS/PfsStructs.cs](liborbispkg/LibOrbisPkg/PFS/PfsStructs.cs), [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs](liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs).

### Default sizes and constants

Key constants evidenced in code:

- PFS block size default: `0x10000`
- XTS sector size: `0x1000`
- XTS starts at sector `16`
- signed block-signature record size: `36` bytes
- `emptyBlock` default in builder state: `0x4`, later adjusted during layout

Source: [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs](liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs).

## Flat Path Table and Collision Handling

`FlatPathTable` builds a sorted mapping from hashed full path to inode metadata.

Verified behaviors:

1. Hashes are computed from full image paths using repeated `hash = char.ToUpper(c) + (31 * hash)`.
2. Non-collision entries store inode number with `0x20000000` ORed in for directories.
3. Collision entries first receive `0x80000000`, then get replaced with `0x80000000 | offset` into a synthetic collision-resolver stream.
4. Collision-resolver records are emitted as dirent-style entries whose names are full paths.
5. Each collision group is followed by `0x18` bytes of padding or spacing in the resolver stream.

Source: [related-projects/liborbispkg/LibOrbisPkg/PFS/FlatPathTable.cs](liborbispkg/LibOrbisPkg/PFS/FlatPathTable.cs).

The builder wires these into the superroot automatically, so `flat_path_table` is always present and `collision_resolver` is conditional on collision detection. Source: [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs](liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs).

## PFSC Wrapping Behavior

PFSC in this repository is a block wrapper around nested PFS payloads, especially `pfs_image.dat`.

### Writer behavior

`FSFile(PfsBuilder)` constructs `pfs_image.dat` by:

1. creating a `PFSCWriter`
2. writing only the PFSC header and block pointer table
3. streaming the nested PFS image bytes immediately after the PFSC header using `OffsetStream`

The writer comment is explicit: it “doesn't actually do compression or anything interesting.” Its pointer table is laid out as if each block is stored at full size after the header. Source: [related-projects/liborbispkg/LibOrbisPkg/PFS/FSTree.cs](liborbispkg/LibOrbisPkg/PFS/FSTree.cs), [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSCWriter.cs](liborbispkg/LibOrbisPkg/PFS/PFSCWriter.cs).

### Reader behavior

`PFSCReader`:

- checks PFSC magic and basic header fields
- loads the block-offset table
- treats `sectorSize == blockSize` as uncompressed or direct-copy
- treats `sectorSize > blockSize` as a zero-filled block
- treats `sectorSize < blockSize` as deflate-compressed data and decompresses after skipping a 2-byte prefix

So the read path is more expressive than the write path. The repository can read compressed PFSC sectors even though the bundled writer does not currently emit them. Source: [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSCReader.cs](liborbispkg/LibOrbisPkg/PFS/PFSCReader.cs), [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSCWriter.cs](liborbispkg/LibOrbisPkg/PFS/PFSCWriter.cs).

## PKG Key Derivation and PFS Integration

### Derived keys from Content ID and passcode

`Crypto.ComputeKeys(ContentId, Passcode, Index)` computes a 32-byte derived key by SHA-256 hashing a 96-byte concatenation of:

1. `SHA256(index_be_4bytes)`
2. `SHA256(ContentId padded to 48 bytes)`
3. the 32-byte ASCII passcode

`Index = 1` is the EKPFS path used throughout the PFS pipeline. Source: [related-projects/liborbispkg/LibOrbisPkg/Util/Crypto.cs](liborbispkg/LibOrbisPkg/Util/Crypto.cs).

This matches the checked wiki description for developer-controlled keys and is also used throughout the codebase from GP4 creation, PkgBuilder, and CLI flows. Source: [related-projects/liborbispkg/LibOrbisPkg/Util/Crypto.cs](liborbispkg/LibOrbisPkg/Util/Crypto.cs), [related-projects/liborbispkg/PkgTool/Program.cs](liborbispkg/PkgTool/Program.cs), https://github.com/maxton/LibOrbisPkg/wiki/PKG-Information#developer-controlled-keys.

### PFS-specific key generation

Verified PFS key helpers:

- `PfsGenCryptoKey(ekpfs, seed, index)` performs `HMACSHA256(ekpfs, index || seed)` where `index` is copied from `BitConverter.GetBytes(index)` and is therefore little-endian on typical target platforms.
- `PfsGenEncKey(ekpfs, seed, newCrypt = false)` generates a 32-byte encryption digest for index `1`, then splits it into 16-byte tweak and data keys.
- `PfsGenSignKey(ekpfs, seed)` uses index `2`.

The `newCrypt` branch changes the HMAC key to `HMACSHA256(ekpfs, seed)` before deriving the encryption key. That behavior is present in code even though it is not captured in the wiki summary. Source: [related-projects/liborbispkg/LibOrbisPkg/Util/Crypto.cs](liborbispkg/LibOrbisPkg/Util/Crypto.cs), https://github.com/maxton/LibOrbisPkg/wiki/PKG-Information#pfs-key-generation.

### Fake PKG and IMAGE_KEY linkage

`Pkg.GetEkpfs()` attempts fake-PKG EKPFS recovery by:

1. decrypting derived key 3 with the known fake-PKG RSA keyset
2. hashing the `IMAGE_KEY` metadata plus `dk3` to produce the AES IV/key material
3. decrypting the `IMAGE_KEY` entry bytes with AES-CBC or CFB128 helper logic
4. RSA-decrypting the resulting payload with the fake mount-image keyset

Source: [related-projects/liborbispkg/LibOrbisPkg/PKG/Pkg.cs](liborbispkg/LibOrbisPkg/PKG/Pkg.cs).

### ENTRY_KEYS construction

`KeysEntry` stores:

- a seed digest derived from the padded Content ID
- seven per-index derived-key digests as `SHA256(dk) XOR dk`
- seven RSA-encrypted key records

Index 0 stores the passcode itself in the RSA-encrypted payload slot instead of the normal derived key bytes. Source: [related-projects/liborbispkg/LibOrbisPkg/PKG/Entry.cs](liborbispkg/LibOrbisPkg/PKG/Entry.cs).

### PKG-to-PFS operational flow

The CLI makes the repo’s intended end-to-end flow explicit:

1. `pfs_buildinner` builds an unsigned inner PFS from a GP4 project.
2. `pfs_buildouter` derives EKPFS from Content ID and passcode, then builds a signed outer PFS that embeds `pfs_image.dat`.
3. `pkg_build` creates the fake PKG around the generated content.
4. extraction verbs reverse the process by opening the PKG, deriving or recovering EKPFS, opening the outer PFS, then decoding `pfs_image.dat` through PFSC and `PfsReader`.

Source: [related-projects/liborbispkg/PkgTool/Program.cs](liborbispkg/PkgTool/Program.cs), [related-projects/liborbispkg/README.md](liborbispkg/README.md).

## Verified Corrections and Caveats

These points were checked directly against source and should be carried forward when reusing prior notes.

1. `PfsGenCryptoKey` uses platform-endian `BitConverter.GetBytes(index)`, which is effectively little-endian on normal targets. This differs from `ComputeKeys`, which explicitly hashes a big-endian index representation. Source: [related-projects/liborbispkg/LibOrbisPkg/Util/Crypto.cs](liborbispkg/LibOrbisPkg/Util/Crypto.cs).
2. `PfsGenEncKey` has a `newCrypt` mode triggered by PKG `pfs_flags`; this is a real code path, not just a theoretical future hook. Source: [related-projects/liborbispkg/LibOrbisPkg/PFS/PfsReader.cs](liborbispkg/LibOrbisPkg/PFS/PfsReader.cs), [related-projects/liborbispkg/LibOrbisPkg/Util/Crypto.cs](liborbispkg/LibOrbisPkg/Util/Crypto.cs).
3. `PfsProperties.MakeOuterPFSProps()` hardcodes the outer-PFS seed to 16 zero bytes with a comment that it does not seem to matter for verification. That is a repository-specific behavior, not a general protocol claim. Source: [related-projects/liborbispkg/LibOrbisPkg/PFS/PfsProperties.cs](liborbispkg/LibOrbisPkg/PFS/PfsProperties.cs).
4. `PFSCWriter` is not a general compression writer. It writes a valid PFSC framing/header and a full-block offset table, then stores raw nested PFS bytes after the header. Source: [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSCWriter.cs](liborbispkg/LibOrbisPkg/PFS/PFSCWriter.cs), [related-projects/liborbispkg/LibOrbisPkg/PFS/FSTree.cs](liborbispkg/LibOrbisPkg/PFS/FSTree.cs).
5. `PFSCReader` can read true compressed sectors and also has a zero-fill branch when a mapped sector length exceeds the nominal block size. Source: [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSCReader.cs](liborbispkg/LibOrbisPkg/PFS/PFSCReader.cs).
6. The builder intentionally filters some `sce_sys` members out of the image tree if their names are already represented as PKG entries. Source: [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs](liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs).
7. The repository includes tests that specifically validate encrypted-reader key requirements and round-trip PKG build/read behavior, which makes the implementation more trustworthy than a code drop without executable checks. Source: [related-projects/liborbispkg/LibOrbisPkgTests/PfsReaderTests.cs](liborbispkg/LibOrbisPkgTests/PfsReaderTests.cs), [related-projects/liborbispkg/LibOrbisPkgTests/PkgBuildTest.cs](liborbispkg/LibOrbisPkgTests/PkgBuildTest.cs).

### Unknowns and partials

Still unresolved or only partially documented in-source:

- several inode flags beyond `compressed`, `readonly`, and `internal`
- the exact semantic meaning of header fallback data written at `0x368` when no seed is present
- when the `newCrypt` `pfs_flags` mode appears in real images and how broadly it is used outside this implementation
- whether a fully general PFSC writer with adaptive compression exists elsewhere in the ecosystem; it is not present in this repo

## Practical Reuse Checklist

For future implementation or verification work derived from this repository alone:

1. Recreate the two-stage model: inner unsigned PFS, then signed outer PFS containing PFSC-wrapped `pfs_image.dat`.
2. Mirror the superroot layout exactly: `flat_path_table`, optional `collision_resolver`, then `uroot`.
3. Preserve separate signed and unsigned inode layouts; do not treat signatures as metadata attached to a common inode struct.
4. Match `FlatPathTable` hashing and collision encoding byte-for-byte.
5. Preserve the signed-image block-signature graph and the ordering dependency between data-block signatures and indirect or final signatures.
6. Preserve XTS behavior exactly: sector size `0x1000`, start sector `16`, and the builder’s empty-block skip behavior.
7. Keep `ComputeKeys` and `PfsGenCryptoKey` endianness behavior distinct.
8. Implement the `newCrypt` branch if compatibility with images flagged that way matters.
9. Treat PFSC writer behavior here as framing-only unless you intentionally add real per-block compression.
10. Use the tests and Binary Template files as verification aids, not just the library code.

## Priority Source Index

Start here for the fastest technical revalidation:

1. [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs](liborbispkg/LibOrbisPkg/PFS/PFSBuilder.cs) — builder orchestration, block layout, signing, encryption, superroot wiring.
2. [related-projects/liborbispkg/LibOrbisPkg/PFS/PfsReader.cs](liborbispkg/LibOrbisPkg/PFS/PfsReader.cs) — read path, encrypted access, non-contiguous signed-file reconstruction.
3. [related-projects/liborbispkg/LibOrbisPkg/PFS/PfsStructs.cs](liborbispkg/LibOrbisPkg/PFS/PfsStructs.cs) — header, inode, dirent, flags, and sizes.
4. [related-projects/liborbispkg/LibOrbisPkg/Util/Crypto.cs](liborbispkg/LibOrbisPkg/Util/Crypto.cs) — derived keys, EKPFS, PFS HMAC helpers, keystone generation.
5. [related-projects/liborbispkg/LibOrbisPkg/PFS/FlatPathTable.cs](liborbispkg/LibOrbisPkg/PFS/FlatPathTable.cs) — hash and collision behavior.
6. [related-projects/liborbispkg/LibOrbisPkg/PFS/FSTree.cs](liborbispkg/LibOrbisPkg/PFS/FSTree.cs) — build-time tree model and PFSC-wrapped `pfs_image.dat` creation.
7. [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSCReader.cs](liborbispkg/LibOrbisPkg/PFS/PFSCReader.cs) and [related-projects/liborbispkg/LibOrbisPkg/PFS/PFSCWriter.cs](liborbispkg/LibOrbisPkg/PFS/PFSCWriter.cs) — nested-image wrapper behavior.
8. [related-projects/liborbispkg/LibOrbisPkg/PKG/Pkg.cs](liborbispkg/LibOrbisPkg/PKG/Pkg.cs) and [related-projects/liborbispkg/LibOrbisPkg/PKG/Entry.cs](liborbispkg/LibOrbisPkg/PKG/Entry.cs) — PKG header linkage, EKPFS recovery, ENTRY_KEYS details.
9. [related-projects/liborbispkg/PkgTool/Program.cs](liborbispkg/PkgTool/Program.cs) — intended CLI workflows and integration sequence.
10. [related-projects/liborbispkg/LibOrbisPkgTests/PfsReaderTests.cs](liborbispkg/LibOrbisPkgTests/PfsReaderTests.cs) and [related-projects/liborbispkg/LibOrbisPkgTests/PkgBuildTest.cs](liborbispkg/LibOrbisPkgTests/PkgBuildTest.cs) — executable expectations.
11. [related-projects/liborbispkg/PS4PFS.bt](liborbispkg/PS4PFS.bt), [related-projects/liborbispkg/PFSC.bt](liborbispkg/PFSC.bt), and [related-projects/liborbispkg/PS4PKG.bt](liborbispkg/PS4PKG.bt) — auxiliary reverse-engineering references.
12. Upstream wiki page: https://github.com/maxton/LibOrbisPkg/wiki/PKG-Information
