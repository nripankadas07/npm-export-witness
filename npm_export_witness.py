"""Offline bounded npm-export-witness analyzer. No operational writes."""

import re
MISSING=object()

def safe_path(s,pattern=False):
    if not isinstance(s,str) or not s.startswith('./') or any(c in s for c in '\\%?#') or (s.count('*')>1 if pattern else '*' in s): raise ValueError('unsupported export path')
    if any(x in ('.','..','node_modules','') for x in s[2:].split('/')): raise ValueError('unsafe or unsupported path segment')
    return s

def validate(node,depth=0):
    if depth>16: raise ValueError('exports nested beyond 16')
    if node is None:return
    if isinstance(node,str):safe_path(node,True);return
    if not isinstance(node,dict) or len(node)>256:raise ValueError('only string, null and condition objects supported; arrays unsupported')
    for key,value in node.items():
        if not isinstance(key,str) or not key or key.startswith('.') or key.isdecimal():raise ValueError('invalid conditional key')
        validate(value,depth+1)

def select(node,conditions,capture,trace,depth=0):
    if node is None:return {'status':'blocked','target':None,'trace':trace}
    if isinstance(node,str):
        target=node.replace('*',capture) if capture is not None else node
        safe_path(target)
        return {'status':'resolved','target':target,'trace':trace}
    for condition,value in node.items():
        if condition=='default' or condition in conditions:
            result=select(value,conditions,capture,trace+[condition],depth+1)
            if result is not MISSING:return result
    return MISSING

def analyze(d):
    if not isinstance(d,dict) or set(d)!={'exports','queries'}:raise ValueError('expected exports and queries')
    exports=d['exports']; submap=isinstance(exports,dict) and any(k.startswith('.') for k in exports)
    if submap:
        if len(exports)>256:raise ValueError('at most 256 export entries')
        for k,v in exports.items():
            if k!='.':safe_path(k,True)
            validate(v)
    else:validate(exports);exports={'.':exports}
    queries=d['queries']
    if not isinstance(queries,list) or len(queries)>256:raise ValueError('at most 256 queries')
    result=[]
    for query in queries:
        if not isinstance(query,dict) or set(query)!={'subpath','conditions'}:raise ValueError('expected subpath and conditions')
        sub=query['subpath'];cond=query['conditions']
        if sub!='.':safe_path(sub)
        if not isinstance(cond,list) or len(cond)>32 or any(not isinstance(x,str) or not x or x.isdecimal() or x.startswith('.') for x in cond):raise ValueError('invalid conditions')
        if 'import' in cond and 'require' in cond:raise ValueError('import and require are mutually exclusive')
        key=None;capture=None
        if sub in exports:key=sub
        else:
            candidates=[]
            for k in exports:
                if '*' not in k:continue
                prefix,suffix=k.split('*')
                if sub.startswith(prefix) and sub.endswith(suffix) and len(sub)>=len(prefix)+len(suffix):
                    candidates.append((len(prefix),len(k),k,sub[len(prefix):len(sub)-len(suffix) if suffix else None]))
            if candidates:_,_,key,capture=max(candidates)
        selected=select(exports[key],set(cond),capture,[]) if key is not None else MISSING
        if selected is MISSING:selected={'status':'not_exported','target':None,'trace':[]}
        result.append({'subpath':sub,'conditions':cond,'matched_key':key,**selected})
    return {'queries':result,'filesystem_checked':False}

def _pairs(pairs):
    result={}
    for key,val in pairs:
        if key in result:raise ValueError('duplicate JSON key: '+key)
        result[key]=val
    return result

def main():
    import argparse,json,sys
    from pathlib import Path
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',help='JSON input path; - for stdin')
    args=parser.parse_args()
    try:
        raw=sys.stdin.buffer.read(1048577) if args.input=='-' else Path(args.input).open('rb').read(1048577)
        if len(raw)>1048576:raise ValueError('input exceeds 1 MiB')
        data=json.loads(raw,object_pairs_hook=_pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite JSON number')))
        print(json.dumps(analyze(data),ensure_ascii=True,indent=2));return 0
    except (ValueError,TypeError,KeyError,OverflowError,RecursionError,OSError) as exc:
        print(json.dumps({'error':str(exc)}),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
