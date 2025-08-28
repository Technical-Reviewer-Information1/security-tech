import streamlit as st
import time

st.title("体験してわかる！ネットワークセキュリティの仕組み")

st.caption("Created by Dit-Lab.(Daiki ITO)")
st.caption("Supported by Tomoaki ATSUMI")

st.markdown("""
「フィルタリング」「ファイアウォール」「VLAN」...。言葉は聞くけど、実際にはどう動いているんだろう？  
ここでは、代表的な3つのセキュリティ技術を、キミの操作で動かしながら体験してみよう！
""")

# セクション選択
section = st.radio(
    "学びたいセキュリティ技術を選んでね！",
    ["フィルタリング 🛡️", "ファイアウォール 🔥", "VLAN 🏢"],
    horizontal=True
)

st.markdown("---")

# フィルタリングの仕組み
if section == "フィルタリング 🛡️":
    st.header("体験1：フィルタリングの仕組み 🛡️")
    
    st.markdown("""
    **シナリオ**: 学校のコンピュータ室で、アクセスできるWebサイトを制限しよう！  
    方法は2つあるよ。どちらが安全だと思う？
    """)
    
    # ユーザー設定エリア
    st.subheader("⚙️ あなたがネットワーク管理者です")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**👤 ユーザーの行動**")
        selected_site = st.selectbox(
            "アクセスしたいサイトを選択:",
            ["WebサイトA (学習系)", "WebサイトB (ゲーム系)", "WebサイトC (ニュース系)", "WebサイトD (SNS系)"]
        )
        
        # アクセス試行ボタン
        if st.button("🌐 このサイトにアクセスしてみる", type="primary"):
            st.session_state.access_attempt = True
        else:
            st.session_state.access_attempt = False
    
    with col2:
        st.markdown("**🛡️ フィルタリング設定**")
        filter_method = st.radio(
            "フィルタリング方式を選択:",
            ["ホワイトリスト方式", "ブラックリスト方式"]
        )
        
        if filter_method == "ホワイトリスト方式":
            allowed_sites = st.multiselect(
                "許可するサイトを選択:",
                ["WebサイトA (学習系)", "WebサイトB (ゲーム系)", "WebサイトC (ニュース系)", "WebサイトD (SNS系)"],
                default=["WebサイトA (学習系)", "WebサイトC (ニュース系)"]
            )
        else:
            blocked_sites = st.multiselect(
                "禁止するサイトを選択:",
                ["WebサイトA (学習系)", "WebサイトB (ゲーム系)", "WebサイトC (ニュース系)", "WebサイトD (SNS系)"],
                default=["WebサイトB (ゲーム系)", "WebサイトD (SNS系)"]
            )
    
    # 判定結果
    if st.session_state.get('access_attempt', False):
        st.markdown("### 📊 アクセス判定結果")
        
        if filter_method == "ホワイトリスト方式":
            if selected_site in allowed_sites:
                st.success(f"✅ **許可**: {selected_site}は許可リストに含まれています。アクセスを許可します。")
                st.balloons()
            else:
                st.error(f"❌ **拒否**: {selected_site}は許可リストにありません。アクセスを拒否します。")
        else:
            if selected_site in blocked_sites:
                st.error(f"❌ **拒否**: {selected_site}は禁止リストに含まれています。アクセスを拒否します。")
            else:
                st.success(f"✅ **許可**: {selected_site}は禁止リストにありません。アクセスを許可します。")
                st.balloons()
        
        # 解説
        st.markdown("### 💡 どちらが安全？")
        if filter_method == "ホワイトリスト方式":
            st.info("**ホワイトリスト方式**は「明確に許可されたもの以外はすべて拒否」という考え方。より安全性が高いとされています。")
        else:
            st.warning("**ブラックリスト方式**は「明確に禁止されたもの以外はすべて許可」という考え方。新しい危険サイトには対応が遅れる可能性があります。")

