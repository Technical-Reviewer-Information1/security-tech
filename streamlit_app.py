import streamlit as st
import time

st.title("体験してわかる！ネットワークセキュリティの仕組み")

st.caption("Created by Dit-Lab.(Daiki ITO)")
st.caption("Supported by Tomoaki ATSUMI")

st.write("「フィルタリング」「ファイアウォール」「VLAN」...。言葉は聞くけど、実際にはどう動いているんだろう？ここでは、代表的な3つのセキュリティ技術を、キミの操作で動かしながら体験してみよう！")

# フィルタリングの仕組み
with st.expander("体験1：フィルタリングの仕組み 🛡️"):
    st.write("**シナリオ**: 学校のコンピュータ室で、アクセスできるWebサイトを制限しよう！方法は2つあるよ。")
    
    # サイト選択
    selected_site = st.selectbox(
        "アクセスしたいサイトを選択:",
        ["WebサイトA (学習系)", "WebサイトB (ゲーム系)", "WebサイトC (ニュース系)", "WebサイトD (SNS系)"]
    )
    
    # フィルタリング方式のタブ
    tab1, tab2 = st.tabs(["ホワイトリスト方式", "ブラックリスト方式"])
    
    with tab1:
        st.write("**許可リスト**: [WebサイトA (学習系), WebサイトC (ニュース系)]")
        st.write("このリストにあるサイトだけにアクセスを許可します。")
        
        if selected_site in ["WebサイトA (学習系)", "WebサイトC (ニュース系)"]:
            st.success("✅ アクセスが許可されました！")
        else:
            st.error("❌ このサイトは許可リストにありません。")
    
    with tab2:
        st.write("**禁止リスト**: [WebサイトB (ゲーム系), WebサイトD (SNS系)]")
        st.write("このリストにあるサイトだけへのアクセスを禁止します。")
        
        if selected_site in ["WebサイトB (ゲーム系)", "WebサイトD (SNS系)"]:
            st.error("❌ このサイトは禁止リストに含まれています。")
        else:
            st.success("✅ アクセスが許可されました！")

# ファイアウォールの仕組み
with st.expander("体験2：ファイアウォールの仕組み 🔥🧱"):
    st.write("**シナリオ**: 会社のネットワークを、インターネットからの不正な侵入から守ろう！ファイアウォールが門番として通信をチェックする様子を見てみよう。")
    
    # ネットワーク図の表現
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### インターネット 🌐")
        st.write("外部からの通信")
    with col2:
        st.markdown("### ファイアウォール 🧱")
        st.write("門番として通信を判断")
    with col3:
        st.markdown("### 内部ネットワーク 💻")
        st.write("会社の安全なネットワーク")
    
    st.write("**ファイアウォールのルール**:")
    st.write("- 許可する通信: Webサイト閲覧(HTTP), メール(SMTP)")
    st.write("- それ以外はすべて禁止")
    
    # 通信の選択
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Webサイトを閲覧する"):
            st.success("✅ [許可] Webサイト閲覧(HTTP)は許可された通信です。")
    
    with col2:
        if st.button("メールを受信する"):
            st.success("✅ [許可] メール(SMTP)は許可された通信です。")
    
    with col3:
        if st.button("不正なスキャン攻撃を試みる"):
            st.error("❌ [拒否] ルールにない不正な通信のためブロックしました！")

# VLANの仕組み
with st.expander("体験3：VLANの仕組み 🏢"):
    st.write("**シナリオ**: 1つのフロアに「営業部」と「開発部」がある会社を考えてみよう。部署が違う人に、関係ない情報が届かないようにするにはどうすればいい？")
    
    # VLAN設定のトグル
    vlan_enabled = st.toggle("VLANを有効にする", key="vlan_toggle")
    
    if not vlan_enabled:
        st.markdown("### VLANなしの状態")
        st.write("1つのスイッチに営業部PC2台と開発部PC2台が接続されています。")
        
        # PC図の表現（簡易版）
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**営業部PC**")
            st.write("📱 PC1")
            st.write("📱 PC2")
        with col2:
            st.markdown("**開発部PC**")
            st.write("💻 PC1")
            st.write("💻 PC2")
        
        if st.button("営業部のPCから全員にお知らせを一斉送信！", key="no_vlan_send"):
            st.warning("⚠️ 全員に届いてしまった... 営業部の情報が開発部にも漏れてしまいました。")
            
    else:
        st.markdown("### VLANありの状態")
        st.write("VLANで営業部(VLAN10)と開発部(VLAN20)のグループに分けました。")
        
        # PC図の表現（色分け版）
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**営業部PC (VLAN10)** 🔵")
            st.markdown("🔵 PC1")
            st.markdown("🔵 PC2")
        with col2:
            st.markdown("**開発部PC (VLAN20)** 🟢")
            st.markdown("🟢 PC1")
            st.markdown("🟢 PC2")
        
        if st.button("営業部のPCから部署内にお知らせを一斉送信！", key="vlan_send"):
            st.success("✅ 営業部内にだけ、きちんと情報が伝わった！VLANによってセキュアに通信できました。")

st.markdown("---")
st.write("各技術を実際に操作してみることで、どのようにネットワークセキュリティが守られているかを体験できたでしょうか？")
st.write("これらの技術は実際の企業や学校のネットワークで使われている重要な仕組みです。")