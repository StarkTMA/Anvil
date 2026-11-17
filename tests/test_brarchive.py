import io
import struct
from pathlib import Path

import pytest
from click.testing import CliRunner

from anvil.cli import cli
from anvil.lib.brarchive import (
    MAGIC,
    BadArchiveError,
    BrArchive,
    BrArchivePacker,
    InvalidEntryError,
    SecurityError,
    UnsupportedVersionError,
    sanitize_path,
)


def test_empty_archive():
    buf = io.BytesIO()
    with BrArchive(buf, mode="w") as arc:
        pass

    raw = buf.getvalue()
    assert len(raw) == 16  # Only the 16-byte header
    reader = BrArchive.from_bytes(raw)
    assert len(reader) == 0
    assert reader.namelist() == []


def test_writestr_and_read_roundtrip():
    buf = io.BytesIO()
    with BrArchive(buf, mode="w") as arc:
        arc.writestr("entities/zombie.json", b'{"id":"zombie"}')
        arc.writestr("entities/skeleton.json", '{"id":"skeleton"}')

    raw = buf.getvalue()
    reader = BrArchive.from_bytes(raw)

    assert len(reader) == 2
    assert "entities/zombie.json" in reader
    assert "entities/creeper.json" not in reader
    assert reader["entities/zombie.json"] == b'{"id":"zombie"}'
    assert reader["entities/skeleton.json"] == b'{"id":"skeleton"}'
    assert set(reader.namelist()) == {"entities/zombie.json", "entities/skeleton.json"}
    assert set(iter(reader)) == {"entities/zombie.json", "entities/skeleton.json"}

    with pytest.raises(KeyError):
        _ = reader["non_existent.json"]


def test_binary_asset_preservation():
    mcb_bytes = b"\x7fMCB\x01\x00\xd2\x20\xde\x77\x00\xff" * 50
    buf = io.BytesIO()
    with BrArchive(buf, mode="w") as arc:
        arc.writestr("particles/spark.mcb", mcb_bytes)

    reader = BrArchive.from_bytes(buf.getvalue())
    assert reader.read("particles/spark.mcb") == mcb_bytes


def test_stream_slice_reading():
    payload = b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    buf = io.BytesIO()
    with BrArchive(buf, mode="w") as arc:
        arc.writestr("sample.txt", payload)

    reader = BrArchive.from_bytes(buf.getvalue())
    with reader.open("sample.txt") as stream:
        assert stream.read(10) == b"0123456789"
        assert stream.tell() == 10
        assert stream.read(10) == b"ABCDEFGHIJ"
        stream.seek(0)
        assert stream.read() == payload


def test_deduplication_effectiveness():
    shared_data = b"TEXTURE_PIXEL_DATA" * 500  # 9000 bytes
    buf_dedup = io.BytesIO()
    with BrArchive(buf_dedup, mode="w", deduplicate=True) as arc:
        arc.writestr("tex/block1.png", shared_data)
        arc.writestr("tex/block2.png", shared_data)
        arc.writestr("tex/block3.png", shared_data)

    raw_dedup = buf_dedup.getvalue()
    expected_content_size = len(shared_data)  # stored once
    expected_archive_size = 16 + (3 * 256) + expected_content_size
    assert len(raw_dedup) == expected_archive_size

    # Without deduplication
    buf_no_dedup = io.BytesIO()
    with BrArchive(buf_no_dedup, mode="w", deduplicate=False) as arc:
        arc.writestr("tex/block1.png", shared_data)
        arc.writestr("tex/block2.png", shared_data)
        arc.writestr("tex/block3.png", shared_data)

    raw_no_dedup = buf_no_dedup.getvalue()
    assert len(raw_no_dedup) == 16 + (3 * 256) + (len(shared_data) * 3)

    # Both read back identical entries
    reader = BrArchive.from_bytes(raw_dedup)
    assert reader["tex/block1.png"] == shared_data
    assert reader["tex/block2.png"] == shared_data
    assert reader["tex/block3.png"] == shared_data


