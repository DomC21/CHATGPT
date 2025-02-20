from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.services.stock_analysis import analyze_stock

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://stocks.carfagnoenterprises.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.get("/healthz")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/api/stock/analysis/{ticker}")
async def stock_analysis(ticker: str):
    """Get comprehensive stock analysis"""
    try:
        result = await analyze_stock(ticker)
        if not result:
            raise HTTPException(status_code=404, detail="Analysis failed")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
