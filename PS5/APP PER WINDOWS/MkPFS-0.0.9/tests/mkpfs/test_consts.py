import unittest

import mkpfs.consts as consts


class TestCoreConstants(unittest.TestCase):
    """Tests for core PFS constants exposed by the constants module."""

    def test_core_constants_match_expected_baseline_values(self) -> None:
        """The most frequently used core constants should keep their expected baseline values."""
        self.assertEqual(consts.PFS_MAGIC, 20130315)
        self.assertIn(consts.PFS_VERSION_PS4, (1,))
        self.assertEqual(consts.SIG_SIZE, 32)


class TestPFSMagicAndVersion(unittest.TestCase):
    """Tests for PFS magic number and version constants."""

    def test_pfs_magic(self) -> None:
        """Verify PFS magic number matches legacy implementation."""
        assert consts.PFS_MAGIC == 20130315

    def test_pfs_version_ps4(self) -> None:
        """Verify PS4 version constant."""
        assert consts.PFS_VERSION_PS4 == 1

    def test_pfs_version_ps5(self) -> None:
        """Verify PS5 version constant."""
        assert consts.PFS_VERSION_PS5 == 2

    def test_pfs_version_default(self) -> None:
        """Verify default PFS version is PS5."""
        assert consts.PFS_VERSION == consts.PFS_VERSION_PS5


class TestPFSModeFlags(unittest.TestCase):
    """Tests for PFS mode flags."""

    def test_pfs_mode_signed(self) -> None:
        """Verify signed mode flag."""
        assert consts.PFS_MODE_SIGNED == 0x1

    def test_pfs_mode_64bit_inodes(self) -> None:
        """Verify 64-bit inodes mode flag."""
        assert consts.PFS_MODE_64BIT_INODES == 0x2

    def test_pfs_mode_encrypted(self) -> None:
        """Verify encrypted mode flag."""
        assert consts.PFS_MODE_ENCRYPTED == 0x4

    def test_pfs_mode_case_insensitive(self) -> None:
        """Verify case-insensitive mode flag."""
        assert consts.PFS_MODE_CASE_INSENSITIVE == 0x8


class TestInodeModeFlags(unittest.TestCase):
    """Tests for inode mode permission flags."""

    def test_inode_mode_o_read(self) -> None:
        """Verify other read permission flag."""
        assert consts.INODE_MODE_O_READ == 0x001

    def test_inode_mode_o_write(self) -> None:
        """Verify other write permission flag."""
        assert consts.INODE_MODE_O_WRITE == 0x002

    def test_inode_mode_o_exec(self) -> None:
        """Verify other execute permission flag."""
        assert consts.INODE_MODE_O_EXEC == 0x004

    def test_inode_mode_g_read(self) -> None:
        """Verify group read permission flag."""
        assert consts.INODE_MODE_G_READ == 0x008

    def test_inode_mode_g_write(self) -> None:
        """Verify group write permission flag."""
        assert consts.INODE_MODE_G_WRITE == 0x010

    def test_inode_mode_g_exec(self) -> None:
        """Verify group execute permission flag."""
        assert consts.INODE_MODE_G_EXEC == 0x020

    def test_inode_mode_u_read(self) -> None:
        """Verify user read permission flag."""
        assert consts.INODE_MODE_U_READ == 0x040

    def test_inode_mode_u_write(self) -> None:
        """Verify user write permission flag."""
        assert consts.INODE_MODE_U_WRITE == 0x080

    def test_inode_mode_u_exec(self) -> None:
        """Verify user execute permission flag."""
        assert consts.INODE_MODE_U_EXEC == 0x100

    def test_inode_mode_dir(self) -> None:
        """Verify directory mode flag."""
        assert consts.INODE_MODE_DIR == 0x4000

    def test_inode_mode_file(self) -> None:
        """Verify regular file mode flag."""
        assert consts.INODE_MODE_FILE == 0x8000


class TestInodeModeComposites(unittest.TestCase):
    """Tests for composite inode mode flags derived from individual flags."""

    def test_inode_mode_any_write(self) -> None:
        """Verify composite any-write flag equals OR of all write bits."""
        expected: int = consts.INODE_MODE_O_WRITE | consts.INODE_MODE_G_WRITE | consts.INODE_MODE_U_WRITE
        assert expected == consts.INODE_MODE_ANY_WRITE
        assert consts.INODE_MODE_ANY_WRITE == 0x092

    def test_inode_rx_only(self) -> None:
        """Verify read-execute-only permission mask."""
        expected: int = (
            consts.INODE_MODE_O_READ
            | consts.INODE_MODE_O_EXEC
            | consts.INODE_MODE_G_READ
            | consts.INODE_MODE_G_EXEC
            | consts.INODE_MODE_U_READ
            | consts.INODE_MODE_U_EXEC
        )
        assert expected == consts.INODE_RX_ONLY
        assert consts.INODE_RX_ONLY == 0x16D
        assert consts.INODE_RX_ONLY == 365


