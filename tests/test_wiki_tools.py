import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from urllib.parse import unquote
import re

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT/'scripts'/f'{name}.py')
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


exporter = module('export_wiki')
synchronizer = module('sync_wiki_files')


class WikiToolsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root/'notes'
        self.output = self.root/'output'
        self.destination = self.root/'destination'
        (self.source/'术语与概念').mkdir(parents=True)

    def tearDown(self):
        self.temp.cleanup()

    def note(self, title, body='正文。', aliases=None):
        path = self.source/'术语与概念'/f'{title}.md'
        path.write_text('---\nstatus: 可用\nsummary: "一句话。"\nupdated: "2026-10-13"\n'
                        'validation: "测试样例"\naliases: '+json.dumps(aliases or [])+
                        '\n---\n\n# '+title+'\n\n'+body+'\n')
        return path

    def test_aliases_tables_code_and_navigation(self):
        self.note('概念甲', aliases=['A'])
        self.note('概念乙', '| [[A\\|甲]] |\n`[[不是链接]]`\n````text\n[[也不是链接]]\n```\n````')
        result = exporter.export(self.source, self.output)
        page = (self.output/'概念乙.md').read_text()
        self.assertIn('[甲]('+exporter.page_url('概念甲')+')', page)
        self.assertIn('`[[不是链接]]`', page)
        self.assertIn('[[也不是链接]]', page)
        self.assertEqual(len(result['pages']), 2)
        filenames = {p.stem for p in self.output.glob('*.md')}
        for path in self.output.glob('*.md'):
            for target in re.findall(re.escape(exporter.WIKI_URL)+r'/([^\s)]+)', path.read_text()):
                self.assertIn(unquote(target), filenames)

    def test_block_aliases_and_source_remains_unchanged(self):
        path = self.note('概念甲')
        path.write_text(path.read_text().replace('aliases: []', 'aliases:\n  - "甲"\n  - "A"'))
        before = path.read_bytes()
        result = exporter.export(self.source, self.output, refresh_index=True)
        self.assertEqual(result['pages'][0]['aliases'], ['甲', 'A'])
        self.assertEqual(before, path.read_bytes())
        self.assertTrue((self.source/'学习路线/关键词索引.md').is_file())

    def test_bad_link_and_duplicate_stop_before_output_changes(self):
        self.note('甲')
        exporter.export(self.source, self.output)
        before = {p.name:p.read_bytes() for p in self.output.iterdir()}
        path = self.note('乙', '[[不存在]]')
        with self.assertRaisesRegex(ValueError, '内部链接'):
            exporter.export(self.source, self.output)
        self.assertEqual(before, {p.name:p.read_bytes() for p in self.output.iterdir()})
        path.unlink()
        (self.source/'工具').mkdir()
        (self.source/'工具/甲.md').write_text((self.source/'术语与概念/甲.md').read_text())
        with self.assertRaisesRegex(ValueError, '重复'):
            exporter.export(self.source, self.output)

    def test_sync_rename_preserves_unmanaged_and_rejects_manual_edit(self):
        path = self.note('旧名')
        exporter.export(self.source, self.output)
        synchronizer.sync(self.output, self.destination)
        (self.destination/'人工页面.md').write_text('不受导出管理')
        (self.output/'private.txt').write_text('不应复制')
        path.unlink()
        self.note('新名')
        exporter.export(self.source, self.output)
        synchronizer.sync(self.output, self.destination)
        self.assertFalse((self.destination/'旧名.md').exists())
        self.assertTrue((self.destination/'新名.md').exists())
        self.assertTrue((self.destination/'人工页面.md').exists())
        self.assertFalse((self.destination/'private.txt').exists())
        (self.destination/'新名.md').write_text('网页上的新修改')
        before = {p.name:p.read_bytes() for p in self.destination.iterdir()}
        with self.assertRaisesRegex(ValueError, '修改'):
            synchronizer.sync(self.output, self.destination)
        self.assertEqual(before, {p.name:p.read_bytes() for p in self.destination.iterdir()})

    def test_hash_tampering_and_unmanaged_collision(self):
        self.note('甲')
        exporter.export(self.source, self.output)
        self.destination.mkdir()
        (self.destination/'甲.md').write_text('已有人工页面')
        with self.assertRaisesRegex(ValueError, '同名页面'):
            synchronizer.sync(self.output, self.destination)
        (self.destination/'甲.md').unlink()
        (self.output/'甲.md').write_text('导出后修改')
        with self.assertRaisesRegex(ValueError, '清单不符'):
            synchronizer.sync(self.output, self.destination)

    def test_drafts_are_not_published_and_cannot_be_linked(self):
        self.note('已完成')
        path = self.note('草稿', '未完成内容')
        path.write_text(path.read_text().replace('status: 可用', 'status: 草稿'))
        result = exporter.export(self.source, self.output)
        self.assertEqual([r['title'] for r in result['pages']], ['已完成'])
        self.assertFalse((self.output/'草稿.md').exists())
        self.note('已完成', '[[草稿]]')
        with self.assertRaisesRegex(ValueError, '内部链接'):
            exporter.export(self.source, self.output)

    def test_legacy_upgrade_requires_matching_previous_content(self):
        self.note('甲')
        exporter.export(self.source, self.output)
        self.destination.mkdir()
        old = b'previous generated content'
        (self.destination/'甲.md').write_bytes(old)
        synchronizer.sync(self.output, self.destination, {'甲.md': hashlib.sha256(old).hexdigest()})
        self.assertEqual((self.destination/'甲.md').read_bytes(), (self.output/'甲.md').read_bytes())


if __name__ == '__main__':
    unittest.main()
