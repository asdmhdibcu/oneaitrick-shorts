"""Short #6: merge spoken numbers into digits for the captions and the upload SRT.
Writes work/words_cap.json. Then:
  python3 ../../tools/make_captions.py work/words_cap.json captions.js 'NOBODY@5.9,DNA@11.85,ODD,HUGE,CRISPR@42.49,NOBEL,RNA,YET@56.97,ASTONISHING,ONE@70.0,AI@73.96,EUREKA,SLEEPS'
  python3 ../../tools/srt_from_words.py work/words_cap.json short06-captions.srt   (then fix ALL-CAPS words by hand)
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

merge('Nine', 0.0, 4, '950')
merge('twenty-one', 2.57, 1, '21')
merge('nine', 19.25, 4, '950')
merge('two', 23.34, 3, '200,000')
merge('three', 26.66, 4, '3,500')
merge('twenty', 29.07, 1, '20')
json.dump(w, open('work/words_cap.json', 'w'), indent=0)
print('ok', len(w), 'words')
