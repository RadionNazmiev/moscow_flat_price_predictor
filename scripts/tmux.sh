#!/bin/bash

# Kill any existing tmux session named "mhpp"
tmux kill-session -t "mhpp" 2>/dev/null

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo "tmux is not installed. Please install tmux first."
    exit 1
fi

# Resolve the absolute path to the project directory
PROJECT_ROOT_DIR="$(pwd)"

# Start tmux server
tmux start-server



# Create a new tmux session named "mhpp" with a window named "back"
tmux new-session -d -s "mhpp" -n "back"

# Horizontally split the "back" window
tmux split-window -v -t "mhpp"

# Rename the panes in the "back" window
tmux select-pane -t "mhpp:back.0" -T "server"
tmux send-keys -t "mhpp:back.0" 'conda activate py3.10' Enter
tmux send-keys -t "mhpp:back.0" "source $PROJECT_ROOT_DIR/scripts/api.sh" Enter

tmux select-pane -t "mhpp:back.1" -T "main"



# Create a new window named "front" within the "mhpp" session
tmux new-window -n "front" -t "mhpp"

# Horizontally split the first pane of the "front" window
tmux split-window -v -t "mhpp:front.0"

# Rename the panes in the "front" window
tmux select-pane -t "mhpp:front.0" -T "server"
tmux send-keys -t "mhpp:front.0" "cd $PROJECT_ROOT_DIR/front-end && npm start" Enter

tmux select-pane -t "mhpp:front.1" -T "main"



# Attach to the "mhpp" session
tmux a -t "mhpp:back"
