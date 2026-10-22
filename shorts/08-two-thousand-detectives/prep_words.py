"""Short #8: merge spoken numbers into digits for the captions and the upload SRT.
Writes work/words_cap.json and work/emph.txt. Then:
  python3 ../../tools/make_captions.py work/words_cap.json captions.js "$(cat work/emph.txt)"
  python3 ../../tools/srt_from_words.py work/words_cap.json short08-captions.srt   (then fix ALL-CAPS words by hand)
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


def say(first, near, disp):
    i = find(first, near); last = w[i]['text']
    tail = last[-1] if last[-1] in '.,…:?' else ''
    w[i]['text'] = disp + tail


merge('Two', 0.0, 2, '2,000')
merge('seven-point-seven', 2.39, 2, '7,700,000')
merge('thirty-two', 5.3, 2, '32:00')
say('Seven-point-seven', 11.28, '7.7')
merge('two', 22.11, 2, '2,000')
say('eleven', 51.6, '11')
merge('SEVEN', 53.92, 2, '7,000')
say('D-C-T-N-1', 68.91, 'DCTN1')
say('D-C-T-N-1', 86.36, 'DCTN1')
merge('Two', 113.14, 2, '2,000')
merge('Thirty-two', 114.89, 2, '32:00')
json.dump(w, open('work/words_cap.json', 'w'), indent=0)
open('work/emph.txt', 'w').write('CLUE@8.09,ONE@17.87,CRISPR,MOUNTAIN,DETECTIVES@38.12,GPT-ROSALIND,CLUE.@67.21,CLUE@67.21,DCTN1@68.91,LORRIES,ON@28.42,ON@76.36,BREAD,MORE@85.28,'
                                  'PERRY,WRONG,LEAD,CURE,MICE,SINGLE,CLUE@116.32')
print('ok', len(w), 'words')
