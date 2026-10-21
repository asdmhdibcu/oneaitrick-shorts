"""Short #5: merge spoken numbers into digits for the karaoke captions and the upload SRT.
Writes work/words_cap.json. Then:
  python3 ../../tools/make_captions.py work/words_cap.json captions.js 'ACED@1.04,FRIDGE,10,SMASHED,80%,REAL@32.46,17,ZERO,90%,HOUR,SURE,COMPETENT,PRACTICAL,RUNNING@72.3'
  python3 ../../tools/srt_from_words.py work/words_cap.json short05-captions.srt
  (then fix two cues by hand: 'gpt-6' -> 'GPT-6', 'zero out of 11.' -> 'Zero out of 11.')
"""
import json, os
os.makedirs('work', exist_ok=True)
w = json.load(open('words.json'))

def find(text, near):
    for i, x in enumerate(w):
        if x['text'].strip('.,…?!:').lower() == text.lower() and abs(x['start'] - near) < 0.4:
            return i
    raise SystemExit(f'missing {text}@{near}')

def merge(first, near, count, disp):
    i = find(first, near); seg = w[i:i + count]; last = seg[-1]['text']
    tail = last[-1] if last[-1] in '.,…:?' else ''
    w[i:i + count] = [{'text': disp + tail, 'start': seg[0]['start'], 'end': seg[-1]['end']}]

merge('eighty', 28.74, 2, '80%')
merge('NINETY', 46.76, 2, '90%')
merge('Seventeen', 40.43, 1, '17')
merge('eighteen', 41.30, 1, '18')
merge('eleven', 44.21, 1, '11')
json.dump(w, open('work/words_cap.json', 'w'), indent=0)
print('ok', len(w), 'words')
