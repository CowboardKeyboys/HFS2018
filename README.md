# Who seeks shall find
Web application built on flask that takes takes written text and provides matching joblistings and recommends an area in Sweden which to relocate based on number of jobs available and other metrics. This is achieved using natural language processing to match for job adds and weighing the fitness of jobs in an municipality to the number of available jobs.
 
## Authors: Hampus Adamsson, Max Andersson, Daniel Eliassen, Christian Johansson, Joakim Nyman, Viktor Palerius.

## HOWTO:

Du måste köra 
`pip install virtualenv &&ugit clone https://github.com/CowboardKeyboys/HFS2018.git && virtualenv ./HFS2018 && cd HFS2018 && source ./bin/activate && pip install -r requirements.txt && export FLASK_APP=main.py && export FLASK_DEBUG=1 && flask run`
