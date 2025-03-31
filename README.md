# KeycloakとFlaskによるSAML認証基盤構築

<p align="center">
  <img src="source/saml.gif" alt="animated">
</p>

![Git](https://img.shields.io/badge/GIT-E44C30?logo=git&logoColor=white)
![gitignore](https://img.shields.io/badge/gitignore%20io-204ECF?logo=gitignoredotio&logoColor=white)
![HTML](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
[![Python](https://img.shields.io/badge/Python-3.10-blue.svg?logo=python&logoColor=blue)](https://www.python.org/)
![Flask](https://img.shields.io/badge/flask-%23000.svg?logo=flask&logoColor=white)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-v3-blue.svg)](https://docs.docker.com/compose/)
![Commit Msg](https://img.shields.io/badge/Commit%20message-Eg-brightgreen.svg)
![Code Cmnt](https://img.shields.io/badge/code%20comment-Ja-brightgreen.svg)

## 概要
このプロジェクトは、Docker Composeを使用して、KeycloakとFlaskアプリケーションを統合し、SAML認証を実装する練習環境を構築するためのものです。Keycloakは、オープンソースのアイデンティティ管理ソリューションであり、SAML 2.0に対応した認証機能を提供します。Flaskアプリケーションは、サービスプロバイダー（SP）としてSAML認証を利用し、Keycloakをアイデンティティプロバイダー（IdP）として使用します。

この構成を通じて、SAML認証フローの理解と実装方法を学ぶことができます。Docker Composeを活用することで、複雑な環境を簡単に立ち上げ、効率的に学習・開発を行うことができます。

主な構成は以下の通りです：
+ IdP（Identity Provider）: Keycloak
+ SP（Service Provider）: Flaskアプリケーション
+ プロトコル: SAML 2.0


## SAMLとSSOの基本概念とその関係
### 1. SAML (Security Assertion Markup Language)とは？
SAMLは、Webベースのシングルサインオン（SSO）を実現するためのXMLベースのオープン標準です。主に企業や組織の内部システムで使用され、複数の異なるドメインでの認証を安全に管理するための方法として利用されます。

SAMLでは、認証情報（ユーザーがシステムにログインした証拠）を、安全に交換するための標準形式である「アサーション」を用います。SAML認証フローは、通常、以下の2つの重要な役割を持つシステムに関与します：

+ アイデンティティプロバイダー（IdP）: ユーザーを認証し、認証情報を生成するシステム。
+ サービスプロバイダー（SP）: ユーザーにサービスを提供するシステム。認証されたユーザーだけがアクセスできるリソースを提供します。

SAML認証フローでは、ユーザーがサービスプロバイダーにアクセスしようとすると、認証要求がアイデンティティプロバイダーにリダイレクトされ、認証後にユーザーの認証情報がサービスプロバイダーに戻され、ユーザーにサービスを提供する流れです。

### 2. SSO (Single Sign-On)とは？
SSOは、ユーザーが一度のログインで、複数の異なるアプリケーションやサービスにアクセスできる認証システムです。SSOを使用することで、ユーザーは各サービスごとに再度ログインする必要がなくなります。

SSOのメリットには以下が含まれます：
+ 利便性の向上: 一度ログインするだけで複数のサービスにアクセスでき、ユーザー体験が向上します。
+ セキュリティの強化: パスワードの管理が一元化され、複数のサービスで同じパスワードを使い回すリスクが減ります。
+ 管理の簡素化: 組織のIT部門にとって、ユーザーのアクセス管理が効率化されます。

SAMLは、SSOを実現するための代表的な技術であり、アイデンティティプロバイダー（IdP）とサービスプロバイダー（SP）間で認証情報を交換するためのフレームワークを提供します。これにより、ユーザーは一度ログインすることで、複数のサービスにアクセスできるようになります。

### 3. SAMLとSSOの関係
SAMLは、SSOの実現手段の一つです。具体的には、SAMLを使用して、異なるドメイン間で安全に認証情報を交換し、ユーザーが一度のログインで複数のシステムにアクセスできるようにすることが可能です。

SAMLを用いたSSOでは、ユーザーが一度ログインすれば、次回以降は再度ログインすることなく、複数のアプリケーションやサービスにシームレスにアクセスすることができます。

## 起動方法と動作確認

このセクションでは、Keycloak の設定手順とクライアントの作成からユーザー管理までの流れを解説します。

### 1. コンテナの起動
まず、プロジェクトディレクトリに移動し、以下のコマンドでコンテナを起動します：

```
docker compose up
```

これにより、Keycloakのコンテナがバックグラウンドで起動します。コンテナが起動するのを待ってから、次のステップに進んでください。

### 2. Keycloak の設定手順
管理コンソールへアクセス
ブラウザで以下の URL にアクセスします。

```
http://localhost:8080/admin/
```

ここで、管理者アカウント「admin」と「admin」を使用してログインします。

### 3. 新しい Realm の作成
Keycloak の管理画面で、認証の単位となる「Realm」を作成します。以下の手順で作成します：
+ 「Realm」の管理画面で、「Add realm」をクリックします。
+ 「Realm Name」に myrealm という名前を設定し、「Create」をクリックします。

### 4. クライアントの作成
次に、Keycloak に新しいクライアントを追加します。
+ 「Clients」メニューに移動し、「Create」ボタンをクリックします。
+ クライアント ID に flask-app を設定し、「Save」をクリックします。

### 5. クライアントの設定
クライアント詳細設定画面で、以下の設定を行います：
```
Root URL: http://localhost:8000/
Redirect URI: http://localhost:8000/acs
Web Origin: http://localhost:8000
Authorization Services Enabled: true
Allow direct access grants: true
Standard Flow Enabled: true
Implicit Flow Enabled: false
Front-channel Logout: true
Back-channel Logout: false

Client Authenticator Type: client-secret
SAML Assertion Signature: true
SAML Server Signature: true
SAML Signature Algorithm: RSA_SHA256
SAML Client Signature: true
```

設定後、「Save」をクリックして変更を保存します。

### 6. ユーザーの作成
次に、Keycloak で新しいユーザーを作成します：
+ 左側の「Users」タブをクリックし、「Add user」ボタンをクリックします。
+ ユーザー情報を入力し、「Save」をクリックします。
+ ユーザー詳細ページで「Credentials」タブを開き、パスワードを設定します。
+ 「Temporary」を OFF に設定して、ユーザーが初回ログイン時にパスワード変更を求められないようにします。

### 7. 動作確認
すべての設定が完了したら、ブラウザで以下の URL にアクセスし、ログインを確認します。

```
http://localhost
```
ここで、設定したクライアントに対してシングルサインオンが正常に機能しているかを確認できます。
