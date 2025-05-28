import streamlit as st

st.title("第7回 Streamlit総合演習")
st.caption("レイアウト、状態管理、フォーム、ファイルアップロードを学びます。")

st.info("このファイルは第7回Streamlit総合演習の概要とファイル案内です。")

st.markdown("---")

st.header("基本コード例")
st.write("スライドで紹介された各機能の基本コード例は以下のファイルを参照してください。")
st.markdown("- [レイアウト機能](src/lecture07/basic/layout.py)")
st.markdown("- [状態管理](src/lecture07/basic/session_state.py)")
st.markdown("- [フォーム機能](src/lecture07/basic/form.py)")
st.markdown("- [ファイルアップロード機能](src/lecture07/basic/file_uploader.py)")

st.markdown("---")

st.header("演習問題")
st.write("各演習問題のテンプレートと解答例はexercisesフォルダを参照してください。")
st.markdown("- [レイアウト演習](src/lecture07/exercises/section1_layout_template.py), [解答](src/lecture07/exercises/section1_layout_answer.py)")
st.markdown("- [状態管理演習 (ToDoリスト)](src/lecture07/exercises/section2_session_state_template.py), [解答](src/lecture07/exercises/section2_session_state_answer.py)")
st.markdown("- [フォーム演習 (アンケート)](src/lecture07/exercises/section3_form_template.py), [解答](src/lecture07/exercises/section3_form_answer.py)")
st.markdown("- [ファイルアップロード演習](src/lecture07/exercises/section4_file_uploader_template.py), [解答](src/lecture07/exercises/section4_file_uploader_answer.py)")

st.markdown("---")
st.success("各ファイルを開いて内容を確認・編集してください。") 
