import uvicorn
from openswell.app import create_service

if __name__ == "__main__":
    app = create_service()
    uvicorn.run(app, host="127.0.0.1", port="8000")