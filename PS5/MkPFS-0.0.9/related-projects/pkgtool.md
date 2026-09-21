# PKGTool — PKG Container Reverse-Engineering Reference

- Canonical source: https://github.com/thesupersonic16/PKGTool
- Local artifact folder: [related-projects/pkgtool](pkgtool)
- Indexed on: 2026-05-14
- Source type: git repository (with recursive submodules)

## Executive Summary

PKGTool provides a practical read/extract and partial write/repack implementation for a PKG archive format via `PKGArchive`. Its strongest value is that the repository contains both the archive parser/writer and the supporting HedgeLib reader/writer primitives needed to verify the binary layout directly from source. Its write path is intentionally incomplete and includes constraints that matter for any faithful reimplementation.

## Table of Contents

1. Scope and Identity
2. Project Structure
3. Supported Workflow Modes
4. Plain-English: How PKG Works Here
5. On-Disk Format Specification
6. Compression Stream Behavior
7. Read/Extract Flow
8. Write/Repack Flow
9. Key Constraints and Implementation Gaps
10. HedgeLib Dependency Findings
11. Python Implementation Blueprint
12. Source Index
13. Reindex Delta vs Older Draft

## Scope and Identity

This reference focuses on the PKG container format as implemented by this repository:

- Archive class: `HedgeLib.Archives.PKGArchive`
- Core parser/writer: [related-projects/pkgtool/PKGTool/PKGArchive.cs](pkgtool/PKGTool/PKGArchive.cs)
- CLI orchestration: [related-projects/pkgtool/PKGTool/Program.cs](pkgtool/PKGTool/Program.cs)

Note on naming:

- Your legacy draft used "PSF/PKG" terminology.
- This repository itself implements a `.pkg` archive format only (class name `PKGArchive`).

## Project Structure

```text
related-projects/pkgtool/
├── .gitmodules
├── PKGTool.sln
├── PKGTool/
│   ├── PKGArchive.cs
│   ├── Program.cs
│   ├── Addon.cs
│   └── PKGTool.csproj
└── HedgeLib/                  # submodule (cloned recursively)
    ├── HedgeLib/
    │   ├── IO/ExtendedBinary.cs
    │   └── Archives/
    │       ├── Archive.cs
    │       └── ArchiveFile.cs
    └── HedgeTools/...
```

High-value files:

- [related-projects/pkgtool/PKGTool/PKGArchive.cs](pkgtool/PKGTool/PKGArchive.cs)
- [related-projects/pkgtool/PKGTool/Program.cs](pkgtool/PKGTool/Program.cs)
- [related-projects/pkgtool/PKGTool/PKGTool.csproj](pkgtool/PKGTool/PKGTool.csproj)
- [related-projects/pkgtool/PKGTool.sln](pkgtool/PKGTool.sln)
- [related-projects/pkgtool/.gitmodules](pkgtool/.gitmodules)
- [related-projects/pkgtool/HedgeLib/HedgeLib/IO/ExtendedBinary.cs](pkgtool/HedgeLib/HedgeLib/IO/ExtendedBinary.cs)
- [related-projects/pkgtool/HedgeLib/HedgeLib/Archives/Archive.cs](pkgtool/HedgeLib/HedgeLib/Archives/Archive.cs)
- [related-projects/pkgtool/HedgeLib/HedgeLib/Archives/ArchiveFile.cs](pkgtool/HedgeLib/HedgeLib/Archives/ArchiveFile.cs)

## Supported Workflow Modes

| Mode | Behavior | Status in Tool |
|------|----------|----------------|
| Extract from `.pkg` | Parses header/table, loads entries, decompresses flagged payloads | Implemented |
| Repack from directory | Adds files to archive and writes table/payloads | Implemented (limited) |
| Write compressed entries | Compression flag/stream emission during save | Not implemented |
| CRC32 generation | CRC field at header offset 0x00 | Not implemented |