class TestInodeFlags(unittest.TestCase):
    """Tests for inode flags."""

    def test_inode_flag_compressed(self) -> None:
        """Verify compressed flag."""
        assert consts.INODE_FLAG_COMPRESSED == 0x1

    def test_inode_flag_readonly(self) -> None:
        """Verify read-only flag."""
        assert consts.INODE_FLAG_READONLY == 0x10

    def test_inode_flag_internal(self) -> None:
        """Verify internal flag."""
        assert consts.INODE_FLAG_INTERNAL == 0x20000

    def test_inode_flag_signed_extra(self) -> None:
        """Verify signed extra flag is composite."""
        expected: int = 0x4 | 0x8
        assert expected == consts.INODE_FLAG_SIGNED_EXTRA
        assert consts.INODE_FLAG_SIGNED_EXTRA == 0x0C


class TestDirentTypes(unittest.TestCase):
    """Tests for directory entry type constants."""

    def test_dirent_type_file(self) -> None:
        """Verify file entry type."""
        assert consts.DIRENT_TYPE_FILE == 2

    def test_dirent_type_directory(self) -> None:
        """Verify directory entry type."""
        assert consts.DIRENT_TYPE_DIRECTORY == 3

    def test_dirent_type_dot(self) -> None:
        """Verify dot (current directory) entry type."""
        assert consts.DIRENT_TYPE_DOT == 4

    def test_dirent_type_dotdot(self) -> None:
        """Verify dotdot (parent directory) entry type."""
        assert consts.DIRENT_TYPE_DOTDOT == 5


class TestInodeSizes(unittest.TestCase):
    """Tests for inode structure size constants."""

    def test_inode_d32_size(self) -> None:
        """Verify 32-bit inode structure size."""
        assert consts.INODE_D32_SIZE == 0xA8
        assert consts.INODE_D32_SIZE == 168

    def test_inode_s32_size(self) -> None:
        """Verify 32-bit signed inode structure size."""
        assert consts.INODE_S32_SIZE == 0x2C8
        assert consts.INODE_S32_SIZE == 712

    def test_inode_s64_size(self) -> None:
        """Verify 64-bit signed inode structure size."""
        assert consts.INODE_S64_SIZE == 0x310
        assert consts.INODE_S64_SIZE == 784


class TestBlockIndirection(unittest.TestCase):
    """Tests for block indirection constants."""

    def test_max_direct_blocks(self) -> None:
        """Verify maximum number of direct block pointers in inode."""
        assert consts.MAX_DIRECT_BLOCKS == 12

    def test_max_indirect_blocks(self) -> None:
        """Verify maximum number of indirect block pointers in inode."""
        assert consts.MAX_INDIRECT_BLOCKS == 5


class TestSignatureConstants(unittest.TestCase):
    """Tests for signature-related constants."""

    def test_sig_entry_size(self) -> None:
        """Verify signature entry size."""
        assert consts.SIG_ENTRY_SIZE == 36

    def test_sig_size(self) -> None:
        """Verify signature size."""
        assert consts.SIG_SIZE == 32


class TestIntegerLimits(unittest.TestCase):
    """Tests for integer limit constants."""

    def test_uint32_max(self) -> None:
        """Verify maximum unsigned 32-bit integer."""
        assert consts.UINT32_MAX == 0xFFFFFFFF
        assert consts.UINT32_MAX == 4294967295

    def test_int32_max(self) -> None:
        """Verify maximum signed 32-bit integer."""
        assert consts.INT32_MAX == 0x7FFFFFFF
        assert consts.INT32_MAX == 2147483647


class TestBinaryConstants(unittest.TestCase):
    """Tests for binary/bytes constants."""

    def test_zero_ekpfs(self) -> None:
        """Verify zero EKPFS constant (32 zero bytes)."""
        assert consts.ZERO_EKPFS == b"\x00" * 32
        assert len(consts.ZERO_EKPFS) == 32

    def test_zero_pfs_seed(self) -> None:
        """Verify zero PFS seed constant (16 zero bytes)."""
        assert consts.ZERO_PFS_SEED == b"\x00" * 16
        assert len(consts.ZERO_PFS_SEED) == 16


