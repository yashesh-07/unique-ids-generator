import os
from fastapi import FastAPI, HTTPException
from app.generator import SnowflakeGenerator

app = FastAPI()

# 1. Configuration from Environment
# We pull these from the docker-compose 'environment' section
MACHINE_ID = int(os.getenv("MACHINE_ID", "0"))
EPOCH = int(os.getenv("EPOCH", "1672531200000"))

# 2. Global Initialization
# We initialize the generator here so it persists across all API calls 
# within this specific container.
generator = SnowflakeGenerator(machine_id=MACHINE_ID, epoch=EPOCH)

@app.get("/generate")
def generate_id():
    """
    The primary endpoint to get a unique, time-ordered ID.
    """
    try:
        # YOUR TASK: 
        # 1. Call the generator's method to get a new ID
        # 2. Return a dictionary containing the ID
        
        new_id = generator.generate_id()
        
        return {
            "id": new_id,
            "id_str": str(new_id),  # Crucial for frontend precision
            "machine_id": MACHINE_ID
        }
    except Exception as e:
        # Handle the Clock Drift exception if it occurs
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """
    Simple check to see if the node is alive and configured correctly.
    """
    return {
        "status": "online",
        "machine_id": MACHINE_ID,
        "current_timestamp": generator._get_timestamp()
    }