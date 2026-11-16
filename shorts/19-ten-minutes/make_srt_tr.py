"""Short #19: tidy the English upload subtitles (numbers as digits) and write the translated ones on the same timings
(worldwide rule). Reads short19-captions.srt (tools/srt_from_words.py); rewrites it and writes
short19-captions.{es,pt,hi,id}.srt. No translation contains GRIT, the hidden word. The last cue of each language runs
into its first one, as the voice does ("...all it took was... Ten minutes of AI").
Usage: python3 ../../tools/srt_from_words.py words.json short19-captions.srt && python3 make_srt_tr.py
"""
EN = "short19-captions.srt"
blocks = open(EN).read().strip().split("\n\n")
cues = [(b.split("\n")[0], b.split("\n")[1], " ".join(b.split("\n")[2:])) for b in blocks]
assert len(cues) == 29, len(cues)

FIX = [("ten minutes of AI...", "Ten minutes of AI..."), ("one skip in a hundred", "1 skip in 100"), ("After AI: eight.", "After AI: 8.")]

TR = {
 "es": ["Diez minutos de IA...", "y la gente se rindió casi el doble de veces.",
        "Imagina tu chatbot de IA como las ruedas de apoyo de una bici.", "Más de mil personas resolvieron problemas de matemáticas.",
        "Cerca de la mitad recibió las ruedas.", "Entonces, sin aviso...", "les quitaron las ruedas.",
        "Solos, resolvieron menos problemas que quienes nunca las tuvieron.", "Y se saltaron preguntas casi el doble de veces.",
        "En lectura, también.", "Sin IA: 1 pregunta saltada de cada 100.", "Después de la IA: 8.",
        "Los investigadores creen que la IA nos acostumbra a esperar respuestas al instante...",
        "así que nunca aprendemos a mantener el equilibrio.", "Aquí viene lo raro.", "Quienes solo le pidieron pistas...",
        "lo hicieron casi igual de bien que quienes no usaron IA.", "¿La trampa?", "Pruebas cortas.",
        "Y lo de las pistas es una señal, no una prueba.", "Así que pídele a tu IA una pista primero...", "no la respuesta.",
        "Como una mano en el asiento de la bici... que te suelta.",
        "Hay una palabra en este video que nunca dije en voz alta.", "¿La viste?", "Escríbela en los comentarios.",
        "Sígueme para más IA, explicada así.", "Y recuerda...", "solo hicieron falta..."],
 "pt": ["Dez minutos de IA...", "e as pessoas desistiram quase o dobro de vezes.",
        "Imagine seu chatbot de IA como as rodinhas de uma bicicleta.", "Mais de mil pessoas resolveram problemas de matemática.",
        "Cerca da metade ganhou as rodinhas.", "Então, sem aviso...", "as rodinhas saíram.",
        "Sozinhas, elas resolveram menos problemas do que quem nunca teve as rodinhas.", "E pularam questões quase o dobro de vezes.",
        "Na leitura, também.", "Sem IA: 1 questão pulada em cada 100.", "Depois da IA: 8.",
        "Os pesquisadores acham que a IA nos acostuma a esperar respostas na hora...",
        "e aí a gente nunca aprende a se equilibrar.", "Agora vem a parte estranha.", "Quem só pediu dicas...",
        "foi quase tão bem quanto quem não usou IA.", "O porém?", "Testes curtos.",
        "E o resultado das dicas é uma pista, não uma prova.", "Então peça à sua IA uma dica primeiro...", "não a resposta.",
        "Como uma mão no banco da bicicleta... que solta.",
        "Tem uma palavra neste vídeo que eu nunca falei em voz alta.", "Você viu?", "Escreva nos comentários.",
        "Siga para mais IA, explicada assim.", "E lembre...", "bastaram..."],
 "hi": ["AI के साथ दस मिनट...", "और लोगों ने लगभग दोगुनी बार हार मान ली।",
        "अपने AI चैटबॉट को साइकिल के ट्रेनिंग व्हील्स समझिए।", "एक हज़ार से ज़्यादा लोगों ने गणित के सवाल हल किए।",
        "लगभग आधे लोगों को ये पहिए मिले।", "फिर, बिना बताए...", "पहिए हटा दिए गए।",
        "अकेले में, उन्होंने उन लोगों से कम सवाल हल किए जिन्हें ये पहिए कभी मिले ही नहीं।", "और लगभग दोगुनी बार सवाल छोड़ दिए।",
        "पढ़ने वाले सवालों में भी।", "बिना AI: 100 में से 1 सवाल छोड़ा।", "AI के बाद: 8।",
        "रिसर्चर्स का मानना है कि AI हमें तुरंत जवाब की आदत डाल देता है...",
        "इसलिए हम कभी संतुलन बनाना नहीं सीखते।", "अब अजीब बात सुनिए।", "जिन लोगों ने सिर्फ़ हिंट माँगे...",
        "उन्होंने लगभग उतना ही अच्छा किया जितना बिना AI वालों ने।", "पेच क्या है?", "टेस्ट छोटे थे।",
        "और हिंट वाली बात एक सुराग है, सबूत नहीं।", "तो अपने AI से पहले हिंट माँगिए...", "जवाब नहीं।",
        "जैसे साइकिल की सीट पर रखा एक हाथ... जो छोड़ देता है।",
        "इस वीडियो में एक शब्द है जो मैंने कभी ज़ोर से नहीं बोला।", "दिखा?", "कमेंट में लिखिए।",
        "ऐसे ही समझाए गए AI के लिए फ़ॉलो करें।", "और याद रखिए...", "बस इतना लगा..."],
 "id": ["Sepuluh menit pakai AI...", "dan orang-orang menyerah hampir dua kali lebih sering.",
        "Bayangkan chatbot AI-mu sebagai roda bantu sepeda.", "Lebih dari seribu orang mengerjakan soal matematika.",
        "Sekitar setengahnya dapat roda bantu.", "Lalu, tanpa peringatan...", "roda bantunya dilepas.",
        "Sendirian, mereka menyelesaikan lebih sedikit soal daripada orang yang tidak pernah memakainya.",
        "Dan mereka melewati soal hampir dua kali lebih sering.", "Soal membaca juga.", "Tanpa AI: 1 soal dilewati dari 100.",
        "Setelah AI: 8.", "Para peneliti menduga AI membuat kita terbiasa menunggu jawaban instan...",
        "jadi kita tidak pernah belajar menjaga keseimbangan.", "Ini bagian anehnya.", "Orang yang hanya minta petunjuk...",
        "hasilnya hampir sama dengan orang tanpa AI.", "Masalahnya?", "Tesnya singkat.",
        "Dan temuan soal petunjuk itu baru dugaan, bukan bukti.", "Jadi, minta petunjuk dulu ke AI-mu...", "bukan jawabannya.",
        "Seperti tangan di sadel sepeda... yang kemudian melepas.",
        "Ada satu kata di video ini yang tidak pernah kuucapkan.", "Sudah lihat?", "Tulis di komentar.",
        "Ikuti untuk AI lainnya, dijelaskan seperti ini.", "Dan ingat...", "cukup dengan..."],
}

out = []
for n, tc, txt in cues:
    for a, b in FIX:
        txt = txt.replace(a, b)
    out.append((n, tc, txt))
open(EN, "w").write("\n\n".join(f"{n}\n{tc}\n{txt}" for n, tc, txt in out) + "\n")
for lang, lines in TR.items():
    assert len(lines) == len(cues), (lang, len(lines))
    assert not any("grit" in t.lower() for t in lines)
    open(f"short19-captions.{lang}.srt", "w").write("\n\n".join(f"{n}\n{tc}\n{t}" for (n, tc, _), t in zip(cues, lines)) + "\n")
print("wrote", EN, "and", ", ".join(TR))
