Interview
=========

`Interview` is an interactive data viewing and inspecting framework
for the Event Horizon Telescope.
=========
pre-reqs https://github.com/sao-eht/
Instructions
git clone https://github.com/phanicode/interview
pip install -e interview
# get data from csv or hops .vx 
python setup.py install
python static.py # for static dem

bokeh serve --show demo.py #for tabs demo

