"""Short #7: merge spoken numbers into digits for the captions and the upload SRT.
Writes work/words_cap.json. Then:
  python3 ../../tools/make_captions.py work/words_cap.json captions.js "$(cat work/emph.txt)"
  python3 ../../tools/srt_from_words.py work/words_cap.json short07-captions.srt   (then fix ALL-CAPS words by hand)
"""
import json, os
os.makedirs('work', exist_ok=True)
w = json.load(open('words.json'))

def find(text, near):
    for i, x in enumerate(w):
        if x['text'].strip('.,…?!:"').lower() == text.lower() and abs(x['start'] - near) < 0.4:
            return i
    raise SystemExit(f'missing {text}@{near}')

def merge(first, near, count, disp):
    i = find(first, near); seg = w[i:i + count]; last = seg[-1]['text']
    tail = last[-1] if last[-1] in '.,…:?' else ''
    w[i:i + count] = [{'text': disp + tail, 'start': seg[0]['start'], 'end': seg[-1]['end']}]

merge('MILLION-dollar', 1.34, 1, '$1,000,000')
merge('eighty-eight', 3.47, 1, '88')
merge('MILLION', 33.39, 2, '$1,000,000')
merge('ten', 36.88, 2, '10,000')
merge('Eighty-eight', 39.48, 1, '88')
json.dump(w, open('work/words_cap.json', 'w'), indent=0)
open('work/emph.txt', 'w').write('NOBODY,RULEBOOK@8.83,BREAK@23.64,INFINITELY,YES@41.1,BREAK@42.4,INFINITY,EXPLODE,NO,MOLECULES,MATHS@58.36,CATCH,PUSH,REAL@71.73,LEAN,YES@83.91,RIGHT@90.82,OWN,HEROES,MORE@106.41,TOO,SLOWLY,CAREFULLY,MAYBE,CENTURY')
print('ok', len(w), 'words')
