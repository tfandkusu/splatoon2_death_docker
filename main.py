# %%
# ライブラリインポート
import os
import sys
import subprocess
import csv
import numpy as np
import cv2
import tensorflow as tf
from tqdm import tqdm
# %%
if len(sys.argv) <= 1:
    print("Usege:")
    print("docker-compose run main python3 main.py <mp4_file_path>")
    exit(0)
# 切り出し元動画パス
src_movie = sys.argv[1]
# 切り出し秒数
cut_duration = 15
# 出力ファイル名ベース
basename = os.path.splitext(os.path.basename(src_movie))[0]
# %%
# TensorFlow lite の初期化
interpreter = tf.lite.Interpreter(model_path='model/model.tflite')
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
# %%
# 切り出し終了時間からこの秒数は切り出し開始しない
death_duration = cut_duration
# 書き出しCSVファイル
with open('cut_time.csv', 'w') as f:
    writer = csv.writer(f)
    # 動画を読み込む
    cap = cv2.VideoCapture(src_movie)
    # フレーム数を取得
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # 1秒あたりフレーム数を取得
    fps = cap.get(cv2.CAP_PROP_FPS)
    # 0.5秒に1回予測する
    skip = fps / 2
    # フレーム
    i = 0
    # 切り出し開始しないカウントダウン
    no_start = 0
    # デバッグ出力画像ファイルインデックス
    out_index = 0
    for i in tqdm(range(frame_count)):
        ret, img = cap.read()
        if ret:
            if i % skip == 0 and no_start == 0:
                # フレームを予測する大きさに縮小
                shrink = cv2.resize(
                    img, (224, 224), interpolation=cv2.INTER_CUBIC)
                # 4次元に変換する
                input_tensor = shrink.reshape(1, 224, 224, 3)
                # それをTensorFlow liteに指定する
                interpreter.set_tensor(input_details[0]['index'], input_tensor)
                # 推論実行
                interpreter.invoke()
                # 出力層を確認
                output_tensor = interpreter.get_tensor(
                    output_details[0]['index'])
                # やられたシーン判定
                scene = np.argmax(output_tensor)
                if scene == 1:
                    # やられたシーンの時は
                    # 切り出し開始秒数を出力
                    ss = i - cut_duration * fps
                    if ss < 0:
                        ss = 0
                    writer.writerow(
                        ["%d.%02d" % (ss/fps, 100 * (ss % fps)/fps)])
                    # シーン判定をしばらく止める
                    no_start = fps * death_duration
            if no_start >= 1:
                no_start -= 1
        else:
            break
# %%
# CSVファイルから切り出し開始時刻配列を作成する
sss = []
with open('cut_time.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        sss.append(row[0])
# %%
# ffmpegで切り出す
for i in tqdm(range(len(sss))):
    ss = sss[i]
    command = "ffmpeg -y -ss %s -i %s -t %d -c:v libx264 -acodec aac -strict experimental -r 30 -b:v 3000k -b:a 320k extract/%s_%03d.mp4" % (
        ss, src_movie, cut_duration, basename, i)
    subprocess.run(command, shell=True)