def test_pack_and_unpack_nested_directory(tmp_path):
    src_dir = tmp_path / "resource_pack"
    src_dir.mkdir()
    (src_dir / "manifest.json").write_bytes(b'{"format_version": 2}')

    textures = src_dir / "textures" / "items"
    textures.mkdir(parents=True)
    (textures / "diamond_sword.png").write_bytes(b"SWORD_PNG")
    (textures / "iron_axe.png").write_bytes(b"AXE_PNG")

    archive_file = tmp_path / "rp.brarchive"
    result = BrArchive.pack(src_dir, archive_file)
    assert result == archive_file
    assert archive_file.exists()

    # Unpack to destination
    dest_dir = tmp_path / "unpacked_rp"
    BrArchive.unpack(archive_file, dest_dir)

    assert (dest_dir / "manifest.json").read_bytes() == b'{"format_version": 2}'
    assert (dest_dir / "textures" / "items" / "diamond_sword.png").read_bytes() == b"SWORD_PNG"
    assert (dest_dir / "textures" / "items" / "iron_axe.png").read_bytes() == b"AXE_PNG"


def test_extract_single_entry(tmp_path):
    src_dir = tmp_path / "pack"
    src_dir.mkdir()
    (src_dir / "file1.txt").write_bytes(b"file 1")
    (src_dir / "file2.txt").write_bytes(b"file 2")

    archive_path = BrArchive.pack(src_dir, tmp_path / "test.brarchive")

    extract_dest = tmp_path / "extracted_single"
    with BrArchive(archive_path, mode="r") as arc:
        out_file = arc.extract("file2.txt", extract_dest)
        assert out_file.exists()
        assert out_file.read_bytes() == b"file 2"
        assert not (extract_dest / "file1.txt").exists()


def test_path_sanitization_and_security():
    assert sanitize_path(r"models\entity\zombie.geo.json") == "models/entity/zombie.geo.json"
    assert sanitize_path("/textures/blocks/stone.png/") == "textures/blocks/stone.png"

    with pytest.raises(InvalidEntryError):
        sanitize_path("")

    with pytest.raises(InvalidEntryError):
        sanitize_path("   ///   ")

    with pytest.raises(InvalidEntryError):
        sanitize_path("null\0byte.png")

    with pytest.raises(InvalidEntryError):
        sanitize_path("a" * 248)

    with pytest.raises(SecurityError):
        sanitize_path("../secret.txt")

    with pytest.raises(SecurityError):
        sanitize_path("sub/../../traversal.txt")

    with pytest.raises(SecurityError):
        sanitize_path("C:/System32/cmd.exe")


def test_security_traversal_on_extraction(tmp_path):
    buf = bytearray()
    buf.extend(struct.pack("<QII", MAGIC, 1, 1))

    desc = bytearray(256)
    evil_name = b"../../malicious.txt"
    desc[0] = len(evil_name)
    desc[1 : 1 + len(evil_name)] = evil_name
    struct.pack_into("<II", desc, 248, 0, 4)
    buf.extend(desc)
    buf.extend(b"DATA")

    with pytest.raises(SecurityError):
        BrArchive.from_bytes(bytes(buf))


def test_corrupt_archive_detection():
    # Bad magic
    with pytest.raises(BadArchiveError):
        BrArchive.from_bytes(struct.pack("<QII", 0x11223344, 0, 1))

    # Unsupported version
    with pytest.raises(UnsupportedVersionError):
        BrArchive.from_bytes(struct.pack("<QII", MAGIC, 0, 99))

    # Truncated descriptor table
    with pytest.raises(BadArchiveError):
        BrArchive.from_bytes(struct.pack("<QII", MAGIC, 5, 1) + b"\x00" * 20)

    # Content offset exceeds total archive size
    bad_offset_archive = bytearray()
    bad_offset_archive.extend(struct.pack("<QII", MAGIC, 1, 1))
    desc = bytearray(256)
    name = b"test.txt"
    desc[0] = len(name)
    desc[1 : 1 + len(name)] = name
    struct.pack_into("<II", desc, 248, 9999, 100)  # offset 9999 out of bounds
    bad_offset_archive.extend(desc)
    bad_offset_archive.extend(b"SHORT")
    with pytest.raises(BadArchiveError):
        BrArchive.from_bytes(bytes(bad_offset_archive))


