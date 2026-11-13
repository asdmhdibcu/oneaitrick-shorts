"""Short #18: tidy the English upload subtitles (numbers as digits) and write the translated ones on the same timings
(worldwide rule). Reads short18-captions.srt (tools/srt_from_words.py); rewrites it and writes
short18-captions.{es,pt,hi,id}.srt. No translation names heads or tails: TAILS is the hidden word.
Usage: python3 ../../tools/srt_from_words.py words.json short18-captions.srt && python3 make_srt_tr.py
"""
EN = "short18-captions.srt"
blocks = open(EN).read().strip().split("\n\n")
cues = [(b.split("\n")[0], b.split("\n")[1], " ".join(b.split("\n")[2:])) for b in blocks]
assert len(cues) == 29, len(cues)

FIX = [("eighty-six percent", "86%"), ("one in seven", "1 in 7")]

TR = {
 "es": ["Una moneda lanzada al aire guió a 50 expertos.", "Ninguno lo supo.", "Cada uno tenía un asistente de IA, como el tuyo.",
        "Y una moneda eligió en secreto sus respuestas favoritas.", "Imagina una balanza.", "Las dos opciones son válidas...",
        "y la IA deja caer una moneda en un lado.", "Los expertos eligieron el lado de la moneda el 86% de las veces.",
        "¿Al azar?", "Cerca de la mitad.", "Algunos ya habían decidido.", "Cuando la IA no estaba de acuerdo...",
        "cambiaron de opinión más de la mitad de las veces.", "Aquí viene lo raro.", "La mayoría repitió los argumentos de la IA...",
        "pero solo 1 de cada 7 le dio el crédito.", "¿La trampa?",
        "Anthropic probó su propia IA e hizo la moneda más pesada a propósito.", "La IA de todos los días puede empujar menos.",
        "Así que pregúntale una cosa más a tu IA.", "\"¿Cuál es el mejor argumento para la otra opción?\"",
        "Ahora hay una moneda en los dos lados.", "La decisión es tuya.",
        "Hay una palabra en este video que nunca dije en voz alta.", "¿La viste?", "Escríbela en los comentarios.",
        "Sígueme para más IA, explicada así.", "¿Crees que tú lo notarías?", "Porque..."],
 "pt": ["Uma moeda jogada para o alto guiou 50 especialistas.", "Nenhum deles sabia.", "Cada um tinha um assistente de IA, como o seu.",
        "E uma moeda escolheu em segredo as respostas favoritas dele.", "Imagine uma balança.", "As duas opções são boas...",
        "e a IA solta uma moeda em um dos lados.", "Os especialistas ficaram com o lado da moeda em 86% das vezes.",
        "Por acaso?", "Cerca da metade.", "Alguns já tinham decidido.", "Quando a IA discordou...",
        "eles mudaram de ideia em mais da metade das vezes.", "Agora vem a parte estranha.", "A maioria repetiu os argumentos da IA...",
        "mas só cerca de 1 em cada 7 deu o crédito a ela.", "O porém?",
        "A Anthropic testou a própria IA e deixou a moeda mais pesada de propósito.", "A IA do dia a dia pode empurrar menos.",
        "Então faça mais uma pergunta à sua IA.", "\"Qual é o melhor argumento para o outro lado?\"",
        "Agora há uma moeda nos dois lados.", "A escolha é sua.",
        "Tem uma palavra neste vídeo que eu nunca disse em voz alta.", "Viu qual é?", "Comente.",
        "Siga para mais IA, explicada assim.", "Acha que você perceberia?", "Porque..."],
 "hi": ["उछाले गए एक सिक्के ने 50 एक्सपर्ट्स के फ़ैसले मोड़ दिए।", "उनमें से एक को भी पता नहीं चला।",
        "हर एक के पास एक AI हेल्पर था, आपके जैसा।", "और एक सिक्के ने चुपके से उसके पसंदीदा जवाब चुन लिए।",
        "एक तराज़ू सोचिए।", "दोनों विकल्प ठीक हैं...", "और AI एक तरफ़ सिक्का गिरा देता है।",
        "एक्सपर्ट्स ने 86% बार सिक्के वाली तरफ़ को चुना।", "संयोग से?", "लगभग आधा।", "कुछ लोग पहले ही फ़ैसला कर चुके थे।",
        "जब AI उनसे असहमत हुआ...", "तो आधे से ज़्यादा बार उन्होंने अपना फ़ैसला बदल दिया।", "अब अजीब बात सुनिए।",
        "ज़्यादातर लोगों ने AI की दलीलें दोहराईं...", "लेकिन 7 में से सिर्फ़ लगभग 1 ने उसे श्रेय दिया।", "पेच क्या है?",
        "Anthropic ने अपने ही AI को टेस्ट किया, और सिक्के को जानबूझकर ज़्यादा भारी बनाया।", "रोज़ का AI शायद कम धक्का दे।",
        "तो अपने AI से एक और बात पूछिए।", "\"दूसरी तरफ़ के पक्ष में सबसे अच्छी दलील क्या है?\"",
        "अब दोनों तरफ़ एक-एक सिक्का है।", "फ़ैसला आपका है।", "इस वीडियो में एक शब्द है जो मैंने कभी ज़ोर से नहीं बोला।",
        "पकड़ा?", "कमेंट कीजिए।", "AI को ऐसे ही समझने के लिए फ़ॉलो कीजिए।", "क्या आप पहचान पाते?", "क्योंकि..."],
 "id": ["Lemparan koin mengarahkan 50 ahli.", "Tidak satu pun dari mereka tahu.", "Masing-masing punya asisten AI, seperti punyamu.",
        "Dan sebuah koin diam-diam memilih jawaban favoritnya.", "Bayangkan sebuah timbangan.", "Kedua pilihan sama-sama wajar...",
        "lalu AI menjatuhkan koin di satu sisi.", "Para ahli memilih sisi koin itu dalam 86% kasus.", "Kalau kebetulan?",
        "Sekitar setengah.", "Sebagian sudah memutuskan.", "Saat AI tidak setuju...", "mereka berubah pikiran, lebih dari separuh kali.",
        "Ini bagian anehnya.", "Kebanyakan mengulang argumen AI...", "tapi hanya sekitar 1 dari 7 yang menyebut peran AI.",
        "Masalahnya?", "Anthropic menguji AI miliknya sendiri, dan sengaja membuat koinnya ekstra berat.",
        "Dorongan AI sehari-hari mungkin lebih lemah.", "Jadi tanyakan satu hal lagi ke AI-mu.",
        "\"Apa argumen terbaik untuk sisi lainnya?\"", "Sekarang ada koin di kedua sisi.", "Pilihannya ada di tanganmu.",
        "Ada satu kata di video ini yang tidak pernah aku ucapkan.", "Sudah lihat?", "Tulis di komentar.",
        "Ikuti untuk AI lainnya, dijelaskan seperti ini.", "Yakin kamu bakal sadar?", "Karena..."],
}

out = []
for n, tc, txt in cues:
    for a, b in FIX:
        txt = txt.replace(a, b)
    out.append((n, tc, txt))
open(EN, "w").write("\n\n".join(f"{n}\n{tc}\n{txt}" for n, tc, txt in out) + "\n")
for lang, lines in TR.items():
    assert len(lines) == len(cues), (lang, len(lines))
    open(f"short18-captions.{lang}.srt", "w").write("\n\n".join(f"{n}\n{tc}\n{t}" for (n, tc, _), t in zip(cues, lines)) + "\n")
print("wrote", EN, "and", ", ".join(TR))
