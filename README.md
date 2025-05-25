# Weather API Project

# Python 3.9.13

# How to Run

1. Download and unzip the project folder (weather-api.zip)

2. Open a terminal and navigate into the project directory:

 cd weather-api (-->bash)


3. Create and activate a virtual environment:

 python -m venv venv
 activate on Windows
 venv\Scripts\activate
 activate on macOS/Linux
 source venv/bin/activate


4. Install dependencies:

 pip install -r requirements.txt


5. Set environment variables in .env file:

 MY_USERNAME=repathsolutions_palaskas_giorgos
 PASSWORD=50TUH8hrr3
 #username and password are valid until 7-June-2025


6. Run the data fetcher to populate the database:

 python fetch_data.py


7. Start the FastAPI server:

 uvicorn main:app --reload


8. Then open your browser at:
 
 http://127.0.0.1:8000/docs

 or testis live at:

 https://weather-api-nk0x.onrender.com/docs