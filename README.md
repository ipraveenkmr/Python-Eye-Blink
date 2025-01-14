1. Create virtual env
python -m venv env


2. activate virtual env
env\Scripts\activate


3. Install from requirements.txt
pip install -r requirements.txt


4. Run command
python eyeblink.py


5. To Freeze env requirements.txt file
pip freeze > requirements.txt


6. To Create exe File
pyinstaller --onefile --windowed --add-data="assets/icons;icons" your_script.py
pyinstaller --onefile --windowed  eyeblink.py



