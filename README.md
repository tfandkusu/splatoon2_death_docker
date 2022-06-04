# splatoon2_death_docker

スプラトゥーン2のプレイ動画から、やられる直前15秒の動画を作成するDockerイメージ

# 使い方

```sh
git clone git@github.com:tfandkusu/splatoon2_death_docker.git
cd splatoon2_death_docker
```

Appleシリコンをお使いの場合は[aarch64ブランチ](https://github.com/tfandkusu/splatoon2_death_docker/pull/8)をチェックアウトします。

```sh
docker compose build
```

```sh
mkdir src
```

srcディレクトリにスプラトゥーン2の録画をコピーする。

```sh
docker compose run --rm main poetry run python main.py src/<動画ファイル名>
```

extractディレクトリにやられる直前15秒の動画一覧が出力されます。


# Appleシリコン向け

現在、対応中です。