Evidence:

- Load path and decompress branch in [related-projects/pkgtool/PKGTool/PKGArchive.cs](pkgtool/PKGTool/PKGArchive.cs)
- Save path TODO comments and hardcoded values in [related-projects/pkgtool/PKGTool/PKGArchive.cs](pkgtool/PKGTool/PKGArchive.cs)

## Plain-English: How PKG Works Here

### PKG in plain English

Think of a `.pkg` file here as a simple archive container:

- The start of the file has a tiny header (CRC placeholder + file count).
- Then comes a fixed-size table that says, for each file:
   - the file name,
   - original size,
   - stored size,
   - where the payload lives in the file,
   - and whether payload bytes are compressed.
- After the table, payload bytes are stored, and each table row points to its payload offset.

How PKG is loaded in PKGTool:

1. Read file count from header.
2. Read all table rows.
3. Jump to each row's payload offset.
4. If compressed flag is off, read bytes directly.
5. If compressed flag is on, run PKGTool's custom decode routine and rebuild original bytes.

How PKG is written in PKGTool today:

- It writes a valid table + payload layout for uncompressed entries.
- It does not currently compute real CRC.
- It does not currently write compressed payload streams.
- File names are stored in a fixed 64-byte field, so long names are a practical hazard.

Primary PKG implementation references:

- [related-projects/pkgtool/PKGTool/PKGArchive.cs](pkgtool/PKGTool/PKGArchive.cs)
- [related-projects/pkgtool/PKGTool/Program.cs](pkgtool/PKGTool/Program.cs)

Quick mental model:

- PKG is a file archive table + payload blobs.
- PKGTool reads the table first, then follows offsets to each payload.
- If a payload is flagged compressed, PKGTool expands it with its custom back-reference decoder before exposing the file bytes.

## On-Disk Format Specification

Endianness:

- Reader/writer are created with `isBigEndian = false` in `PKGArchive`.
- In HedgeLib, `ExtendedBinaryReader` / `ExtendedBinaryWriter` default to little-endian when `IsBigEndian == false`.

Evidence:

- [related-projects/pkgtool/PKGTool/PKGArchive.cs](pkgtool/PKGTool/PKGArchive.cs)
- [related-projects/pkgtool/HedgeLib/HedgeLib/IO/ExtendedBinary.cs](pkgtool/HedgeLib/HedgeLib/IO/ExtendedBinary.cs)

### Header

- `0x00..0x03`: CRC32 placeholder (`uint32`) (not actually computed by tool)
- `0x04..0x07`: file count (`int32`)

### File table

Per-entry size is `0x54` bytes (`84`):

- `0x00..0x3F` (64 bytes): filename buffer
- `0x40..0x43` (`uint32`): uncompressed size
- `0x44..0x47` (`uint32`): stored size
- `0x48..0x4B` (`uint32`): absolute payload offset
- `0x4C` (`byte`): compressed flag (`1` or `0`)
- `0x4D..0x4F` (3 bytes): unknown attributes

Reader behavior:

- `ReadSignature(0x40).Replace("\0", "")` strips all NUL characters from the raw name field.

Writer behavior:

- Creates `char[0x40]`, copies file name, writes fixed 64-char field.

Evidence:

- [related-projects/pkgtool/PKGTool/PKGArchive.cs](pkgtool/PKGTool/PKGArchive.cs)

## Compression Stream Behavior

Compressed entries are decoded by `ReadAndDecompress` in [related-projects/pkgtool/PKGTool/PKGArchive.cs](pkgtool/PKGTool/PKGArchive.cs).

### Compressed payload header (12 bytes)

- `uint32 decompressedSize`
- `uint32 compressedSize`
- `byte copyByte` (escape marker)
- `3 bytes` reserved/skipped

### Decode algorithm

Loop while output length `< decompressedSize`:

1. Read byte `b`.
2. If `b != copyByte`, emit `b` literally.
3. If `b == copyByte`:
   - Read `returnByte`.
   - If `returnByte == copyByte`, emit one literal `copyByte`.
   - Else:
     - If `returnByte >= copyByte`, decrement `returnByte` by 1.
     - Compute `offset = output_position - returnByte`.
     - Read `length` byte.
     - Seek output stream to `offset`, read `length` bytes, seek back, append them.

Important implementation notes:

- Decode termination is controlled by `decompressedSize`, not `compressedSize`.
- `compressedSize` is read but not used as a hard decode bound.
- Back-reference copy relies on seeking in output stream; there are no explicit guardrails in this method for malformed offsets.

## Read/Extract Flow

`Program.Main` dispatches:

- Existing file path -> `ExtractPKG`
- Existing directory path -> `RepackPKG`

Extract flow in [related-projects/pkgtool/PKGTool/Program.cs](pkgtool/PKGTool/Program.cs):

1. Create output directory named after input file stem.
2. `PKGArchive.Load(path)`.
3. For each `ArchiveFile`, call `Extract` to disk.

Load flow in [related-projects/pkgtool/PKGTool/PKGArchive.cs](pkgtool/PKGTool/PKGArchive.cs):

1. Skip 4-byte CRC field.
2. Read file count.
3. Parse `fileCount` table entries.
4. Seek to each `DataOffset`.
5. If `Compressed` -> decode via `ReadAndDecompress`; else read raw bytes sized by `DataUncompressedSize`.
6. Add `ArchiveFile { Name, Data }` to archive list.

## Write/Repack Flow

Repack flow in [related-projects/pkgtool/PKGTool/Program.cs](pkgtool/PKGTool/Program.cs):

1. `archive.AddDirectory(dirPath, false)`
2. `archive.Save(dirPath + ".pkg")`

Save flow in [related-projects/pkgtool/PKGTool/PKGArchive.cs](pkgtool/PKGTool/PKGArchive.cs):

1. Reserve 4-byte CRC offset via `AddOffset("crc32")`.
2. Write file count.
3. For each file:
   - Write 64-char filename buffer.
   - Write uncompressed size.
   - Write stored size (same value).
   - Reserve payload offset.
   - Write `0u` for compression/attrs block.
4. Fill each payload offset and write payload data.
5. Fill CRC with `0u`.

Offset semantics:

- `FillInOffset` writes absolute offsets by default in HedgeLib writer.

Evidence:

- [related-projects/pkgtool/HedgeLib/HedgeLib/IO/ExtendedBinary.cs](pkgtool/HedgeLib/HedgeLib/IO/ExtendedBinary.cs)

## Key Constraints and Implementation Gaps

These are revalidated against current source and important for faithful reimplementation:

1. CRC is placeholder-only.
2. Writer does not emit compressed entries.
3. Unknown 3-byte attribute field semantics are not preserved/populated.
4. Repack is non-recursive (`AddDirectory(..., false)`).
5. Repack path flattening risk:
   - `ArchiveFile(filePath)` stores only basename in `Name`.
   - Directory hierarchy is not represented in entry names by default.
6. Filename length hazard:
   - Writer uses `char[0x40]` and `file.Name.CopyTo(...)` with no truncation handling.
   - Names > 64 chars can throw during save.
7. Decompressor does not validate `compressedSize` as a strict bound.

Evidence:

- [related-projects/pkgtool/PKGTool/PKGArchive.cs](pkgtool/PKGTool/PKGArchive.cs)
- [related-projects/pkgtool/HedgeLib/HedgeLib/Archives/Archive.cs](pkgtool/HedgeLib/HedgeLib/Archives/Archive.cs)
- [related-projects/pkgtool/HedgeLib/HedgeLib/Archives/ArchiveFile.cs](pkgtool/HedgeLib/HedgeLib/Archives/ArchiveFile.cs)

## HedgeLib Dependency Findings

