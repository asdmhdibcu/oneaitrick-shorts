# Usage: python3 align_by_chunks.py work/voice16k.wav work/script_plain.txt work/whisper_chunks.txt work/words_take.json
# Align a long take chunk by chunk: whisper chunk texts decide which script words go in each chunk,
# then tools/align.py runs per chunk and the times are offset back.
import sys, re, json, subprocess, difflib, os, tempfile
wav16, script, chunks_txt, out = sys.argv[1:5]
ALIGN = '/root/oneaitrick-shorts/tools/align.py'
disp = open(script).read().split()
def norm(t):
    t = t.lower().replace('$200', 'two hundred dollars').replace('100', 'a hundred').replace('2030', '2030')
    t = re.sub(r'\b1\b', 'one', t); t = re.sub(r'\b0\b', 'zero', t)
    return [re.sub(r"[^a-z0-9']", '', x) for x in t.split() if re.sub(r"[^a-z0-9']", '', x)]
chunks = []
for line in open(chunks_txt):
    m = re.match(r'\[\s*([\d.]+)-\s*([\d.]+)\]\s*(.*)', line)
    if m: chunks.append((float(m[1]), float(m[2]), norm(m[3])))
# label whisper tokens with chunk index, then match script tokens to them
wt, wc = [], []
for i, (_, _, toks) in enumerate(chunks):
    wt += toks; wc += [i] * len(toks)
st = [norm(x)[0] if norm(x) else '' for x in disp]
sm = difflib.SequenceMatcher(a=st, b=wt, autojunk=False)
owner = [None] * len(st)
for a, b, n in sm.get_matching_blocks():
    for k in range(n): owner[a + k] = wc[b + k]
# fill gaps with the previous owner
last = 0
for i in range(len(owner)):
    if owner[i] is None: owner[i] = last
    last = owner[i]
words = []
tmp = tempfile.mkdtemp()
for ci, (a, b, _) in enumerate(chunks):
    idx = [i for i, o in enumerate(owner) if o == ci]
    if not idx: continue
    txt = ' '.join(disp[i] for i in idx)
    # pad the audio window a little either side
    pa, pb = max(0, a - 0.15), b + 0.15
    cw, ct, cj = f'{tmp}/c{ci}.wav', f'{tmp}/c{ci}.txt', f'{tmp}/c{ci}.json'
    open(ct, 'w').write(txt)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(pa), '-to', str(pb), '-i', wav16, cw], check=True)
    r = subprocess.run(['python3', ALIGN, cw, ct, cj], capture_output=True, text=True)
    if r.returncode:
        print('chunk', ci, 'FAILED', r.stderr.strip().splitlines()[-1]); sys.exit(1)
    for x in json.load(open(cj)):
        x['start'] = round(x['start'] + pa, 3); x['end'] = round(x['end'] + pa, 3); words.append(x)
    print(f'chunk {ci}: {len(idx)} words ok', flush=True)
json.dump(words, open(out, 'w'), indent=0)
print(len(words), 'words of', len(disp))
