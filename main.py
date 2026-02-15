from fastapi import FastAPI, HTTPException
from utils import get_order_data_gemini, create_docx

app = FastAPI()

@app.post("/generate-memo")
async def generate_memo(payload: dict):
    user_input = payload.get("text")
    if not user_input:
        raise HTTPException(status_code=400, detail="Текст не введен")
    
    try: 
        print(f"Запрос к Gemini с текстом: {user_input}")
        data = get_order_data_gemini(user_input)
        print(f"Получены данные от Gemini: {data}")
        file_path = create_docx(data)
        print(f"Файл создан: {file_path}")
        return {
            "status": "success",
            "data": data,
            "file_name": file_path
        }
    except Exception as e:
        import traceback
        print("!!! ПРОИЗОШЛА ОШИБКА !!!")
        print(traceback.format_exc()) 
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)