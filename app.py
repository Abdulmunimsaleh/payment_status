from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

# Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change for security in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the path to the text file
DATA_FILE = "payment_status.txt"

class PaymentStatus(BaseModel):
    new_status: str

# Function to read the payment status from the file
def read_payment_status():
    if not os.path.exists(DATA_FILE):
        return "Payment status not found"
    
    with open(DATA_FILE, "r") as file:
        return file.read().strip()

# Function to update the payment status in the file
def update_payment_status(new_status: str):
    try:
        with open(DATA_FILE, "w") as file:
            file.write(new_status.strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating data: {str(e)}")

# Endpoint to check payment status based on user input
@app.get("/payment-status/")
async def get_payment_status(user_input: str = Query(..., description="Enter 'yes' if you have paid, or 'no' if you haven't")):
    try:
        status = read_payment_status()
        
        if user_input.lower() == "yes":
            if status.lower() == "success you have paid":
                return {"message": "Payment successful. Thank you!"}
            else:
                return {"message": "Your payment is pending. Please wait for confirmation."}
        
        elif user_input.lower() == "no":
            payment_page = "http://127.0.0.1:5500/pay.html"  # Change to actual deployment URL
            return {"message": "You haven't paid yet.", "payment_link": payment_page}
        
        else:
            raise HTTPException(status_code=400, detail="Invalid input. Please enter 'yes' or 'no'.")
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading data: {str(e)}")

# Endpoint to update payment status (triggered by Pay Now button)
@app.post("/update-payment-status/")
async def update_payment_status_endpoint(data: PaymentStatus):
    try:
        update_payment_status(data.new_status)
        return {"message": "Payment status updated successfully", "new_status": data.new_status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating data: {str(e)}")
