import streamlit as st
from datetime import date
import os
import json
from uuid import uuid4
from streamlit_calendar import calendar

# フォルダ・ファイル定義
MEDIA_DIR = "media"
DATA_FILE = "diary_data.json"
os.makedirs(MEDIA_DIR, exist_ok=True)

# 投稿保存関数
def save_post(entry):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# 既存データのID付与処理
def add_ids_to_existing_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        updated = False
        for entry in data:
            if "id" not in entry:
                entry["id"] = uuid4().hex
                updated = True

        if updated:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        return data
    else:
        return []

# 投稿表示カード
def render_card(entry):
    st.markdown(
        f"""
        <div style="
            background-color: white;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            padding: 20px;
            margin: 20px 0;
        ">
            <h4>📅 {entry['date']}</h4>
            <p style="white-space: pre-wrap;">{entry['text']}</p>
            <p>気分: {entry.get('mood', '')}  タグ: {', '.join(entry.get('tags', []))}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    for media_path in entry.get("media", []):
        if media_path.endswith((".jpg", ".jpeg", ".png")):
            st.image(media_path, use_column_width=True)
        elif media_path.endswith((".mp4", ".mov")):
            st.video(media_path)

    st.markdown("<hr>", unsafe_allow_html=True)

# Streamlit UI設定
st.set_page_config(page_title="日記アプリ", layout="centered")
st.title("📔 My日記")

# 既存投稿にIDを追加（起動時に一度だけ実行）
data = add_ids_to_existing_data()

# 入力フォーム
today = st.date_input("日付", value=date.today())
text = st.text_area("今日の出来事や気持ちを入力してください", height=150)
uploaded_files = st.file_uploader("画像や動画をアップロード", type=["jpg", "jpeg", "png", "mp4", "mov"], accept_multiple_files=True)

# 気分マークとタグ候補
mood_options = ["😄", "😐", "😢", "😠", "🥰"]
tag_options = ["旅行", "カフェ", "猫", "勉強", "趣味", "自然", "ゲーム"]

selected_mood = st.selectbox("今の気分を選んでください", mood_options)
selected_tags = st.multiselect("タグを選んでください（複数可）", tag_options)

# 投稿処理
if st.button("✅ 投稿を保存する"):
    media_paths = []

    for file in uploaded_files:
        ext = os.path.splitext(file.name)[-1]
        unique_filename = f"{uuid4().hex}{ext}"
        save_path = os.path.join(MEDIA_DIR, unique_filename)

        with open(save_path, "wb") as f:
            f.write(file.getbuffer())

        media_paths.append(save_path)

    post_entry = {
        "id": uuid4().hex,
        "date": str(today),
        "text": text,
        "media": media_paths,
        "mood": selected_mood,
        "tags": selected_tags
    }

    save_post(post_entry)
    st.success("✅ 投稿が保存されました！")
    st.experimental_rerun()  # 投稿後にページリロードして投稿一覧更新

st.header("📜 投稿一覧")

# 投稿の再読み込み（最新状態）
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    data = sorted(data, key=lambda x: x["date"], reverse=True)

    # 投稿表示と削除ボタン
    for entry in data:
        render_card(entry)
        if st.button(f"🗑️ 削除する", key=entry["id"]):
            # 削除処理
            data = [d for d in data if d["id"] != entry["id"]]
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            st.success("投稿が削除されました")
            st.experimental_rerun()
else:
    st.info("まだ投稿がありません。最初の日記を投稿してみましょう！")

# サイドバーのフィルター機能（参考）
st.sidebar.header("🔎 フィルター")
selected_date = st.sidebar.date_input("📅 特定の日付で絞り込み", value=None)
search_keyword = st.sidebar.text_input("🔤 キーワード検索")

if (selected_date is not None or search_keyword):  # ←ここを追加
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        data = sorted(data, key=lambda x: x["date"], reverse=True)

        if selected_date:
            data = [d for d in data if d["date"] == str(selected_date)]
        if search_keyword:
            data = [d for d in data if search_keyword.lower() in d["text"].lower()]

        if data:
            st.subheader("📜 フィルター結果")
            for entry in data:
                render_card(entry)
        else:
            st.warning("一致する投稿がありませんでした。")
    else:
        st.info("まだ投稿がありません。")


# ここからカレンダー表示部分

st.subheader("🗓️ カレンダー表示")

# イベントリストを作成  ※キーは "start"
events = [{"title": "📝", "start": entry["date"]} for entry in data]

# オプションは辞書で指定
options = {
    "initialView": "dayGridMonth",
    "locale": "ja"
}

# カレンダーを描画
selected = calendar(events=events, options=options)

# クリックされた日付があれば、その日の投稿を表示
if selected and selected.get("start"):
    clicked_date = selected["start"][:10]  # 'YYYY-MM-DD'
    st.markdown(f"### 📅 {clicked_date} の投稿")
    matched = [d for d in data if d["date"] == clicked_date]
    if matched:
        for e in matched:
            render_card(e)
    else:
        st.info("この日には投稿がありません。")
