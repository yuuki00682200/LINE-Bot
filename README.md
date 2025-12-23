# LINE Bot Framework

このプロジェクトは、PythonベースのLINE Bot開発フレームワークです。
大規模なリファクタリングにより、ディレクトリ構成が整理され、拡張性と保守性が向上しました。単一のエントリーポイント (`main.py`) を使用して、異なる種類のボット（SelfBot, ProtectBotなど）を簡単に起動・管理できます。

## ディレクトリ構成

プロジェクトは以下のような構成になっています。

```text
.
├── main.py                 # 統合エントリーポイント（ここから起動します）
├── requirements.txt        # 依存ライブラリ一覧
├── certs/                  # ログイン認証用ファイル (*.crt, *.session)
├── data/                   # 設定ファイルやボットデータ (*.json)
└── src/
    └── linebot/
        ├── core/           # LINE APIとの通信を行うコアロジック
        ├── bots/           # 各ボットの実装ディレクトリ
        │   ├── self_bot/   # SelfBot (多機能ボット)
        │   ├── auto_login/ # 自動ログイン用ボット
        │   ├── protect/    # ProtectBot
        │   └── pub_protect/# Public ProtectBot
        ├── generated/      # Thriftから生成されたAPI定義コード
        └── utils/          # データベース、暗号化、メールなどのユーティリティ
```

## インストール

1. **Pythonの準備**: Python 3.x が必要です。
2. **依存ライブラリのインストール**:

```bash
pip install -r requirements.txt
```

※ 一部のライブラリ（`thrift` など）がプロジェクト内に同梱されている場合や、特定のバージョンが必要な場合があります。環境に合わせて調整してください。

## 使い方

すべてのボットは `main.py` を通じて起動します。

### ヘルプの表示

利用可能なコマンドやオプションを確認できます。

```bash
python3 main.py --help
```

### 1. SelfBot の起動

個人のLINEアカウントで動作する多機能ボットです。

```bash
python3 main.py selfbot <MID> --token <YOUR_AUTH_TOKEN> --password <YOUR_PASSWORD>
```
*   `MID`: 対象のユーザーMID、または設定キー
*   `--token`: LINEの認証トークン
*   `--password`: パスワード

### 2. LoginBot (Auto Login) の起動

自動ログイン処理を行うボットです。

```bash
python3 main.py loginbot --token <YOUR_AUTH_TOKEN> --password <YOUR_PASSWORD>
```

### 3. ProtectBot の起動

特定のグループやユーザーを保護するためのボットです。

```bash
python3 main.py protect <MID>
```

### 4. Public ProtectBot の起動

```bash
python3 main.py pub_protect
```

## 開発者向け情報

*   **新しい機能の追加**: `src/linebot/core` 内のコアロジックを修正するか、`src/linebot/bots` 内に新しいボットパッケージを作成してください。
*   **インポート**: プロジェクト内でのインポートは `from linebot.core.client import LineClient` のように、`linebot` パッケージをルートとして記述してください。
*   **データ管理**: 永続化が必要なデータは `data/` ディレクトリ内のJSONファイルを使用してください。
*   **証明書**: ログインセッションや証明書は `certs/` ディレクトリに保存されます。

## 注意事項

*   このプログラムの使用によって生じたアカウントの凍結や不利益について、開発者は責任を負いません。自己責任で利用してください。
*   `certs/` や `data/` に含まれる個人情報（トークンやパスワードを含むファイル）は、Gitなどのバージョン管理システムにコミットしないよう注意してください（`.gitignore` の設定を推奨）。
