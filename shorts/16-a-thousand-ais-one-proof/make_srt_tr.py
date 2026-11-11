"""Short #16: tidy the English upload subtitles (numbers as digits) and write the translated ones on the same timings
(worldwide rule). Reads short16-captions.srt (tools/srt_from_words.py); rewrites it and writes
short16-captions.{es,pt,hi,id}.srt.
Usage: python3 ../../tools/srt_from_words.py words.json short16-captions.srt && python3 make_srt_tr.py
"""
EN = "short16-captions.srt"
blocks = open(EN).read().strip().split("\n\n")
cues = [(b.split("\n")[0], b.split("\n")[1], " ".join(b.split("\n")[2:])) for b in blocks]
assert len(cues) == 36, len(cues)

FIX = [("3 hundred and fifty-eight", "358"), ("Thirteen million", "13 million"), ("eleven days", "11 days"),
       ("A thousand copies", "1,000 copies"), ("nine hundred and ninety-nine", "999"), ("sixty sections", "60 sections"),
       ("forty-seven couldn't", "47 couldn't"), ("the other ten", "the other 10"), ("seventy minutes", "70 minutes"),
       ("thirty hours", "30 hours"), ("sixty checkpoints", "60 checkpoints"), ("forty-seven bricks", "47 bricks"),
       ("nineteen automatic", "19 automatic")]

