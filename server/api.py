from fastapi import FastAPI, HTTPException
from typing import List
import pandas as pd

app = FastAPI()

def read_csv(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV file not found")

@app.get("/", response_model=List[dict])
async def get_historical_data():
    data = read_csv("data.csv")
    last_20_records = data.tail(20).to_dict(orient='records')
    return last_20_records

@app.get('*', include_in_schema=False)
async def not_found():
    raise HTTPException(status_code=404, detail="Not Found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
