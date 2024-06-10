
if ! command -v conda &> /dev/null; then
    echo "Error: Conda is not installed or not in PATH. Please install Conda and try again."
    exit 1
fi

echo "Initializing Conda..."
eval "$(conda shell.bash hook)"
conda activate py3.10


if [[ $? -ne 0 ]]; then
    echo "Error: Failed to activate Conda environment. Please check your Conda installation and environment setup."
    exit 1
fi

echo "Navigating to the directory..."

cd "/home/radionnazmiev/DS/moscow_flat_pricing_predictor/back-end/" || {
    echo "Error: Failed to navigate to the directory. Please check the path and try again."
    exit 1
}

echo "Starting Python server..."
python server.py
