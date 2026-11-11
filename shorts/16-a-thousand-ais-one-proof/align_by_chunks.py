"""Align the take chunk by chunk (from #15's align_by_chunks.py, with numbers spoken out on both sides).

Usage: python3 align_by_chunks.py work/voice16k.wav work/script_plain.txt work/whisper_chunks.txt work/words_take.json
Whisper's chunk texts decide which script words fall in each chunk; tools/align.py then aligns each chunk and the
times are shifted back. Whisper writes numbers as digits, so both sides are turned into words before matching.
"""
import difflib, json, os, re, subprocess, sys, tempfile
wav16, script, chunks_txt, out = sys.argv[1:5]
ALIGN = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools', 'align.py')
ONES = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
TENS = 'x x twenty thirty forty fifty sixty seventy eighty ninety'.split()
def spell(n):
    n = int(n)
    if n < 20: return ONES[n]
    if n < 100: return TENS[n // 10] + ('' if n % 10 == 0 else ' ' + ONES[n % 10])
    if n < 1000: return ONES[n // 100] + ' hundred' + ('' if n % 100 == 0 else ' and ' + spell(n % 100))
    return spell(n // 100) + ' ' + spell(n % 100)          # years: 1637 -> sixteen thirty seven
def norm(t):
    t = t.lower().replace('5.2', ' five point two ').replace('-', ' ')
    t = re.sub(r'\d+', lambda m: ' ' + spell(m.group()) + ' ', t)
    return [re.sub(r"[^a-z']", '', x) for x in t.split() if re.sub(r"[^a-z']", '', x)]
disp = open(script).read().split()
chunks = []
for line in open(chunks_txt):
    m = re.match(r'\[\s*([\d.]+)-\s*([\d.]+)\]\s*(.*)', line)
    if m: chunks.append((float(m[1]), float(m[2]), norm(m[3])))
wt, wc = [], []
for i, (_, _, toks) in enumerate(chunks):
    wt += toks; wc += [i] * len(toks)
# one entry per spoken token, remembering which display word it came from
st, sd = [], []
for i, d in enumerate(disp):
    for tok in norm(d): st.append(tok); sd.append(i)
sm = difflib.SequenceMatcher(a=st, b=wt, autojunk=False)
owner_tok = [None] * len(st)
for a, b, n in sm.get_matching_blocks():
    for k in range(n): owner_tok[a + k] = wc[b + k]
owner = [None] * len(disp)
for k, o in enumerate(owner_tok):
    if o is not None and owner[sd[k]] is None: owner[sd[k]] = o
last = 0
for i in range(len(owner)):
    if owner[i] is None: owner[i] = last
    last = owner[i]
words, tmp = [], tempfile.mkdtemp()
for ci, (a, b, _) in enumerate(chunks):
    idx = [i for i, o in enumerate(owner) if o == ci]
    if not idx: continue
    pa, pb = max(0, a - 0.15), b + 0.15
    cw, ct, cj = f'{tmp}/c{ci}.wav', f'{tmp}/c{ci}.txt', f'{tmp}/c{ci}.json'
    open(ct, 'w').write(' '.join(disp[i] for i in idx))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(pa), '-to', str(pb), '-i', wav16, cw], check=True)
    r = subprocess.run(['python3', ALIGN, cw, ct, cj], capture_output=True, text=True)
    if r.returncode:
        print('chunk', ci, 'FAILED', r.stderr.strip().splitlines()[-1]); sys.exit(1)
    for x in json.load(open(cj)):
        x['start'] = round(x['start'] + pa, 3); x['end'] = round(x['end'] + pa, 3); words.append(x)
    print(f'chunk {ci}: {len(idx)} words, first "{disp[idx[0]]}", last "{disp[idx[-1]]}"', flush=True)
json.dump(words, open(out, 'w'), indent=0)
print(len(words), 'words of', len(disp))
