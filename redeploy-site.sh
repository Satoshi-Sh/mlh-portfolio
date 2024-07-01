tmux kill-window -t flask-run
cd mlh-portfolio
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
pip install reuirements.txt
tmux new-session -d -s flask-run "flask run --host=0.0.0.0"