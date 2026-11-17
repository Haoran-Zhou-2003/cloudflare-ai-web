import urllib.request,urllib.error,json,time,sys,re
base='http://localhost:38479'
for attempt in range(40):
 try:
  with urllib.request.urlopen(base+'/api/config',timeout=3) as r:
   config=json.load(r)
  break
 except Exception:
  time.sleep(0.5)
else:
 print('Local worker did not become ready');sys.exit(1)
assert isinstance(config.get('needCode'),bool),config
assert not any(k in config for k in ['apiKey','code','codes','googleApiKey']),config
assert config['defaultModel']=='gemma-4-31b-it@google',config
assert '+gemma-4-31b-it@Google' in config['customModels'],config
assert '+gemma-4-26b-a4b-it@Google' in config['customModels'],config
print('PASS /api/config selects Google Gemma and exposes no credentials')
with urllib.request.urlopen(base+'/',timeout=20) as r:
 html=r.read().decode()
assert '<title>NextChat</title>' in html
assert '/_next/static/' in html
print('PASS / returns NextChat HTML and compiled assets')
asset=re.search(r'(?:src|href)="(/_next/static/[^\"]+)"',html).group(1)
with urllib.request.urlopen(base+asset,timeout=20) as r:
 assert r.status==200
 assert 'immutable' in r.headers.get('Cache-Control','')
print('PASS static asset is served with immutable cache headers')
for path,headers,expected in [
 ('/api/unsupported/test', {'x-base-url':'http://example.com'},400),
 ('/api/upstash/notallowed/key?endpoint=https://example.com',{},403),
 ('/api/webdav/backup.json?endpoint=https://example.com',{},400),
]:
 try:
  with urllib.request.urlopen(urllib.request.Request(base+path,headers=headers),timeout=20) as r:
   status=r.status
 except urllib.error.HTTPError as e:
  status=e.code
 assert status==expected,(path,status,expected)
 print('PASS route',path.split('?')[0],status)
print('All local Workers smoke checks passed')
