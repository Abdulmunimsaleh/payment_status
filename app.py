from fastapi import FastAPI, HTTPException, Query
import os

app = FastAPI()

# Define the path to the text file
DATA_FILE = "payment_status.txt"

# Function to read the content of the file
def read_payment_status():
    if not os.path.exists(DATA_FILE):
        raise HTTPException(status_code=404, detail="Data file not found")
    
    with open(DATA_FILE, "r") as file:
        content = file.read().strip()
        return content

# Function to update the content of the file
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
        # Check if the user has paid
        if user_input.lower() == "yes":
            status = read_payment_status()
            
            # If the file says the user has paid
            if status.lower() == "success you have paid":
                return {"message": "Payment successful. Thank you!"}
            else:
                return {"message": "Your payment is pending. Please wait for confirmation."}
        
        # If the user hasn't paid
        elif user_input.lower() == "no":
            payment_link = "https://paymenttour1.netlify.app/?user_id={contact_uuid}"  # Replace with your actual payment link
            return {"message": "You haven't paid yet.", "payment_link": payment_link}
        
        # Invalid input
        else:
            raise HTTPException(status_code=400, detail="Invalid input. Please enter 'yes' or 'no'.")
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading data: {str(e)}")

# Optional: Endpoint to update the payment status (for demonstration purposes)
@app.post("/update-payment-status/")
async def update_payment_status_endpoint(new_status: str):
    try:
        update_payment_status(new_status)
        return {"message": "Payment status updated successfully", "new_status": new_status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating data: {str(e)}")