class TestHeaderConstants(unittest.TestCase):
    """Tests for header-related constants."""

    def test_header_digest_offset(self) -> None:
        """Verify header digest offset."""
        assert consts.HEADER_DIGEST_OFFSET == 0x380
        assert consts.HEADER_DIGEST_OFFSET == 896

    def test_header_digest_size(self) -> None:
        """Verify header digest size."""
        assert consts.HEADER_DIGEST_SIZE == 0x5A0
        assert consts.HEADER_DIGEST_SIZE == 1440


class TestPFSCConstants(unittest.TestCase):
    """Tests for PFSC-related compression constants."""

    def test_pfsc_magic(self) -> None:
        """Verify PFSC magic value."""
        assert consts.PFSC_MAGIC == 0x43534650

    def test_pfsc_unknown_fields(self) -> None:
        """Verify PFSC unknown header fields match the reference layout."""
        assert consts.PFSC_UNK4 == 0
        assert consts.PFSC_UNK8 == 6

    def test_pfsc_logical_block_size(self) -> None:
        """Verify PFSC logical block size value."""
        assert consts.PFSC_LOGICAL_BLOCK_SIZE == 0x10000

    def test_pfsc_header_size(self) -> None:
        """Verify PFSC header size value."""
        assert consts.PFSC_HEADER_SIZE == 0x30

    def test_pfsc_offset_entry_size(self) -> None:
        """Verify PFSC offset entry size value."""
        assert consts.PFSC_OFFSET_ENTRY_SIZE == 0x8

    def test_pfsc_layout_offsets(self) -> None:
        """Verify PFSC header/table offset constants match the reference layout."""
        assert consts.PFSC_BLOCK_OFFSETS_OFFSET == 0x400
        assert consts.PFSC_INITIAL_DATA_OFFSET == 0x10000


class TestConstantConsistency(unittest.TestCase):
    """Tests for internal consistency and relationships between constants."""

    def test_pfs_mode_flags_are_powers_of_two(self) -> None:
        """Verify PFS mode flags are distinct power-of-two values."""
        flags: list[int] = [
            consts.PFS_MODE_SIGNED,
            consts.PFS_MODE_64BIT_INODES,
            consts.PFS_MODE_ENCRYPTED,
            consts.PFS_MODE_CASE_INSENSITIVE,
        ]
        # Check all are powers of 2
        for flag in flags:
            assert flag & (flag - 1) == 0, f"Flag {hex(flag)} is not power of 2"
        # Check all are distinct
        assert len(flags) == len(set(flags)), "Duplicate flags found"

    def test_permission_flags_no_overlap(self) -> None:
        """Verify permission flags don't overlap."""
        flags: list[int] = [
            consts.INODE_MODE_O_READ,
            consts.INODE_MODE_O_WRITE,
            consts.INODE_MODE_O_EXEC,
            consts.INODE_MODE_G_READ,
            consts.INODE_MODE_G_WRITE,
            consts.INODE_MODE_G_EXEC,
            consts.INODE_MODE_U_READ,
            consts.INODE_MODE_U_WRITE,
            consts.INODE_MODE_U_EXEC,
        ]
        for i, flag_a in enumerate(flags):
            for flag_b in flags[i + 1 :]:
                assert (flag_a & flag_b) == 0, f"Flags {hex(flag_a)} and {hex(flag_b)} overlap"

    def test_file_type_flags_distinct(self) -> None:
        """Verify file type flags are distinct."""
        flags: list[int] = [
            consts.INODE_MODE_DIR,
            consts.INODE_MODE_FILE,
        ]
        assert len(flags) == len(set(flags)), "Duplicate file type flags"
        assert (consts.INODE_MODE_DIR & consts.INODE_MODE_FILE) == 0

    def test_dirent_types_sequential(self) -> None:
        """Verify directory entry types are sequential."""
        assert consts.DIRENT_TYPE_FILE == 2
        assert consts.DIRENT_TYPE_DIRECTORY == 3
        assert consts.DIRENT_TYPE_DOT == 4
        assert consts.DIRENT_TYPE_DOTDOT == 5

    def test_inode_flag_no_overlap(self) -> None:
        """Verify inode flags don't overlap."""
        flags: list[int] = [
            consts.INODE_FLAG_COMPRESSED,
            consts.INODE_FLAG_READONLY,
            consts.INODE_FLAG_INTERNAL,
        ]
        for i, flag_a in enumerate(flags):
            for flag_b in flags[i + 1 :]:
                assert (flag_a & flag_b) == 0, f"Inode flags {hex(flag_a)} and {hex(flag_b)} overlap"

    def test_version_constants_increasing(self) -> None:
        """Verify PS4 version is less than PS5 version."""
        assert consts.PFS_VERSION_PS4 < consts.PFS_VERSION_PS5
