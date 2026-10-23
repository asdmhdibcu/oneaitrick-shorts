"""Short #9: merge spoken numbers into digits for the captions and the upload SRT.
Writes work/words_cap.json and work/emph.txt. Then:
  python3 ../../tools/make_captions.py work/words_cap.json captions.js "$(cat work/emph.txt)"
  python3 ../../tools/srt_from_words.py work/words_cap.json short09-captions.srt   (prep_words.py --srt fixes the case after)
"""
import json, os, re, sys
os.makedirs('work', exist_ok=True)

if '--srt' in sys.argv:  # emphasis CAPS from the script back to normal case in the upload SRT; names stay
    KEEP = {'AI', 'ARTEX', 'AI,'}
    s = open('short09-captions.srt').read()
    s = re.sub(r"\b([A-Z]{2,}[A-Z']*)\b", lambda m: m.group(1) if m.group(1) in KEEP else m.group(1).lower(), s)
    s = re.sub(r'\bartex\b', 'ARTEX', s, flags=re.I)  # the tool lowercases all-caps words; the name stays
    open('short09-captions.srt', 'w').write(s)
    print('srt case fixed'); sys.exit()

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


merge('two', 2.35, 4, '2,200')
merge('fourteen', 26.17, 1, '14')
merge('two', 32.46, 4, '2,900')
json.dump(w, open('work/words_cap.json', 'w'), indent=0)
open('work/emph.txt', 'w').write('3@6.86,ROBOT@17.86,EVERY@19.39,MINUTE,ONE@36.27,DID,KEY@43.2,CONNECTWISE,STOLE,TRUSTED,BOSS,ARTEX,'
                                  'GOOD,OWN,FIRST,ELSE')
print('ok', len(w), 'words')
