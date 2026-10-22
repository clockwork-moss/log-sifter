import io,unittest
from log_sifter import parse_line,records
class LogTests(unittest.TestCase):
    def test_underscore(self): self.assertEqual(parse_line('2026-01-01T00:00:00Z ERROR user=batch_worker failed')['user'],'batch_worker')
    def test_bad_date(self): self.assertIsNone(parse_line('bad INFO hello'))
    def test_bad_line(self): self.assertIsNone(parse_line('continuation'))
    def test_filter_stats(self):
        stats={};text='2026-01-01 INFO good\n2026-01-01 ERROR FAILED\nnope\n'
        rows=list(records(io.StringIO(text),['ERROR'],'failed',stats))
        self.assertEqual(len(rows),1);self.assertEqual(stats,{'INFO':1,'ERROR':1,'unparsed':1})
    def test_lazy(self):
        def source():
            yield '2026-01-01 INFO first'
            raise AssertionError('read ahead')
        self.assertEqual(next(records(source()))['message'],'first')