# ファイアウォールの仕組み
elif section == "ファイアウォール 🔥":
    st.header("体験2：ファイアウォールの仕組み 🔥")
    
    st.markdown("""
    **シナリオ**: あなたは会社のネットワーク管理者です。  
    ファイアウォールのルールを設定して、安全な通信だけを通しましょう！
    """)
    
    # ネットワーク図
    st.subheader("🌐 ネットワーク構成")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background-color: #ffebee; border-radius: 10px; margin: 10px;'>
        <h3>🌐 インターネット</h3>
        <p>外部からの通信</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background-color: #fff3e0; border-radius: 10px; margin: 10px;'>
        <h3>🧱 ファイアウォール</h3>
        <p>門番として通信を判断</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background-color: #e8f5e8; border-radius: 10px; margin: 10px;'>
        <h3>💻 内部ネットワーク</h3>
        <p>会社の安全なネットワーク</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### ⚙️ ファイアウォール設定")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📋 通信ルール設定**")
        allow_http = st.checkbox("HTTP (Webサイト閲覧)", value=True)
        allow_https = st.checkbox("HTTPS (暗号化Web通信)", value=True)
        allow_smtp = st.checkbox("SMTP (メール送信)", value=True)
        allow_ftp = st.checkbox("FTP (ファイル転送)", value=False)
        allow_ssh = st.checkbox("SSH (リモートアクセス)", value=False)
        
        st.markdown("**🚨 セキュリティレベル**")
        security_level = st.slider("セキュリティの厳しさ", 1, 5, 3)
        
    with col2:
        st.markdown("**🎯 通信を試してみる**")
        communication_type = st.selectbox(
            "どんな通信を試す？",
            ["HTTP (Webサイト閲覧)", "HTTPS (暗号化Web通信)", "SMTP (メール送信)", 
             "FTP (ファイル転送)", "SSH (リモートアクセス)", "不正なポートスキャン", "マルウェア通信"]
        )
        
        source_ip = st.text_input("送信元IPアドレス", "192.168.1.100")
        dest_port = st.number_input("送信先ポート番号", 1, 65535, 80)
        
        if st.button("🚀 通信を送信", type="primary"):
            st.session_state.firewall_test = True
    
    # ファイアウォール判定
    if st.session_state.get('firewall_test', False):
        st.markdown("### 📊 ファイアウォール判定結果")
        
        # 基本的な判定ロジック
        allowed = False
        reason = ""
        
        if communication_type == "HTTP (Webサイト閲覧)" and allow_http:
            allowed = True
            reason = "HTTP通信が許可設定されています"
        elif communication_type == "HTTPS (暗号化Web通信)" and allow_https:
            allowed = True
            reason = "HTTPS通信が許可設定されています"
        elif communication_type == "SMTP (メール送信)" and allow_smtp:
            allowed = True
            reason = "SMTP通信が許可設定されています"
        elif communication_type == "FTP (ファイル転送)" and allow_ftp:
            allowed = True
            reason = "FTP通信が許可設定されています"
        elif communication_type == "SSH (リモートアクセス)" and allow_ssh:
            allowed = True
            reason = "SSH通信が許可設定されています"
        elif communication_type in ["不正なポートスキャン", "マルウェア通信"]:
            allowed = False
            reason = "不正な通信パターンを検出"
        else:
            allowed = False
            reason = "許可されていない通信タイプです"
        
        # セキュリティレベルによる追加判定
        if security_level >= 4 and "192.168" not in source_ip:
            allowed = False
            reason += " (高セキュリティ設定により外部IPをブロック)"
        
        if allowed:
            st.success(f"✅ **通信許可**: {reason}")
            st.balloons()
        else:
            st.error(f"❌ **通信拒否**: {reason}")
        
        # 詳細情報
        with st.expander("📋 詳細ログ"):
            st.write(f"**通信タイプ**: {communication_type}")
            st.write(f"**送信元IP**: {source_ip}")
            st.write(f"**送信先ポート**: {dest_port}")
            st.write(f"**セキュリティレベル**: {security_level}/5")
            st.write(f"**判定時刻**: {time.strftime('%Y-%m-%d %H:%M:%S')}")