TR = {
 "es": ["Estas IA dijeron que la mayor parte del trabajo no se podía hacer.", "Y luego lo hicieron.",
        "Imagina un edificio famoso en papel.",
        "Ahora reconstrúyelo ladrillo a ladrillo, mientras un inspector estricto revisa cada ladrillo.",
        "El edificio es una famosa demostración matemática.", "Fermat escribió la regla en el margen de un libro en 1637.",
        "Demostrarla tomó 358 años.", "Pero el papel puede esconder errores.", "En un lenguaje de computadora llamado Lean,",
        "el inspector es una máquina, y nada se le escapa.", "En septiembre, agentes de Claude lo lograron por primera vez.",
        "13 millones de líneas, un investigador guiándolos, 11 días.",
        "Esta semana, Anthropic lo intentó de nuevo con Claude Fable 5.2.", "1.000 copias, sin investigador.",
        "Un jefe y 999 ayudantes.", "¿El giro?", "Los ayudantes revisaron 60 partes y dijeron que 47 no se podían",
        "hacer a tiempo.", "El jefe las dejó a un lado y puso a casi todos en las otras 10.",
        "Listas en unos 70 minutos.", "Entonces el jefe escribió: \"No hay razón para quedarse quieto\".",
        "Y mandó a los ayudantes de vuelta a las difíciles.",
        "Menos de 30 horas después, toda la demostración pasó la inspección.", "¿La trampa?",
        "Los humanos diseñaron este edificio hace mucho,", "y el equipo tenía ventaja: 60 puntos de control,",
        "un mapa de una línea, 47 ladrillos ya puestos.", "¿La lección de Anthropic?",
        "Los agentes se rinden demasiado pronto con los problemas difíciles.",
        "Incluso este jefe recibió 19 recordatorios automáticos para seguir.",
        "Así que cuando una IA diga que algo no se puede hacer,", "dile que siga.",
        "Hay una palabra en este video que nunca dije en voz alta.", "¿La viste?", "Escríbela en los comentarios.",
        "Sígueme para más IA, explicada así."],
 "pt": ["Essas IAs disseram que a maior parte do trabalho não dava para fazer.", "E depois fizeram.",
        "Imagine um prédio famoso no papel.",
        "Agora reconstrua tijolo por tijolo, enquanto um inspetor rigoroso confere cada tijolo.",
        "O prédio é uma famosa prova matemática.", "Fermat rabiscou a regra na margem de um livro em 1637.",
        "Provar isso levou 358 anos.", "Mas o papel pode esconder erros.", "Numa linguagem de computador chamada Lean,",
        "o inspetor é uma máquina, e nada passa por ele.", "Em setembro, agentes do Claude conseguiram pela primeira vez.",
        "13 milhões de linhas, um pesquisador guiando, 11 dias.",
        "Esta semana, a Anthropic tentou de novo com o Claude Fable 5.2.", "1.000 cópias, sem pesquisador.",
        "Um chefe e 999 ajudantes.", "A reviravolta?", "Os ajudantes olharam 60 partes e disseram que 47 não dava para fazer",
        "a tempo.", "O chefe deixou essas de lado e colocou quase todos nas outras 10.",
        "Prontas em uns 70 minutos.", "Aí o chefe escreveu: \"Não há motivo para ficar parado\".",
        "E mandou os ajudantes de volta para as difíceis.",
        "Menos de 30 horas depois, a prova inteira passou pelo inspetor.", "O porém?",
        "Humanos projetaram esse prédio há muito tempo,", "e a equipe saiu na frente: 60 pontos de controle,",
        "um mapa de uma linha, 47 tijolos já assentados.", "A lição da Anthropic?",
        "Agentes desistem cedo demais de problemas difíceis.",
        "Até esse chefe recebeu 19 lembretes automáticos para continuar.",
        "Então, quando uma IA disser que algo não dá para fazer,", "diga para ela continuar.",
        "Tem uma palavra neste vídeo que eu nunca falei em voz alta.", "Viu qual é?", "Comente.",
        "Siga para mais IA, explicada assim."],
 "hi": ["इन AI ने कहा कि ज़्यादातर काम नहीं हो सकता।", "फिर उन्होंने कर दिखाया।",
        "कागज़ पर बनी एक मशहूर इमारत की कल्पना करो।",
        "अब इसे ईंट-ईंट करके फिर से बनाओ, और एक सख़्त इंस्पेक्टर हर ईंट जाँचे।",
        "यह इमारत गणित का एक मशहूर प्रमाण है।", "फ़र्मा ने 1637 में एक किताब के हाशिये पर यह नियम लिखा था।",
        "इसे साबित करने में 358 साल लगे।", "लेकिन कागज़ पर गलतियाँ छिप सकती हैं।", "Lean नाम की एक कंप्यूटर भाषा में",
        "इंस्पेक्टर एक मशीन है, और उससे कुछ नहीं बचता।", "सितंबर में, Claude एजेंट्स ने पहली बार यह कर दिखाया।",
        "1.3 करोड़ लाइनें, एक रिसर्चर का मार्गदर्शन, 11 दिन।",
        "इस हफ़्ते, Anthropic ने Claude Fable 5.2 के साथ फिर कोशिश की।", "1,000 कॉपियाँ, कोई रिसर्चर नहीं।",
        "एक बॉस और 999 हेल्पर।", "ट्विस्ट?", "हेल्पर्स ने 60 हिस्से देखे और कहा कि 47 समय पर",
        "नहीं हो सकते।", "बॉस ने उन्हें अलग रखा और लगभग सबको बाकी 10 पर लगा दिया।",
        "लगभग 70 मिनट में पूरे।", "फिर बॉस ने लिखा: \"बेकार बैठने की कोई वजह नहीं है।\"",
        "और हेल्पर्स को वापस मुश्किल हिस्सों पर भेज दिया।",
        "30 घंटे से भी कम में, पूरा प्रमाण इंस्पेक्टर से पास हो गया।", "पेच क्या है?",
        "यह इमारत इंसानों ने बहुत पहले डिज़ाइन की थी,", "और टीम को बढ़त मिली थी: 60 चेकपॉइंट,",
        "एक लाइन का नक्शा, 47 ईंटें पहले से लगी हुई।", "Anthropic का सबक?",
        "एजेंट्स मुश्किल समस्याओं पर बहुत जल्दी हार मान लेते हैं।",
        "इस बॉस को भी चलते रहने के लिए 19 ऑटोमैटिक रिमाइंडर मिले।",
        "तो जब कोई AI कहे कि कुछ नहीं हो सकता,", "उससे कहो कि चलते रहो।",
        "इस वीडियो में एक शब्द है जो मैंने कभी ज़ोर से नहीं बोला।", "पकड़ा?", "कमेंट करो।",
        "ऐसे ही समझाए गए AI के लिए फ़ॉलो करो।"],
 "id": ["AI ini bilang sebagian besar pekerjaannya tidak bisa dikerjakan.", "Lalu mereka berhasil.",
        "Bayangkan sebuah bangunan terkenal di atas kertas.",
        "Sekarang bangun ulang bata demi bata, sementara seorang pengawas ketat memeriksa setiap bata.",
        "Bangunan itu adalah sebuah bukti matematika terkenal.", "Fermat menulis aturan itu di pinggir halaman buku pada 1637.",
        "Membuktikannya butuh 358 tahun.", "Tapi kertas bisa menyembunyikan kesalahan.", "Dalam bahasa komputer bernama Lean,",
        "pengawasnya adalah mesin, dan tidak ada yang lolos.", "Pada September, agen Claude berhasil untuk pertama kalinya.",
        "13 juta baris, seorang peneliti membimbing, 11 hari.",
        "Minggu ini, Anthropic mencoba lagi dengan Claude Fable 5.2.", "1.000 salinan, tanpa peneliti.",
        "Satu bos dan 999 pembantu.", "Kejutannya?", "Para pembantu melihat 60 bagian dan bilang 47 tidak bisa selesai",
        "tepat waktu.", "Bos menyisihkannya dan menaruh hampir semua orang di 10 bagian lainnya.",
        "Selesai dalam sekitar 70 menit.", "Lalu bos menulis: \"Tidak ada alasan untuk diam.\"",
        "Dan mengirim para pembantu kembali ke bagian yang sulit.",
        "Kurang dari 30 jam kemudian, seluruh bukti lolos pemeriksaan.", "Masalahnya?",
        "Manusia sudah merancang bangunan ini sejak lama,", "dan timnya punya modal awal: 60 titik periksa,",
        "peta satu baris, 47 bata yang sudah terpasang.", "Pelajaran dari Anthropic?",
        "Agen menyerah terlalu cepat pada masalah yang sulit.",
        "Bahkan bos ini dapat 19 pengingat otomatis untuk terus jalan.",
        "Jadi saat AI bilang sesuatu tidak bisa dikerjakan,", "suruh dia terus jalan.",
        "Ada satu kata di video ini yang tidak pernah kuucapkan.", "Sudah lihat?", "Tulis di komentar.",
        "Ikuti untuk AI lainnya, dijelaskan seperti ini."],
}


def wrap(t, n=42):
    if len(t) <= n:
        return t
    words, best = t.split(), None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        d = abs(len(a) - len(b))
        if best is None or d < best[0]:
            best = (d, a + "\n" + b)
    return best[1]


def write(path, texts):
    out = []
    for (n, tm, _), t in zip(cues, texts):
        out.append(f"{n}\n{tm}\n{wrap(t)}")
    open(path, "w").write("\n\n".join(out) + "\n")


en = []
for _, _, t in cues:
    for a, b in FIX:
        t = t.replace(a, b)
    en.append(t)
write(EN, en)
for lang, texts in TR.items():
    assert len(texts) == 36, (lang, len(texts))
    write(f"short16-captions.{lang}.srt", texts)
print("wrote en (tidied),", ", ".join(TR))
