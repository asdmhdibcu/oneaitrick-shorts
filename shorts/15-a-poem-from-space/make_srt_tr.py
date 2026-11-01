"""Short #15: translated upload subtitles (worldwide rule) on the English SRT's timings.
Writes short15-captions.{es,pt,hi,id}.srt from short15-captions.srt.
Usage: python3 make_srt_tr.py
"""
EN = "short15-captions.srt"
blocks = open(EN).read().strip().split("\n\n")
cues = [(b.split("\n")[0], b.split("\n")[1], " ".join(b.split("\n")[2:])) for b in blocks]
assert len(cues) == 70, len(cues)

TR = {
 "es": ["Google acaba de lanzar una IA al espacio.", "Y lo primero que respondió… fue un poema.",
        "Bueno, para ser justos… se lo pidieron.", "Pero ese pequeño poema es el comienzo de una idea muy grande.",
        "Hace un mes, un cohete de SpaceX llevó un satélite del tamaño de un refrigerador",
        "a la órbita, hecho junto con una empresa llamada Planet.",
        "Dentro: un chip de IA de Google, del tipo que usa en sus enormes centros de datos,",
        "con el propio modelo de IA de Google, Gemma.", "Da la vuelta a la Tierra más o menos cada hora y media,",
        "así que los ingenieros le escriben cada vez que pasa por encima.", "¿Su primer pedido?", "Un haiku sobre el espacio.",
        "Llegó desde lo más alto del mundo:", "3 líneas cortas sobre mirar la Tierra desde arriba.",
        "Pero ¿por qué tanto esfuerzo?", "Porque la IA tiene hambre.",
        "Casi cada respuesta de IA que recibes viene de un centro de datos:",
        "un edificio lleno de computadoras, todas comiendo electricidad.",
        "Para 2030, los centros de datos podrían usar más electricidad que todo", "Japón hoy.",
        "Así que Google miró hacia arriba.", "El sol produce cien billones de veces más energía que toda",
        "la electricidad que produce la gente.", "Aquí abajo, los paneles solares se detienen de noche,",
        "y las nubes estorban.", "Pero en la órbita correcta, siguiendo la línea donde el día se junta con la noche,",
        "el sol casi nunca se pone.", "Un panel allá arriba produce hasta ocho veces más energía.",
        "Sol gratis, para siempre.", "¿Perfecto?", "No del todo.", "Los chips convierten la electricidad en calor.",
        "¿Sabes cuando tu teléfono se calienta demasiado y tiene que enfriarse?",
        "En la Tierra, ventiladores y agua se llevan ese calor.", "¿En el espacio?", "Sin aire.", "Sin viento.", "Sin agua.",
        "Piensa en un termo.", "El espacio vacío entre sus paredes mantiene caliente tu café.",
        "El espacio… es un termo gigante.", "Allá arriba, el calor solo puede salir como luz invisible,",
        "como el calor de una fogata.", "Por eso el satélite lleva paneles, llamados radiadores,", "para irradiarlo.",
        "Por ahora, la IA trabaja en ráfagas cortas… y luego descansa para enfriarse.", "Luego está la radiación.",
        "Partículas diminutas y rápidas pueden cambiar un uno por un cero.",
        "Un error de tipeo, justo en medio del pensamiento de la IA.",
        "Así que Google bombardeó sus chips con un haz de partículas mientras ejecutaban", "IA.",
        "Resistieron más de cinco años de radiación.", "¿El gran sueño?",
        "Decenas de satélites, volando a unos cien metros entre sí,", "compartiendo el trabajo y hablando por láser.",
        "Google dice que apuntar esos láseres es como darle a una moneda desde kilómetros",
        "de distancia… mientras los dos se mueven.", "Dos satélites de prueba subirán en 2027.",
        "Pero seamos honestos.", "Las propias cuentas de Google dicen que los lanzamientos tienen que abaratarse mucho:",
        "menos de doscientos dólares por kilo.", "Nadie puede arreglar un chip roto allá arriba.",
        "Y hasta el líder del proyecto dice que no será más barato que en la Tierra por años.",
        "Así que ese pequeño poema nos dice algo grande.", "Cada pregunta que le haces a una IA cuesta energía… y la búsqueda de más",
        "acaba de salir del planeta.", "Hay una palabra en este video que nunca dije en voz alta.", "¿La viste?",
        "Escríbela en los comentarios.", "Sígueme para más IA, explicada así."],
 "pt": ["O Google acabou de lançar uma IA no espaço.", "E a primeira coisa que ela respondeu… foi um poema.",
        "Tá, para ser justo… eles pediram um.", "Mas esse pequeno poema é o começo de uma ideia muito grande.",
        "Há um mês, um foguete da SpaceX levou um satélite do tamanho de uma geladeira",
        "para a órbita, feito com uma empresa chamada Planet.",
        "Dentro: um chip de IA do Google, do tipo que ele usa nos seus enormes data centers,",
        "rodando o próprio modelo de IA do Google, o Gemma.", "Ele dá a volta na Terra mais ou menos a cada hora e meia,",
        "então os engenheiros mandam mensagens toda vez que ele passa por cima.", "O primeiro pedido?", "Um haicai sobre o espaço.",
        "Ele chegou pelo topo do mundo:", "3 linhas curtas sobre olhar a Terra lá de cima.",
        "Mas por que tanto trabalho?", "Porque a IA tem fome.",
        "Quase toda resposta de IA que você recebe vem de um data center:",
        "um prédio cheio de computadores, todos comendo eletricidade.",
        "Até 2030, os data centers podem usar mais eletricidade do que o", "Japão inteiro usa hoje.",
        "Então o Google olhou para cima.", "O sol produz cem trilhões de vezes mais energia do que toda",
        "a eletricidade que as pessoas produzem.", "Aqui embaixo, os painéis solares param à noite,",
        "e as nuvens atrapalham.", "Mas na órbita certa, seguindo a linha onde o dia encontra a noite,",
        "o sol quase nunca se põe.", "Um painel lá em cima gera até oito vezes mais energia.",
        "Sol de graça, para sempre.", "Perfeito?", "Não exatamente.", "Chips transformam eletricidade em calor.",
        "Sabe quando o seu celular esquenta demais e precisa esfriar?",
        "Na Terra, ventiladores e água levam esse calor embora.", "No espaço?", "Sem ar.", "Sem vento.", "Sem água.",
        "Pense numa garrafa térmica.", "O espaço vazio entre as paredes mantém o seu café quente.",
        "O espaço… é uma garrafa térmica gigante.", "Lá em cima, o calor só sai como luz invisível,",
        "como o calor de uma fogueira.", "Por isso o satélite leva painéis, chamados radiadores,", "para irradiar esse calor.",
        "Por enquanto, a IA trabalha em rajadas curtas… e depois descansa para esfriar.", "Depois vem a radiação.",
        "Partículas minúsculas e rápidas podem trocar um um por um zero.",
        "Um erro de digitação, bem no meio do pensamento da IA.",
        "Então o Google bombardeou seus chips com um feixe de partículas enquanto rodavam", "IA.",
        "Eles aguentaram mais de cinco anos de radiação.", "O grande sonho?",
        "Dezenas de satélites, voando a uns cem metros um do outro,", "dividindo o trabalho e conversando por laser.",
        "O Google diz que mirar esses lasers é como acertar uma moeda a quilômetros",
        "de distância… com os dois em movimento.", "Dois satélites de teste sobem em 2027.",
        "Mas vamos ser sinceros.", "As próprias contas do Google dizem que os lançamentos precisam ficar muito mais baratos:",
        "menos de duzentos dólares por quilo.", "Ninguém consegue consertar um chip quebrado lá em cima.",
        "E até o líder do projeto diz que não vai ficar mais barato do que na Terra por anos.",
        "Então esse pequeno poema nos diz algo grande.", "Cada pergunta que você faz a uma IA custa energia… e a busca por mais",
        "acabou de sair do planeta.", "Tem uma palavra neste vídeo que eu nunca falei em voz alta.", "Achou?", "Comente.",
        "Siga para mais IA, explicada assim."],
 "hi": ["Google ने अभी-अभी एक AI को अंतरिक्ष में भेजा।", "और उसने सबसे पहले जो जवाब दिया… वह एक कविता थी।",
        "ठीक है, सच कहें तो… उन्होंने कविता माँगी थी।", "लेकिन वह छोटी-सी कविता एक बहुत बड़े आइडिया की शुरुआत है।",
        "एक महीने पहले, SpaceX का एक रॉकेट फ्रिज के आकार का एक सैटेलाइट",
        "ऑर्बिट में ले गया, जिसे Planet नाम की कंपनी के साथ बनाया गया।",
        "अंदर: Google का एक AI चिप, वैसा ही जैसा वह अपने विशाल डेटा सेंटरों में इस्तेमाल करता है,",
        "जिस पर Google का अपना AI मॉडल, Gemma, चलता है।", "यह लगभग हर डेढ़ घंटे में पृथ्वी का एक चक्कर लगाता है,",
        "इसलिए इंजीनियर हर बार ऊपर से गुज़रने पर इसे मैसेज भेजते हैं।", "उनकी पहली माँग?", "अंतरिक्ष पर एक हाइकु।",
        "जवाब दुनिया के सबसे ऊपरी हिस्से के ऊपर से आया:", "ऊपर से पृथ्वी को देखने के बारे में 3 छोटी पंक्तियाँ।",
        "लेकिन इतनी मेहनत क्यों?", "क्योंकि AI भूखा है।",
        "आपको मिलने वाला लगभग हर AI जवाब एक डेटा सेंटर से आता है:",
        "कंप्यूटरों से भरी एक इमारत, जो सब बिजली खाते हैं।",
        "2030 तक, डेटा सेंटर उतनी बिजली इस्तेमाल कर सकते हैं जितनी आज पूरा", "जापान करता है, उससे भी ज़्यादा।",
        "तो Google ने ऊपर देखा।", "सूरज इंसानों की बनाई कुल बिजली से सौ ट्रिलियन गुना ज़्यादा",
        "ऊर्जा देता है।", "यहाँ नीचे, सोलर पैनल रात में रुक जाते हैं,",
        "और बादल रास्ता रोकते हैं।", "लेकिन सही ऑर्बिट में, उस रेखा पर चलते हुए जहाँ दिन और रात मिलते हैं,",
        "सूरज लगभग कभी नहीं डूबता।", "वहाँ ऊपर एक पैनल आठ गुना तक ज़्यादा बिजली बनाता है।",
        "मुफ़्त धूप, हमेशा के लिए।", "परफ़ेक्ट?", "पूरी तरह नहीं।", "चिप बिजली को गर्मी में बदलते हैं।",
        "जानते हैं जब आपका फ़ोन बहुत गर्म हो जाता है और उसे ठंडा होना पड़ता है?",
        "पृथ्वी पर, पंखे और पानी वह गर्मी दूर ले जाते हैं।", "अंतरिक्ष में?", "हवा नहीं।", "आँधी नहीं।", "पानी नहीं।",
        "एक थर्मस के बारे में सोचिए।", "उसकी दीवारों के बीच का खाली गैप आपकी कॉफ़ी को गर्म रखता है।",
        "अंतरिक्ष… एक विशाल थर्मस है।", "वहाँ ऊपर, गर्मी सिर्फ़ अदृश्य रोशनी के रूप में निकल सकती है,",
        "जैसे आग की गर्माहट।", "इसलिए सैटेलाइट में पैनल लगे हैं, जिन्हें रेडिएटर कहते हैं,", "जो उसे चमककर बाहर निकालते हैं।",
        "अभी के लिए, AI छोटे-छोटे दौर में काम करता है… फिर ठंडा होने के लिए आराम करता है।", "फिर आता है रेडिएशन।",
        "छोटे, तेज़ कण एक एक को शून्य में बदल सकते हैं।",
        "AI की सोच के ठीक बीच में एक टाइपो।",
        "तो Google ने अपने चिपों पर कणों की बौछार की, जब वे चला रहे थे", "AI।",
        "वे पाँच साल से ज़्यादा के रेडिएशन में भी बचे रहे।", "बड़ा सपना?",
        "दर्जनों सैटेलाइट, एक-दूसरे से लगभग सौ मीटर दूर उड़ते हुए,", "काम बाँटते हुए और लेज़र से बात करते हुए।",
        "Google कहता है कि उन लेज़रों को निशाना लगाना मीलों दूर से एक सिक्के",
        "को मारने जैसा है… जबकि दोनों चल रहे हों।", "2027 में दो टेस्ट सैटेलाइट ऊपर जाएँगे।",
        "लेकिन सच कहें तो।", "Google के अपने हिसाब से लॉन्च को बहुत सस्ता होना होगा:",
        "दो सौ डॉलर प्रति किलो से कम।", "वहाँ ऊपर कोई टूटा चिप ठीक नहीं कर सकता।",
        "और प्रोजेक्ट के लीडर भी कहते हैं कि यह सालों तक पृथ्वी से सस्ता नहीं होगा।",
        "तो वह छोटी-सी कविता हमें कुछ बड़ा बताती है।", "AI से पूछा गया हर सवाल बिजली खर्च करता है… और ज़्यादा बिजली की तलाश",
        "अब धरती से बाहर निकल गई है।", "इस वीडियो में एक शब्द है जो मैंने कभी ज़ोर से नहीं कहा।", "देखा?",
        "कमेंट में लिखिए।", "ऐसे ही समझाए गए AI के लिए फ़ॉलो करें।"],
 "id": ["Google baru saja meluncurkan AI ke luar angkasa.", "Dan hal pertama yang ia jawab… adalah sebuah puisi.",
        "Oke, jujur saja… mereka memang memintanya.", "Tapi puisi kecil itu adalah awal dari ide yang sangat besar.",
        "Sebulan lalu, roket SpaceX membawa satelit seukuran kulkas",
        "ke orbit, dibuat bersama perusahaan bernama Planet.",
        "Di dalamnya: chip AI Google, jenis yang dipakai di pusat data raksasanya,",
        "menjalankan model AI milik Google sendiri, Gemma.", "Ia mengelilingi Bumi kira-kira setiap satu setengah jam,",
        "jadi para insinyur mengirim pesan setiap kali ia lewat di atas.", "Permintaan pertama mereka?", "Sebuah haiku tentang luar angkasa.",
        "Jawabannya turun di atas puncak dunia:", "3 baris pendek tentang memandang Bumi dari atas.",
        "Tapi kenapa repot-repot begini?", "Karena AI itu lapar.",
        "Hampir setiap jawaban AI yang kamu dapat berasal dari pusat data:",
        "gedung penuh komputer, semuanya memakan listrik.",
        "Pada 2030, pusat data bisa memakai listrik lebih banyak daripada seluruh", "Jepang saat ini.",
        "Jadi Google melihat ke atas.", "Matahari menghasilkan energi seratus triliun kali lebih banyak daripada semua",
        "listrik yang dibuat manusia.", "Di bawah sini, panel surya berhenti di malam hari,",
        "dan awan menghalangi.", "Tapi di orbit yang tepat, menyusuri garis tempat siang bertemu malam,",
        "matahari hampir tidak pernah terbenam.", "Panel di atas sana menghasilkan listrik hingga delapan kali lebih banyak.",
        "Sinar matahari gratis, selamanya.", "Sempurna?", "Tidak juga.", "Chip mengubah listrik menjadi panas.",
        "Kamu tahu saat ponselmu terlalu panas dan harus didinginkan dulu?",
        "Di Bumi, kipas dan air membawa panas itu pergi.", "Di luar angkasa?", "Tak ada udara.", "Tak ada angin.", "Tak ada air.",
        "Bayangkan termos.", "Celah kosong di antara dindingnya menjaga kopimu tetap panas.",
        "Luar angkasa… adalah satu termos raksasa.", "Di atas sana, panas hanya bisa keluar sebagai cahaya tak terlihat,",
        "seperti hangatnya api unggun.", "Jadi satelit membawa panel, yang disebut radiator,", "untuk memancarkannya keluar.",
        "Untuk saat ini, AI bekerja dalam waktu singkat… lalu istirahat untuk mendingin.", "Lalu ada radiasi.",
        "Partikel kecil dan cepat bisa mengubah angka satu menjadi nol.",
        "Salah ketik, tepat di tengah pemikiran AI.",
        "Jadi Google menembakkan berkas partikel ke chipnya saat chip itu menjalankan", "AI.",
        "Chip itu bertahan dari radiasi setara lebih dari lima tahun.", "Mimpi besarnya?",
        "Puluhan satelit, terbang sekitar seratus meter satu sama lain,", "berbagi pekerjaan dan berbicara lewat laser.",
        "Google bilang mengarahkan laser itu seperti mengenai koin dari jarak bermil-mil",
        "jauhnya… sambil keduanya bergerak.", "Dua satelit uji akan naik pada 2027.",
        "Tapi mari jujur.", "Hitungan Google sendiri bilang biaya peluncuran harus jauh lebih murah:",
        "di bawah dua ratus dolar per kilo.", "Tak ada yang bisa memperbaiki chip rusak di atas sana.",
        "Dan bahkan pemimpin proyeknya bilang ini tak akan lebih murah daripada di Bumi selama bertahun-tahun.",
        "Jadi puisi kecil itu memberi tahu kita sesuatu yang besar.", "Setiap pertanyaan yang kamu ajukan ke AI butuh listrik… dan pencarian akan lebih banyak",
        "baru saja meninggalkan planet ini.", "Ada satu kata di video ini yang tidak pernah kuucapkan.", "Sudah lihat?",
        "Tulis di komentar.", "Ikuti untuk AI lainnya, dijelaskan seperti ini."],
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
    assert len(texts) == 70, (lang, len(texts))
    write(f"short15-captions.{lang}.srt", texts)
print("wrote", ", ".join(TR))
