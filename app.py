import streamlit as st
import requests
import os

st.set_page_config(page_title="Gemini HR Agent", page_icon="🤖")

st.title("AI Агент: Генератор приказов")
st.info("Использует Gemini 1.5 Flash для анализа текста")

user_input = st.text_area("Введите запрос (например: 'Отправь Иванова в Париж на неделю с 1 мая для переговоров'):")

if st.button("Создать документ"):
    if user_input:
        with st.spinner('Gemini анализирует текст...'):
            try:
                response = requests.post("http://127.0.0.1:8000/generate-memo", json={"text": user_input})
                if response.status_code == 200:
                    result = response.json()
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.success("Данные извлечены!")
                        st.json(result["data"])
                    
                    with col2:
                        st.success("Файл готов!")
                        file_path = result["file_name"]
                        with open(file_path, "rb") as f:
                            st.download_button(
                                label="📥 Скачать .docx",
                                data=f,
                                file_name=file_path,
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                else:
                    st.error("Ошибка API")
            except Exception as e:
                st.error(f"Ошибка связи с сервером: {e}")