The legacy draft noted incomplete dependency checkout. In this reindex run, the repo was cloned with recursive submodules and `HedgeLib` is present locally.

Project wiring:

- `PKGTool.csproj` references:
  - `..\HedgeLib\HedgeLib\HedgeLib.csproj`
  - `..\HedgeLib\HedgeTools\HedgeArchiveEditor\HedgeArchiveEditor.csproj`
- `PKGTool.sln` includes `PKGTool`, `HedgeLib`, and `HedgeArchiveEditor` projects.
- PKGTool `.gitmodules` declares `HedgeLib` submodule URL.

Evidence:

- [related-projects/pkgtool/PKGTool/PKGTool.csproj](pkgtool/PKGTool/PKGTool.csproj)
- [related-projects/pkgtool/PKGTool.sln](pkgtool/PKGTool.sln)
- [related-projects/pkgtool/.gitmodules](pkgtool/.gitmodules)

## Implementation Blueprint

### Stage 1: Reader parity first

Implement `read_pkg(path)` mirroring C# parse behavior exactly:

- Header and table fields as little-endian.
- Fixed 64-byte name parsing and NUL cleanup.
- Decompress path behavior parity (`copyByte` semantics, loop by decompressed size).

### Stage 2: Stable uncompressed writer

Implement `write_pkg_uncompressed(entries)`:

- Header with CRC placeholder.
- Entry table with fixed `0x54` records.
- Absolute offsets.
- Compression flag off.
- Attr bytes zeroed.

### Stage 3: Round-trip fixtures

Validate against C# tool behavior:

- Python write -> C# extract parity.
- C# write -> Python read parity.
- Edge fixtures: long names, nested directories, unusual bytes.

### Stage 4: Compression and CRC reverse-engineering

- Implement compressor compatible with `ReadAndDecompress`.
- Determine CRC algorithm/coverage from real corpus.
- Determine semantics of 3-byte attrs via differential analysis.

## Source Index

Core PKGTool sources:

- [related-projects/pkgtool/PKGTool/PKGArchive.cs](pkgtool/PKGTool/PKGArchive.cs)
- [related-projects/pkgtool/PKGTool/Program.cs](pkgtool/PKGTool/Program.cs)
- [related-projects/pkgtool/PKGTool/Addon.cs](pkgtool/PKGTool/Addon.cs)
- [related-projects/pkgtool/PKGTool/PKGTool.csproj](pkgtool/PKGTool/PKGTool.csproj)
- [related-projects/pkgtool/PKGTool.sln](pkgtool/PKGTool.sln)
- [related-projects/pkgtool/.gitmodules](pkgtool/.gitmodules)

Supporting HedgeLib definitions used by PKGTool:

- [related-projects/pkgtool/HedgeLib/HedgeLib/IO/ExtendedBinary.cs](pkgtool/HedgeLib/HedgeLib/IO/ExtendedBinary.cs)
- [related-projects/pkgtool/HedgeLib/HedgeLib/Archives/Archive.cs](pkgtool/HedgeLib/HedgeLib/Archives/Archive.cs)
- [related-projects/pkgtool/HedgeLib/HedgeLib/Archives/ArchiveFile.cs](pkgtool/HedgeLib/HedgeLib/Archives/ArchiveFile.cs)

Upstream references:

- https://github.com/thesupersonic16/PKGTool
- https://github.com/Radfordhound/HedgeLib

## Reindex Delta vs Older Draft

Validated and retained:

- Header/table shape (`0x54` entries) and decompression control-byte mechanics.
- CRC placeholder and non-compressed writer behavior.

Updated from re-scan:

- Repository now cloned with recursive submodules; HedgeLib source is available locally and was used to validate binary helper behavior.
- Repack limitations now explicitly include non-recursive input and filename flattening behavior inherited from `ArchiveFile` and `AddDirectory(..., false)`.
- Added explicit risk note for names exceeding 64-char fixed entry field.
