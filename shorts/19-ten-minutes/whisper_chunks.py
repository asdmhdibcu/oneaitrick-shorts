# Transcribe the take in ~12-25 s chunks with Whisper base.en (sherpa-onnx; model from the k2-fsa GitHub release
# asr-models/sherpa-onnx-whisper-base.en, kept in /root/models, not in git). Checks the take against the script and
# gives align_by_chunks.py its chunk texts. Usage: python3 whisper_chunks.py work/voice16k.wav > work/whisper_chunks.txt
import sys, numpy as np, scipy.io.wavfile as w, sherpa_onnx, subprocess, re
wav=sys.argv[1]; M='/root/models/sherpa-onnx-whisper-base.en/'
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=M+'base.en-encoder.int8.onnx',decoder=M+'base.en-decoder.int8.onnx',tokens=M+'base.en-tokens.txt',language='en',task='transcribe',num_threads=2)
sr,x=w.read(wav); x=x.astype(np.float32)/32768
out=subprocess.run(['ffmpeg','-hide_banner','-i',wav,'-af','silencedetect=noise=-40dB:d=0.25','-f','null','-'],capture_output=True,text=True).stderr
sil=[(float(a)+float(b))/2 for a,b in zip(re.findall(r'silence_start: ([\d.]+)',out),re.findall(r'silence_end: ([\d.]+)',out))]
cuts=[0.0]; dur=len(x)/sr
for s in sil:
    if s-cuts[-1]>12: cuts.append(s)
cuts.append(dur)
for a,b in zip(cuts,cuts[1:]):
    st=rec.create_stream(); st.accept_waveform(sr,x[int(a*sr):int(b*sr)]); rec.decode_stream(st)
    print(f'[{a:6.1f}-{b:6.1f}] {st.result.text.strip()}', flush=True)
