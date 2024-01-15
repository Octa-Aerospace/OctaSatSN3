from fastapi import FastAPI, HTTPException
from typing import List
import csv

app = FastAPI()

def read_csv(file_path):
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            data = list(csv_reader)
            return data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV file not found")

@app.get("/", response_model=List[dict])
async def get_historical_data():
    data = read_csv("data.csv")
    last_20_records = data[-20:]  # Get the last 20 records
    return last_20_records

@app.get('*', include_in_schema=False)
async def not_found():
    raise HTTPException(status_code=404, detail="Not Found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
