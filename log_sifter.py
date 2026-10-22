"""Streaming ISO timestamp and severity log reader."""
import argparse,csv,json,re,sys
from datetime import datetime
PATTERN=re.compile(r'^(\S+)\s+(DEBUG|INFO|WARNING|ERROR|CRITICAL)\s+(.*)$')
USER=re.compile(r'\buser=([A-Za-z0-9_-]+)\b')
def parse_line(line):
    match=PATTERN.match(line.strip())
    if not match: return None
    stamp,level,message=match.groups()
    try: stamp=datetime.fromisoformat(stamp.replace('Z','+00:00')).isoformat()
    except ValueError: return None
    user=USER.search(message)
    return {'timestamp':stamp,'severity':level,'user':user.group(1) if user else '', 'message':message}
def records(stream, severity=None, keyword=None, stats=None):
    stats = stats if stats is not None else {}
    for line in stream:
        row=parse_line(line)
        if row is None: stats['unparsed']=stats.get('unparsed',0)+1;continue
        stats[row['severity']]=stats.get(row['severity'],0)+1
        if severity and row['severity'] not in severity: continue
        if keyword and keyword.casefold() not in row['message'].casefold(): continue
        yield row
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('file');p.add_argument('--severity',action='append',choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL']);p.add_argument('--keyword');p.add_argument('--format',choices=['text','json','csv'],default='text');p.add_argument('--stats',action='store_true')
    a=p.parse_args();stats={}
    try:
        with open(a.file,encoding='utf-8',errors='replace') as stream:
            rows=records(stream,a.severity,a.keyword,stats)
            if a.format=='csv':
                writer=csv.DictWriter(sys.stdout,fieldnames=['timestamp','severity','user','message']);writer.writeheader()
                for row in rows: writer.writerow(row)
            elif a.format=='json':
                print('[',end='');sep=''
                for row in rows: print(sep+json.dumps(row),end='');sep=','
                print(']')
            else:
                for row in rows: print(f"{row['timestamp']} {row['severity']} {row['message']}")
        if a.stats: print(json.dumps(stats,sort_keys=True),file=sys.stderr)
    except OSError as e: p.error(str(e))
if __name__=='__main__': main()
