cd "$(dirname "$0")"
R=work/raw
G=$R/ScreenRecording_10-22-2026_01-50-21_1_3.mp4
Q=$R/ScreenRecording_10-22-2026_01-52-59_1_2.mp4
D=$R/ScreenRecording_10-22-2026_01-57-27_1_3.mp4
M=$R/ScreenRecording_10-22-2026_02-00-45_1_3.mp4
N=$R/db6b216e-ScreenRecording_10-22-2026_02-03-16_1.mp4
python3 stitch_page.py $G 0 20.5 345 2580 work/pages/gh_readme.png > work/pages/gh_readme.log 2>&1 &
python3 stitch_page.py $G 33 84 345 2580 work/pages/gh_lean.png --xlock > work/pages/gh_lean.log 2>&1 &
python3 stitch_page.py $G 90 100.7 345 2580 work/pages/gh_files.png > work/pages/gh_files.log 2>&1 &
wait
python3 stitch_page.py $Q 0 68 345 2600 work/pages/quanta_a.png > work/pages/quanta_a.log 2>&1 &
python3 stitch_page.py $Q 96 121.1 345 2600 work/pages/quanta_b.png > work/pages/quanta_b.log 2>&1 &
python3 stitch_page.py $D 0 35.6 170 2600 work/pages/decoder.png > work/pages/decoder.log 2>&1 &
wait
python3 stitch_page.py $M 0 45 170 2600 work/pages/clay_mill.png > work/pages/clay_mill.log 2>&1 &
python3 stitch_page.py $N 0 10 170 2480 work/pages/clay_ns.png > work/pages/clay_ns.log 2>&1 &
python3 stitch_page.py $N 10.5 27.9 170 2480 work/pages/clay_rules.png > work/pages/clay_rules.log 2>&1 &
wait
echo ALLDONE
