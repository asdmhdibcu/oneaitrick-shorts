"""Derive caption/SRT word lists from words.json: spoken numbers merged into digits.
Writes work/words_cap.json (on-screen karaoke) and work/words_srt.json (upload SRT)."""
import json, os
os.makedirs('work', exist_ok=True)

def load():
    return json.load(open('words.json'))

def find(w, text, near):
    for i, x in enumerate(w):
        if x['text'].strip('.,…?!:').lower() == text.lower() and abs(x['start'] - near) < 0.4:
            return i
    raise SystemExit(f'missing {text}@{near}')

def merge(w, first, near, count, disp):
    i = find(w, first, near); seg = w[i:i + count]; last = seg[-1]['text']
    tail = last[-1] if last[-1] in '.,…:?' else ''
    w[i:i + count] = [{'text': disp + tail, 'start': seg[0]['start'], 'end': seg[-1]['end']}]

def common(w):
    merge(w, 'a', 18.52, 4, '£120'); merge(w, 'four', 22.74, 5, '4,500'); merge(w, 'seven', 48.15, 4, '780')
    merge(w, 'one', 53.10, 4, '1.5'); merge(w, 'One', 63.47, 3, '1.8')

w = load(); common(w)
i = find(w, 'four-point-two-trillion-dollar', 65.35); x = w[i]; a, b = x['start'], x['end']; d = b - a
w[i:i + 1] = [{'text': '$4.2', 'start': a, 'end': round(a + d * 3 / 7, 3)}, {'text': 'TRILLION', 'start': round(a + d * 3 / 7, 3), 'end': round(a + d * 5 / 7, 3)},
              {'text': 'DOLLAR', 'start': round(a + d * 5 / 7, 3), 'end': b}]
json.dump(w, open('work/words_cap.json', 'w'), indent=0)
w = load(); common(w); merge(w, 'four-point-two-trillion-dollar', 65.35, 1, '$4.2-trillion')
json.dump(w, open('work/words_srt.json', 'w'))
print('ok')
# then:
#   python3 ../../tools/make_captions.py work/words_cap.json captions.js 'AI@2.86,1845,RAILWAY@6.17,EVERYTHING,DARWIN,£120,TWICE,CRASHED,20@36.69,TRACKS,RICHER,780,BILLION,1.5,TRILLION@53.92,6,TRILLION@60.04,1.8,$4.2,GAP,BUBBLE,SMARTPHONE,CLOUD'
#   (and mark the "4,500" word as emphasised in captions.js; commas can't be passed in the list)
#   python3 ../../tools/srt_from_words.py work/words_srt.json short04-captions.srt