def test_exclude_patterns_on_pack(tmp_path):
    src_dir = tmp_path / "dirty_folder"
    src_dir.mkdir()
    (src_dir / "valid.json").write_bytes(b"{}")
    (src_dir / "Thumbs.db").write_bytes(b"thumbs")
    (src_dir / "temp.tmp").write_bytes(b"temp")
    git_dir = src_dir / ".git"
    git_dir.mkdir()
    (git_dir / "config").write_bytes(b"gitconfig")

    arc_path = BrArchive.pack(src_dir, tmp_path / "cleaned.brarchive")
    with BrArchive(arc_path, mode="r") as arc:
        assert arc.namelist() == ["valid.json"]


def test_cli_integration(tmp_path):
    runner = CliRunner()

    src_dir = tmp_path / "cli_test_pack"
    src_dir.mkdir()
    (src_dir / "data1.json").write_bytes(b'{"val": 1}')
    (src_dir / "data2.json").write_bytes(b'{"val": 1}')

    archive_file = tmp_path / "cli_pack.brarchive"

    # 1. pack
    res_pack = runner.invoke(cli, ["brarchive", "pack", str(src_dir), "-o", str(archive_file)])
    assert res_pack.exit_code == 0, res_pack.output
    assert archive_file.exists()

    # 2. list
    res_list = runner.invoke(cli, ["archive", "list", str(archive_file)])
    assert res_list.exit_code == 0, res_list.output
    assert "data1.json" in res_list.output
    assert "data2.json" in res_list.output
    assert "Deduplication save:" in res_list.output

    # 3. extract single
    extract_target = tmp_path / "cli_single"
    res_extract = runner.invoke(
        cli, ["bra", "extract", str(archive_file), "-e", "data1.json", "-o", str(extract_target)]
    )
    assert res_extract.exit_code == 0, res_extract.output
    assert (extract_target / "data1.json").read_bytes() == b'{"val": 1}'

    # 4. unpack
    unpack_target = tmp_path / "cli_unpacked"
    res_unpack = runner.invoke(cli, ["brarch", "u", str(archive_file), "-o", str(unpack_target)])
    assert res_unpack.exit_code == 0, res_unpack.output
    assert (unpack_target / "data1.json").read_bytes() == b'{"val": 1}'
    assert (unpack_target / "data2.json").read_bytes() == b'{"val": 1}'


# ---------------------------------------------------------------------------
# Baking packs into the __brarchive layout
# ---------------------------------------------------------------------------


def _descriptors(path: Path) -> list[tuple[str, int, int]]:
    raw = path.read_bytes()
    _, count, _ = struct.unpack_from("<QII", raw, 0)
    out = []
    for i in range(count):
        d = 16 + i * 256
        name = raw[d + 1 : d + 1 + raw[d]].decode()
        offset, size = struct.unpack_from("<II", raw, d + 248)
        out.append((name, offset, size))
    return out


def test_empty_entries_point_at_offset_zero(tmp_path):
    arc = BrArchive(deduplicate=False)
    arc.writestr("a.json", b"{}")
    arc.writestr("b.ogg", b"")
    arc.writestr("c.json", b"[]")
    path = arc.save(tmp_path / "x.brarchive")
    assert _descriptors(path) == [("a.json", 0, 2), ("b.ogg", 0, 0), ("c.json", 2, 2)]


def _make_pack(root: Path) -> Path:
    files = {
        "manifest.json": b"{}",
        "pack_icon.png": b"png",
        "textures/terrain_texture.json": b'{"t":1}',
        "textures/item_texture.json": b'{"i":1}',
        "textures/starktma/blocks/ruby_ore.png": b"ruby",
        "sounds/mob/hit.ogg": b"ogg",
        "materials/entity.material": b"mat",
        "structures/house.mcstructure": b"nbt",
        "texts/en_US.lang": b"lang",
        "entity/thing.entity.json": b'{"e":1}',
        "scripts/main.js": b"js",
    }
    for rel, data in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return root


