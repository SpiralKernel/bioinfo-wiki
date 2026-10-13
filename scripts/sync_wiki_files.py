#!/usr/bin/env python3
"""Synchronize generated pages, preserving unmanaged files and remote edits."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

MANIFEST = '.wiki-export.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_manifest(directory):
    path = directory / MANIFEST
    if path.is_symlink():
        raise ValueError('拒绝使用符号链接清单')
    data = json.loads(path.read_text())
    names = data.get('generated_files', [])
    hashes = data.get('file_hashes', {})
    if (data.get('schema') != 1 or not isinstance(names, list) or not names or
            len(names) != len(set(names)) or not isinstance(hashes, dict) or set(names) != set(hashes)):
        raise ValueError('导出清单缺失或不完整，请重新导出')
    for name in names:
        if not isinstance(name, str) or Path(name).name != name or not name.endswith('.md') or name.startswith('.'):
            raise ValueError('导出清单包含不安全的文件名')
        if not isinstance(hashes[name], str) or len(hashes[name]) != 64:
            raise ValueError('导出清单包含无效校验值')
    return data


def sync(source, destination, legacy_hashes=None, check=False):
    source, destination = source.resolve(), destination.resolve()
    if source == destination or source in destination.parents or destination in source.parents:
        raise ValueError('导出目录与Wiki目录必须独立且不能互相包含')
    incoming = load_manifest(source)
    names = set(incoming['generated_files'])
    for name in names:
        path = source/name
        if path.is_symlink() or not path.is_file() or digest(path) != incoming['file_hashes'][name]:
            raise ValueError(f'发布文件与清单不符，请重新导出：{name}')
    old = load_manifest(destination) if (destination/MANIFEST).exists() or (destination/MANIFEST).is_symlink() else None
    managed = set(old['generated_files']) if old else set()
    legacy = legacy_hashes or {}
    # Validate every collision and deletion before touching any destination file.
    for name in names | managed:
        path = destination/name
        if path.is_symlink():
            raise ValueError(f'目标页面为符号链接，已停止：{name}')
        if name in managed:
            if not path.is_file() or digest(path) != old['file_hashes'][name]:
                raise ValueError(f'Wiki页面有导出后修改，请先合并回Obsidian原稿：{name}')
        elif path.exists():
            if not path.is_file():
                raise ValueError(f'目标不是普通文件：{name}')
            actual = digest(path)
            allowed = {incoming['file_hashes'][name]}
            if not old and name in legacy:
                allowed.add(legacy[name])
            if actual not in allowed:
                raise ValueError(f'同名页面不属于当前导出，或曾被修改，请先核对：{name}')
    removed = sorted(managed - names)
    if not check:
        destination.mkdir(parents=True, exist_ok=True)
        for name in sorted(names):
            shutil.copy2(source/name, destination/name)
        for name in removed:
            (destination/name).unlink()
        shutil.copy2(source/MANIFEST, destination/MANIFEST)
    print(f'{"检查通过" if check else "已同步"}：{len(names)} 个受管理页面；删除 {len(removed)} 个旧页面。')
    return removed


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--destination', type=Path, required=True)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        legacy_path = Path(__file__).with_name('legacy-wiki-files.json')
        legacy = json.loads(legacy_path.read_text()) if legacy_path.exists() else {}
        sync(args.source, args.destination, legacy, args.check)
    except (ValueError, OSError) as error:
        parser.exit(1, f'同步失败：{error}\n')
