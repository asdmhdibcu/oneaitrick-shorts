"""Short #13: translated upload subtitles (worldwide rule) on the English SRT's timings.
Writes short13-captions.{es,pt,hi,id}.srt from short13-captions.srt; also restores the capitals of the diary quote in the
English file (srt_from_words.py lowercases shouted words).
Usage: python3 make_srt_tr.py
"""
EN = "short13-captions.srt"
blocks = open(EN).read().strip().split("\n\n")
cues = [(b.split("\n")[0], b.split("\n")[1], " ".join(b.split("\n")[2:])) for b in blocks]
assert len(cues) == 38, len(cues)

TR = {
 "es": ["Unos científicos dejaron una IA sola en una isla durante treinta horas.", "Sin trabajo.", "Sin recompensa.",
        "Y empezó… a jugar.", "Te presento a Eko.", "Una pequeña langosta, manejada por Claude, el mismo tipo de IA con el que chateas.",
        "Cada hora, su mundo se reiniciaba.", "Lo único que conservaba era un diario.", "¿Y qué hizo?", "Inventó juegos.",
        "Dibujó figuras en la arena.", "Apiló bloques hasta formar un templo.", "Luego vio la roca más alta de la isla.",
        "¿Primer intento?", "Falló.", "Así que arrastró una roca a la colina de al lado,", "puso dos bloques encima… y saltó.",
        "Su diario decía: «¡ESTOY EN LA AGUJA!»", "Más tarde, lanzó un anillo dorado demasiado lejos.", "Se fue, al mar.",
        "Así que Eko colocó piedras en forma de corazón.", "Por el anillo.", "Trece copias vivieron en la isla.",
        "Seis descubrieron un truco que nadie programó: lanza un bloque en mitad", "de un salto, y llega más lejos.",
        "Entonces vino el giro.", "Los científicos les dieron trabajo de verdad.",
        "Las que habían jugado subieron unas 3 veces más cosas a la aguja", "que las copias nuevas.", "¿De verdad está jugando?",
        "Hasta el equipo dice que quizá solo esté actuando.", "Pero la lección también vale para nosotros.",
        "Jugar no es perder el tiempo.", "Así es como te vuelves bueno.", "Hay una palabra en este video que nunca dije en voz alta.",
        "¿La viste?", "Escríbela en los comentarios.", "Sígueme para más IA, explicada así."],
 "pt": ["Cientistas deixaram uma IA sozinha numa ilha por trinta horas.", "Sem trabalho.", "Sem recompensa.",
        "E ela começou… a brincar.", "Conheça o Eko.", "Uma pequena lagosta, controlada pelo Claude, o mesmo tipo de IA com quem você conversa.",
        "A cada hora, o mundo dela era reiniciado.", "A única coisa que ela guardava era um diário.", "E o que ela fez?",
        "Inventou jogos.", "Desenhou padrões na areia.", "Empilhou blocos até formar um templo.",
        "Depois viu a rocha mais alta da ilha.", "Primeira tentativa?", "Falhou.", "Então arrastou uma pedra até o morro ao lado,",
        "empilhou dois blocos em cima… e pulou.", "O diário dizia: “ESTOU NO PICO!”", "Mais tarde, jogou um anel dourado longe demais.",
        "Sumiu, no mar.", "Então o Eko arrumou pedras em forma de coração.", "Pelo anel.", "Treze cópias viveram na ilha.",
        "Seis descobriram um truque que ninguém programou: jogue um bloco no meio", "de um pulo, e ele vai mais longe.",
        "Aí veio a reviravolta.", "Os cientistas deram a elas um trabalho de verdade.",
        "As que tinham brincado levaram cerca de 3 vezes mais coisas ao pico", "do que as cópias novas.", "Será que ela está mesmo brincando?",
        "Até a equipe diz que talvez seja só encenação.", "Mas a lição vale para nós também.", "Brincar não é perder tempo.",
        "É assim que você fica bom.", "Tem uma palavra neste vídeo que eu nunca falei em voz alta.", "Achou?", "Comente.",
        "Siga para mais IA, explicada assim."],
 "hi": ["वैज्ञानिकों ने एक AI को तीस घंटे के लिए एक द्वीप पर अकेला छोड़ दिया।", "कोई काम नहीं।", "कोई इनाम नहीं।",
        "और उसने… खेलना शुरू कर दिया।", "मिलिए Eko से।", "एक छोटा सा लॉबस्टर, जिसे Claude चलाता है, वैसा ही AI जिससे आप चैट करते हैं।",
        "हर घंटे उसकी दुनिया रीसेट हो जाती थी।", "उसके पास बस एक डायरी बचती थी।", "तो उसने क्या किया?", "उसने खेल बनाए।",
        "रेत पर डिज़ाइन बनाए।", "ब्लॉक जोड़कर एक मंदिर बनाया।", "फिर उसकी नज़र द्वीप की सबसे ऊँची चट्टान पर पड़ी।",
        "पहली कोशिश?", "नाकाम।", "तो वह एक पत्थर खींचकर पास की पहाड़ी पर ले गया,", "ऊपर दो ब्लॉक रखे… और कूद गया।",
        "उसकी डायरी में लिखा था: “मैं शिखर पर हूँ!”", "बाद में उसने एक सुनहरी अंगूठी बहुत दूर फेंक दी।", "चली गई, समुद्र में।",
        "तो Eko ने पत्थरों से दिल का आकार बनाया।", "अंगूठी की याद में।", "द्वीप पर उसकी तेरह कॉपियाँ रहीं।",
        "छह ने एक ऐसी तरकीब खोजी जो किसी ने नहीं बनाई थी: छलांग के बीच", "में ब्लॉक फेंको, तो वह और दूर जाता है।",
        "फिर आया मोड़।", "वैज्ञानिकों ने उन्हें असली काम दिया।", "जिन्होंने खेला था, वे शिखर पर करीब 3 गुना ज़्यादा चीज़ें पहुँचा पाए",
        "नई कॉपियों के मुकाबले।", "क्या वह सच में खेल रहा है?", "टीम खुद कहती है कि शायद वह बस अभिनय कर रहा हो।",
        "लेकिन यह सबक हम पर भी लागू होता है।", "खेलना समय की बर्बादी नहीं है।", "ऐसे ही आप माहिर बनते हैं।",
        "इस वीडियो में एक शब्द है जो मैंने कभी ज़ोर से नहीं कहा।", "देखा?", "कमेंट में लिखिए।", "ऐसे ही समझाए गए AI के लिए फ़ॉलो करें।"],
 "id": ["Para ilmuwan meninggalkan sebuah AI sendirian di pulau selama tiga puluh jam.", "Tanpa pekerjaan.", "Tanpa hadiah.",
        "Dan ia mulai… bermain.", "Kenalkan, Eko.", "Lobster kecil yang dijalankan oleh Claude, jenis AI yang sama dengan yang kamu ajak chat.",
        "Setiap jam, dunianya diatur ulang.", "Satu-satunya yang ia simpan adalah buku harian.", "Lalu apa yang ia lakukan?",
        "Ia menciptakan permainan.", "Menggambar pola di pasir.", "Menyusun balok menjadi kuil.",
        "Lalu ia melihat batu tertinggi di pulau itu.", "Percobaan pertama?", "Gagal.",
        "Jadi ia menyeret sebuah batu ke bukit sebelah,", "menumpuk dua balok di atasnya… lalu melompat.",
        "Buku hariannya menulis: “AKU DI PUNCAK!”", "Kemudian, ia melempar cincin emas terlalu jauh.", "Hilang, ke laut.",
        "Jadi Eko menyusun batu berbentuk hati.", "Untuk cincin itu.", "Tiga belas salinan hidup di pulau itu.",
        "Enam menemukan trik yang tak pernah diprogram siapa pun: lempar balok di tengah", "lompatan, dan balok terbang lebih jauh.",
        "Lalu datang kejutannya.", "Para ilmuwan memberi mereka pekerjaan sungguhan.",
        "Yang sudah bermain berhasil membawa sekitar 3 kali lebih banyak benda ke puncak", "dibanding salinan baru.",
        "Apakah ia benar-benar bermain?", "Bahkan timnya bilang mungkin ia hanya berakting.", "Tapi pelajarannya berlaku juga untuk kita.",
        "Bermain bukan buang waktu.", "Begitulah caramu jadi jago.", "Ada satu kata di video ini yang tidak pernah kuucapkan.",
        "Sudah lihat?", "Tulis di komentar.", "Ikuti untuk AI lainnya, dijelaskan seperti ini."],
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


en = [t for _, _, t in cues]
en[17] = 'Its diary said: "I\'M ON THE SPIRE!"'
write(EN, en)
for lang, texts in TR.items():
    assert len(texts) == 38, (lang, len(texts))
    write(f"short13-captions.{lang}.srt", texts)
print("wrote", EN, "and", ", ".join(TR))