def test_bake_pack_layout(tmp_path):
    pack = _make_pack(tmp_path / "RP")
    BrArchivePacker.bake(pack)
    arc = pack / "__brarchive"

    archives = sorted(p.relative_to(arc).as_posix() for p in arc.rglob("*.brarchive"))
    assert archives == [
        "entity.brarchive",
        "materials.brarchive",
        "sounds.brarchive",
        "sounds/mob.brarchive",
        "structures.brarchive",
        "texts.brarchive",
        "textures.brarchive",
        "textures/starktma.brarchive",
        "textures/starktma/blocks.brarchive",
    ]
    # One archive per folder, bare names, sorted; folders with only subfolders are empty
    assert _descriptors(arc / "textures.brarchive") == [
        ("item_texture.json", 0, 7),
        ("terrain_texture.json", 7, 7),
    ]
    assert _descriptors(arc / "textures/starktma.brarchive") == []
    assert _descriptors(arc / "textures/starktma/blocks.brarchive") == [("ruby_ore.png", 0, 4)]
    # Files that stay loose are listed as empty entries
    assert _descriptors(arc / "texts.brarchive") == [("en_US.lang", 0, 0)]
    # Sounds, materials and structures are stored with their data
    assert _descriptors(arc / "structures.brarchive") == [("house.mcstructure", 0, 3)]
    assert _descriptors(arc / "sounds/mob.brarchive") == [("hit.ogg", 0, 3)]
    assert _descriptors(arc / "materials.brarchive") == [("entity.material", 0, 3)]

    # Stored files are removed, except the ones the game also reads loose
    assert not (pack / "textures/item_texture.json").exists()
    assert (pack / "textures/terrain_texture.json").exists()
    assert not (pack / "textures/starktma").exists()
    assert not (pack / "entity").exists()
    assert not (pack / "sounds").exists()
    assert not (pack / "materials").exists()
    assert not (pack / "structures").exists()
    assert (pack / "texts/en_US.lang").exists()
    # The pack root and scripts are left alone
    assert (pack / "manifest.json").exists() and (pack / "pack_icon.png").exists()
    assert (pack / "scripts/main.js").exists()
    assert not (arc / "scripts.brarchive").exists()



def test_bake_packs_loot_tables(tmp_path):
    pack = tmp_path / "BP"
    (pack / "loot_tables/entities").mkdir(parents=True)
    (pack / "loot_tables/entities/ruby_golem.json").write_bytes(b'{"pools":[]}')
    BrArchivePacker.bake(pack)
    assert not (pack / "loot_tables").exists()
    arc = BrArchive(pack / "__brarchive/loot_tables/entities.brarchive")
    assert arc.read("ruby_golem.json") == b'{"pools":[]}'


def test_brarchive_build_archives_from_memory(tmp_path, monkeypatch):
    from anvil.lib import config
    from anvil.lib.lib import AnvilIO, Directory

    monkeypatch.chdir(tmp_path)
    (tmp_path / "assets").mkdir()
    (tmp_path / "assets/hit.ogg").write_bytes(b"ogg")
    with config.override(
        NAMESPACE="testns",
        PROJECT_NAME="proj",
        _LOCAL_EXPORT=True,
        _BRARCHIVE=True,
        _MINIFY=True,
        _ADD_STAMP=False,
    ) as cfg:
        rp = cfg.RP_PATH
        AnvilIO.file("thing.entity.json", {"e": 1}, rp / "entity", "w")
        AnvilIO.file("terrain_texture.json", {"t": 1}, rp / "textures", "w")
        AnvilIO.file("en_US.lang", "a=b", rp / "texts", "w")
        AnvilIO.file("manifest.json", {"m": 1}, rp, "w")
        Directory.copy_files(tmp_path / "assets", rp / "sounds/mob", "hit.ogg")

        # Stored files never reach the disk; loose ones do
        assert not (rp / "entity").exists()
        assert not (rp / "sounds").exists()
        assert (rp / "textures/terrain_texture.json").exists()
        assert (rp / "texts/en_US.lang").exists()
        assert (rp / "manifest.json").exists()

        BrArchivePacker.bake(rp)

    arc = rp / "__brarchive"
    assert BrArchive(arc / "entity.brarchive").read("thing.entity.json") == b'{"e":1}'
    assert _descriptors(arc / "sounds.brarchive") == []
    assert BrArchive(arc / "sounds/mob.brarchive").read("hit.ogg") == b"ogg"
    assert _descriptors(arc / "texts.brarchive") == [("en_US.lang", 0, 0)]
    assert BrArchive(arc / "textures.brarchive").read("terrain_texture.json") == b'{"t":1}'
