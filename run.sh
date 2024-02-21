if test -d ./venv; then
    echo "Venv is already created, running script..."
else 
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
    if [ "$(uname)" == "Darwin" ]; then
        source venv/bin/activate
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        source venv/bin/activate
    elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
        venv\Scripts\activate
    fi

echo "Installing requirements..."
pip install -q -r requirements.txt
echo "Requirements installed!"
python main.py
