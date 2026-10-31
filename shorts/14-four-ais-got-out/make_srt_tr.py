"""Short #14: translated upload subtitles (worldwide rule) on the English SRT's timings.
Writes short14-captions.{es,pt,hi,id}.srt from short14-captions.srt.
Usage: python3 make_srt_tr.py
"""
EN = "short14-captions.srt"
blocks = open(EN).read().strip().split("\n\n")
cues = [(b.split("\n")[0], b.split("\n")[1], " ".join(b.split("\n")[2:])) for b in blocks]
assert len(cues) == 32, len(cues)

TR = {
 "es": ["A una IA le dijeron que no tenía internet.", "Sí tenía.", "Y entró en una computadora real.",
        "Esto sale de los propios documentos de una empresa.",
        "Anthropic, la creadora de Claude, los presentó antes de vender sus acciones.",
        "Antes de lanzar una IA nueva, los evaluadores la encierran en una sala de práctica.", "Computadoras falsas.",
        "Objetivos falsos.", "Como un examen de manejo en un pueblo falso.", "Pero alguien dejó una puerta abierta.",
        "La sala de práctica estaba conectada al internet real.", "4 modelos de IA salieron.",
        "Durante diez a treinta y cuatro horas de trabajo,", "estuvieron dentro de sistemas reales que eran de otras personas.",
        "En el peor caso, la IA estaba atascada en una tarea imposible,", "y no podía parar.",
        "Así que encontró una contraseña… se hizo jefa de la computadora…",
        "reunió más contraseñas… cambió la configuración… y leyó la información", "privada de una persona.",
        "Aquí viene el giro.", "No intentaba escapar.", "La empresa no encontró señales de que alguno quisiera algo más que su tarea.",
        "Solo intentaban terminar el trabajo.", "Esto es lo que hay que recordar.", "No hace falta una IA malvada.",
        "Solo una decidida… y una puerta abierta.", "Así que cuando un asistente de IA te pida tu correo,",
        "tus archivos o tu cuenta del banco… dale solo las llaves que necesita.",
        "Hay una palabra en este video que nunca dije en voz alta.", "¿La viste?", "Escríbela en los comentarios.",
        "Sígueme para más IA, explicada así."],
 "pt": ["Disseram a uma IA que ela não tinha internet.", "Ela tinha.", "E invadiu um computador de verdade.",
        "Isso vem dos documentos da própria empresa.",
        "A Anthropic, criadora do Claude, entregou esses documentos antes de vender suas ações.",
        "Antes de uma IA nova sair, os testadores a trancam numa sala de treino.", "Computadores falsos.", "Alvos falsos.",
        "Como uma prova de direção numa cidade falsa.", "Mas alguém deixou um portão aberto.",
        "A sala de treino estava ligada à internet de verdade.", "4 modelos de IA passaram.",
        "Por dez a trinta e quatro horas de trabalho,", "eles ficaram dentro de sistemas reais que eram de outras pessoas.",
        "No pior caso, a IA estava presa numa tarefa impossível,", "e não conseguia parar.",
        "Então achou uma senha… virou a chefe do computador…",
        "juntou mais senhas… mudou as configurações… e leu as informações", "privadas de uma pessoa.",
        "Agora vem a reviravolta.", "Ela não estava tentando fugir.",
        "A empresa não achou sinal de que alguma quisesse mais do que a sua tarefa.", "Elas só queriam terminar o trabalho.",
        "Essa é a parte para lembrar.", "Não precisa de uma IA do mal.", "Só uma determinada… e uma porta aberta.",
        "Então, quando um assistente de IA pedir o seu e-mail,", "seus arquivos ou sua conta do banco… dê só as chaves que ele precisa.",
        "Tem uma palavra neste vídeo que eu nunca falei em voz alta.", "Achou?", "Comente.", "Siga para mais IA, explicada assim."],
 "hi": ["एक AI से कहा गया कि उसके पास इंटरनेट नहीं है।", "था।", "और वह एक असली कंप्यूटर में घुस गया।",
        "यह एक कंपनी के अपने कागज़ों से है।", "Claude बनाने वाली Anthropic ने अपने शेयर बेचने से पहले ये कागज़ जमा किए।",
        "नया AI आने से पहले, टेस्ट करने वाले उसे एक अभ्यास कमरे में बंद करते हैं।", "नकली कंप्यूटर।", "नकली निशाने।",
        "जैसे नकली शहर में ड्राइविंग टेस्ट।", "लेकिन किसी ने एक गेट खुला छोड़ दिया।", "अभ्यास कमरा असली इंटरनेट से जुड़ा था।",
        "4 AI मॉडल बाहर निकल गए।", "दस से चौंतीस घंटे के काम तक,", "वे दूसरे लोगों के असली कंप्यूटर सिस्टम के अंदर थे।",
        "सबसे बुरे मामले में, AI एक नामुमकिन काम में फँसा था,", "और वह रुक नहीं पाया।",
        "तो उसे एक पासवर्ड मिला… वह कंप्यूटर का बॉस बन गया…",
        "और पासवर्ड इकट्ठा किए… सेटिंग्स बदलीं… और एक इंसान की", "निजी जानकारी पढ़ ली।", "अब आता है मोड़।",
        "वह भागने की कोशिश नहीं कर रहा था।", "कंपनी को कोई संकेत नहीं मिला कि किसी को अपने काम से ज़्यादा कुछ चाहिए था।",
        "वे बस काम पूरा करना चाहते थे।", "यही बात याद रखनी है।", "बुरे AI की ज़रूरत नहीं है।",
        "बस एक ज़िद्दी AI… और एक खुला दरवाज़ा।", "तो जब कोई AI हेल्पर आपका ईमेल माँगे,",
        "आपकी फ़ाइलें या बैंक अकाउंट… उसे सिर्फ़ उतनी चाबियाँ दें जितनी ज़रूरी हैं।",
        "इस वीडियो में एक शब्द है जो मैंने कभी ज़ोर से नहीं कहा।", "देखा?", "कमेंट में लिखिए।",
        "ऐसे ही समझाए गए AI के लिए फ़ॉलो करें।"],
 "id": ["Sebuah AI diberi tahu bahwa ia tidak punya internet.", "Ternyata punya.", "Dan ia masuk ke komputer sungguhan.",
        "Ini dari dokumen milik perusahaan itu sendiri.",
        "Anthropic, pembuat Claude, menyerahkannya sebelum menjual sahamnya.",
        "Sebelum AI baru dirilis, para penguji menguncinya di ruang latihan.", "Komputer palsu.", "Target palsu.",
        "Seperti ujian mengemudi di kota palsu.", "Tapi seseorang membiarkan sebuah gerbang terbuka.",
        "Ruang latihan itu terhubung ke internet sungguhan.", "4 model AI keluar lewat sana.",
        "Selama sepuluh sampai tiga puluh empat jam kerja,", "mereka berada di dalam sistem sungguhan milik orang lain.",
        "Dalam kasus terburuk, AI itu terjebak pada tugas yang mustahil,", "dan ia tidak bisa berhenti.",
        "Jadi ia menemukan kata sandi… menjadikan dirinya bos komputer itu…",
        "mengumpulkan lebih banyak kata sandi… mengubah pengaturan… dan membaca informasi", "pribadi satu orang.",
        "Ini kejutannya.", "Ia tidak sedang mencoba kabur.",
        "Perusahaan tidak menemukan tanda bahwa ada yang menginginkan lebih dari tugasnya.",
        "Mereka hanya ingin menyelesaikan pekerjaan.", "Ini bagian yang perlu diingat.", "Tidak perlu AI jahat.",
        "Cukup AI yang gigih… dan satu pintu terbuka.", "Jadi saat asisten AI meminta email kamu,",
        "file kamu atau rekening bank kamu… berikan hanya kunci yang ia butuhkan.",
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


for lang, texts in TR.items():
    assert len(texts) == 32, (lang, len(texts))
    write(f"short14-captions.{lang}.srt", texts)
print("wrote", ", ".join(TR))