# VLANの仕組み
else:  # section == "VLAN 🏢"
    st.header("体験3：VLANの仕組み 🏢")
    
    st.markdown("""
    **シナリオ**: あなたは会社のネットワーク管理者です。  
    1つのフロアに「営業部」と「開発部」があります。部署間の情報漏洩を防ぎましょう！
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### ⚙️ ネットワーク設定")
        vlan_enabled = st.toggle("VLANを有効にする", key="vlan_toggle")
        
        if vlan_enabled:
            st.success("✅ VLAN機能: 有効")
            st.write("営業部: VLAN 10 🔵")
            st.write("開発部: VLAN 20 🟢")
        else:
            st.warning("⚠️ VLAN機能: 無効")
            st.write("すべてのPCが同一ネットワーク")
        
        st.markdown("### 👥 部署を選択")
        sender_dept = st.radio("送信者の部署:", ["営業部", "開発部"])
        
        st.markdown("### 📝 送信内容")
        message_type = st.selectbox(
            "送信する情報の種類:",
            ["部署内連絡", "全社連絡", "機密情報", "新商品企画書", "顧客リスト"]
        )
        
        message_content = st.text_area("メッセージ内容:", "お疲れさまです。本日の会議資料をお送りします。")
        
    with col2:
        st.markdown("### 🖥️ オフィスレイアウト")
        
        if not vlan_enabled:
            # VLANなしの表示
            st.markdown("""
            <div style='border: 2px solid #ccc; padding: 20px; border-radius: 10px; background-color: #f5f5f5;'>
            <h4 style='text-align: center; margin-bottom: 20px;'>📡 物理スイッチ (VLAN なし)</h4>
            <div style='display: flex; justify-content: space-around;'>
                <div style='text-align: center;'>
                    <h5>営業部</h5>
                    <div>🖥️ PC1</div>
                    <div>🖥️ PC2</div>
                </div>
                <div style='text-align: center;'>
                    <h5>開発部</h5>
                    <div>💻 PC1</div>
                    <div>💻 PC2</div>
                </div>
            </div>
            <p style='text-align: center; color: red; margin-top: 10px;'>⚠️ すべてのPCが同じネットワークに接続</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # VLANありの表示
            st.markdown("""
            <div style='border: 2px solid #4CAF50; padding: 20px; border-radius: 10px; background-color: #f9f9f9;'>
            <h4 style='text-align: center; margin-bottom: 20px;'>📡 VLANスイッチ (VLAN あり)</h4>
            <div style='display: flex; justify-content: space-around;'>
                <div style='text-align: center; background-color: #e3f2fd; padding: 15px; border-radius: 8px; border: 2px solid #2196F3;'>
                    <h5>🔵 営業部 (VLAN 10)</h5>
                    <div>🖥️ PC1</div>
                    <div>🖥️ PC2</div>
                </div>
                <div style='text-align: center; background-color: #e8f5e8; padding: 15px; border-radius: 8px; border: 2px solid #4CAF50;'>
                    <h5>🟢 開発部 (VLAN 20)</h5>
                    <div>💻 PC1</div>
                    <div>💻 PC2</div>
                </div>
            </div>
            <p style='text-align: center; color: green; margin-top: 10px;'>✅ 各部署が論理的に分離</p>
            </div>
            """, unsafe_allow_html=True)
    
    # 送信ボタンと結果
    st.markdown("### 📤 情報送信テスト")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📧 部署内に送信", type="primary"):
            st.session_state.vlan_send_internal = True
    
    with col2:
        if st.button("📢 全部署に送信", type="secondary"):
            st.session_state.vlan_send_all = True
    
    with col3:
        if st.button("🔍 送信状況を確認"):
            st.session_state.vlan_check_status = True
    
    # 送信結果の表示
    if st.session_state.get('vlan_send_internal', False):
        st.markdown("### 📊 送信結果 (部署内)")
        if vlan_enabled:
            st.success(f"✅ {sender_dept}内にのみ「{message_type}」が送信されました！")
            st.info(f"VLANにより、{sender_dept}以外の部署には情報が届きませんでした。")
            st.balloons()
        else:
            st.error(f"❌ 全部署に「{message_type}」が送信されてしまいました...")
            st.warning("VLANが無効のため、部署を限定した送信ができませんでした。")
    
    elif st.session_state.get('vlan_send_all', False):
        st.markdown("### 📊 送信結果 (全部署)")
        if message_type in ["機密情報", "顧客リスト"] and vlan_enabled:
            st.error("❌ 機密情報の全部署送信は管理者により制限されています。")
            st.warning("VLANセキュリティポリシーにより、機密情報は部署間送信が制限されています。")
        else:
            st.success("✅ 全部署に送信されました！")
            if not vlan_enabled:
                st.info("VLANが無効のため、すべての通信が同じネットワークを通ります。")
    
    elif st.session_state.get('vlan_check_status', False):
        st.markdown("### 📋 現在のネットワーク状況")
        
        if vlan_enabled:
            st.success("🔵 **営業部 (VLAN 10)**: 2台のPC - 正常稼働")
            st.success("🟢 **開発部 (VLAN 20)**: 2台のPC - 正常稼働")
            st.info("✅ 各VLANは独立して動作しています。部署間の通信は制御されています。")
        else:
            st.warning("🖥️ **全PC**: 4台すべてが同一ネットワーク")
            st.error("⚠️ 部署間の通信制御ができていません。情報漏洩のリスクがあります。")

st.markdown("---")
st.markdown("""
### 🎓 学習のまとめ
各技術を実際に操作してみることで、どのようにネットワークセキュリティが守られているかを体験できましたか？
これらの技術は実際の企業や学校のネットワークで使われている重要な仕組みです。

- **フィルタリング**: アクセス制御でユーザーを守る
- **ファイアウォール**: 不正な通信をブロックしてネットワークを守る  
- **VLAN**: ネットワークを論理的に分離して情報漏洩を防ぐ
""")