"""Short #10: words for the captions and the upload SRT. Writes work/words_cap.json and work/emph.txt. Then:
  python3 ../../tools/make_captions.py work/words_cap.json captions.js "$(cat work/emph.txt)"
  python3 ../../tools/srt_from_words.py work/words_cap.json short10-captions.srt && python3 prep_words.py --srt
Numbers: "seven in ten" shows as 7 IN 10 (make_captions turns number words into digits).
"""
import json, os, re, sys
os.makedirs('work', exist_ok=True)

if '--srt' in sys.argv:  # emphasis CAPS from the script back to normal case in the upload SRT; names stay
    s = open('short10-captions.srt').read()
    KEEP = {'AI', 'EU', 'UK', 'AI,'}
    s = re.sub(r"\b([A-Z]{2,}[A-Z']*)\b", lambda m: m.group(1) if m.group(1) in KEEP else m.group(1).capitalize() if m.group(1) in {'SEE'} else m.group(1).lower(), s)
    for a, b in (('chatgpt', 'ChatGPT'), ('openai', 'OpenAI'), ('claude', 'Claude'), ('anthropic', 'Anthropic'), (r'\beu\b', 'EU'), (r'\buk\b', 'UK'),
                 ('paris', 'Paris'), ('london', 'London'), ('spanish', 'Spanish'), ('romanian', 'Romanian'), ('europe', 'Europe')):
        s = re.sub(a, b, s, flags=re.I)
    s = s.replace('\nSee ', '\nSEE ').replace(' See ', ' see ')
    open('short10-captions.srt', 'w').write(s)
    print('srt case fixed'); sys.exit()

w = json.load(open('words.json'))
json.dump(w, open('work/words_cap.json', 'w'), indent=0)
t = lambda k: round(w[k]['start'], 2)
emph = [f'SEE@{t(13)}', f'LARGE@{t(24)}', f'BEGIN@{t(27)}', f'COIN@{t(35)}', f'LOADED@{t(48)}', f'ALL@{t(58)}', f'SIGNATURE@{t(64)}',
        f'IS@{t(80)}', f'EVERYWHERE@{t(111)}', f'TRANSLATED@{t(146)}', f'OWN@{t(149)}', f'PROOF@{t(165)}', f'CHEATED@{t(184)}',
        f'NO@{t(186)}', f'SAY@{t(201)}']
open('work/emph.txt', 'w').write(','.join(emph))
print('ok', len(w), 'words;', len(emph), 'emphasis')
