"""Short #17: tidy the English upload subtitles (numbers as digits) and write the translated ones on the same timings
(worldwide rule). Reads short17-captions.srt (tools/srt_from_words.py); rewrites it and writes
short17-captions.{es,pt,hi,id}.srt.
Usage: python3 ../../tools/srt_from_words.py words.json short17-captions.srt && python3 make_srt_tr.py
"""
EN = "short17-captions.srt"
blocks = open(EN).read().strip().split("\n\n")
cues = [(b.split("\n")[0], b.split("\n")[1], " ".join(b.split("\n")[2:])) for b in blocks]
assert len(cues) == 43, len(cues)

FIX = [("Nearly one in 3", "Nearly 1 in 3"), ("money. now.", "money. NOW."), ("thirty seconds", "30 seconds"),
       ("over seven times in two years", "over 7 times in 2 years"), ("about ten dollars", "about $10"),
       ("add two locks", "add 2 locks")]

TR = {
 "es": ["Casi 1 de cada 3 personas dice que una voz falsa la llamó.", "Imagínalo.", "Suena tu teléfono.", "Dice \"Mamá\".",
        "Está llorando.", "Necesita dinero. YA.", "Su voz funciona como una llave.", "La oyes...", "y la puerta se abre.",
        "¿Copiar una llave?", "Solo necesitas verla bien.", "La app que uso para esta voz dice que 30 segundos pueden bastar.",
        "Una nota de voz.", "Sí.", "Esta voz es una copia de la mía.", "Y ahora las máquinas que copian llaves están a la venta.",
        "Una empresa de seguridad vigiló grupos de chat de criminales.",
        "El comercio de clonación de voz creció más de 7 veces en 2 años.", "¿Cuentas robadas de apps reales de clonación?",
        "Desde unos 10 dólares.", "¿El giro?", "De lo que más hablan estos criminales... no es de mamá.", "Es tu BANCO.",
        "Una línea falsa del banco llama y pide tu código.", "Ese código es tu segunda cerradura.", "Si lo dices en voz alta, entran.",
        "¿La trampa?", "Estas cifras vienen de empresas que venden protección.",
        "Cuentan publicaciones y respuestas de encuestas, no dinero robado.", "Así que pon 2 cerraduras que ninguna copia pueda abrir.",
        "Una.", "Una palabra secreta familiar, acordada cara a cara.", "Dos.", "Tu código nunca sale de tu teléfono.",
        "Un banco de verdad no te lo pedirá.", "Cuelga y llama a un número que conozcas.", "Ahora suena tu teléfono.", "\"Mamá\".",
        "Le pides la palabra.", "Hay una palabra en este video que nunca dije en voz alta.", "¿La viste?", "Escríbela en los comentarios.",
        "Sígueme para más IA, explicada así."],
 "pt": ["Quase 1 em cada 3 pessoas diz que uma voz falsa ligou para elas.", "Imagine.", "Seu celular toca.", "Aparece \"Mãe\".",
        "Ela está chorando.", "Precisa de dinheiro. JÁ.", "A voz dela funciona como uma chave.", "Você ouve...", "e a porta se abre.",
        "Copiar uma chave?", "Basta olhar bem para ela.", "O app que uso para esta voz diz que 30 segundos podem bastar.",
        "Uma mensagem de voz.", "Sim.", "Esta voz é uma cópia da minha.", "E agora as máquinas de copiar chaves estão à venda.",
        "Uma empresa de segurança vigiou grupos de chat de criminosos.",
        "O comércio de clonagem de voz cresceu mais de 7 vezes em 2 anos.", "Contas roubadas de apps reais de clonagem?",
        "A partir de uns 10 dólares.", "A reviravolta?", "O assunto preferido desses criminosos... não é a mãe.", "É o seu BANCO.",
        "Uma linha falsa do banco liga e pede o seu código.", "Esse código é a sua segunda fechadura.", "Leia em voz alta e eles entram.",
        "O porém?", "Esses números vêm de empresas que vendem proteção.",
        "Eles contam postagens e respostas de pesquisa, não dinheiro roubado.", "Então coloque 2 fechaduras que nenhuma cópia abre.",
        "Uma.", "Uma palavra secreta da família, combinada pessoalmente.", "Duas.", "Seu código nunca sai do seu celular.",
        "Um banco de verdade não pede.", "Desligue e ligue para um número que você conhece.", "Agora o seu celular toca.", "\"Mãe\".",
        "Você pede a palavra.", "Tem uma palavra neste vídeo que eu nunca disse em voz alta.", "Viu qual é?", "Comente.",
        "Siga para mais IA, explicada assim."],
 "hi": ["लगभग 3 में से 1 व्यक्ति कहता है कि उन्हें एक नकली आवाज़ ने कॉल किया।", "सोचिए।", "आपका फ़ोन बजता है।", "उस पर लिखा है \"माँ\"।",
        "वह रो रही है।", "उसे पैसे चाहिए। अभी।", "उसकी आवाज़ एक चाबी की तरह काम करती है।", "आप उसे सुनते हैं...", "और दरवाज़ा खुल जाता है।",
        "चाबी की नकल?", "बस उसे ठीक से देखना काफ़ी है।", "इस आवाज़ के लिए मैं जो ऐप इस्तेमाल करता हूँ, वह कहता है कि 30 सेकंड काफ़ी हो सकते हैं।",
        "एक वॉइस नोट।", "हाँ।", "यह आवाज़ मेरी ही आवाज़ की नकल है।", "और अब चाबी बनाने वाली मशीनें बिक रही हैं।",
        "एक सुरक्षा कंपनी ने अपराधियों के चैट ग्रुप पर नज़र रखी।", "आवाज़ की नकल का कारोबार 2 साल में 7 गुना से ज़्यादा बढ़ा।",
        "असली क्लोनिंग ऐप्स के चुराए हुए अकाउंट?", "लगभग 10 डॉलर से शुरू।", "मोड़?", "ये अपराधी सबसे ज़्यादा जिसकी बात करते हैं... वह माँ नहीं है।",
        "वह है आपका बैंक।", "एक नकली बैंक लाइन कॉल करती है और आपका कोड माँगती है।", "वह कोड आपका दूसरा ताला है।", "उसे बोल दिया, तो वे अंदर हैं।",
        "पेंच?", "ये आँकड़े उन कंपनियों के हैं जो सुरक्षा बेचती हैं।", "वे पोस्ट और सर्वे के जवाब गिनती हैं, चुराया गया पैसा नहीं।",
        "तो 2 ऐसे ताले लगाइए जिन्हें कोई नकल न खोल सके।", "एक।", "परिवार का एक गुप्त शब्द, आमने-सामने तय किया हुआ।", "दो।",
        "आपका कोड कभी आपके फ़ोन से बाहर नहीं जाता।", "असली बैंक कभी नहीं माँगेगा।", "फ़ोन काटिए, और किसी जाने-पहचाने नंबर पर कॉल कीजिए।",
        "अब आपका फ़ोन बजता है।", "\"माँ\"।", "आप वह शब्द पूछते हैं।", "इस वीडियो में एक शब्द है जो मैंने कभी ज़ोर से नहीं कहा।",
        "पकड़ा?", "कमेंट कीजिए।", "AI को ऐसे ही समझने के लिए फ़ॉलो कीजिए।"],
 "id": ["Hampir 1 dari 3 orang bilang pernah ditelepon suara palsu.", "Bayangkan.", "Ponselmu berdering.", "Tertulis \"Ibu\".",
        "Dia menangis.", "Dia butuh uang. SEKARANG.", "Suaranya bekerja seperti kunci.", "Kamu mendengarnya...", "dan pintu terbuka.",
        "Menyalin kunci?", "Cukup melihatnya dengan jelas.", "Aplikasi yang saya pakai untuk suara ini bilang 30 detik bisa cukup.",
        "Satu pesan suara.", "Ya.", "Suara ini adalah salinan suara saya.", "Dan sekarang mesin penyalin kunci dijual.",
        "Sebuah perusahaan keamanan memantau grup obrolan para penjahat.",
        "Perdagangan kloning suara tumbuh lebih dari 7 kali dalam 2 tahun.", "Akun curian dari aplikasi kloning asli?",
        "Mulai sekitar 10 dolar.", "Kejutannya?", "Yang paling sering dibahas para penjahat ini... bukan ibu.", "Tapi BANK kamu.",
        "Saluran bank palsu menelepon dan meminta kodemu.", "Kode itu kunci keduamu.", "Kalau kamu bacakan, mereka masuk.",
        "Tapi ada catatannya.", "Angka-angka ini dari perusahaan yang menjual perlindungan.",
        "Mereka menghitung unggahan dan jawaban survei, bukan uang yang dicuri.", "Jadi pasang 2 kunci yang tak bisa dibuka salinan.",
        "Satu.", "Kata rahasia keluarga, disepakati langsung bertatap muka.", "Dua.", "Kodemu tidak pernah keluar dari ponselmu.",
        "Bank sungguhan tidak akan memintanya.", "Tutup telepon, lalu hubungi nomor yang kamu kenal.", "Sekarang ponselmu berdering.",
        "\"Ibu\".", "Kamu tanyakan katanya.", "Ada satu kata di video ini yang tak pernah saya ucapkan.", "Sudah lihat?", "Tulis di komentar.",
        "Ikuti untuk AI lainnya, dijelaskan seperti ini."],
}

out = []
for n, tc, txt in cues:
    for a, b in FIX:
        txt = txt.replace(a, b)
    out.append((n, tc, txt))
open(EN, "w").write("\n\n".join(f"{n}\n{tc}\n{txt}" for n, tc, txt in out) + "\n")
for lang, lines in TR.items():
    assert len(lines) == len(cues), (lang, len(lines))
    open(f"short17-captions.{lang}.srt", "w").write("\n\n".join(f"{n}\n{tc}\n{t}" for (n, tc, _), t in zip(cues, lines)) + "\n")
print("wrote", EN, "and", ", ".join(TR))
