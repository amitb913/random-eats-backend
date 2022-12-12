# Random Eats (Backend) - CS 545

This repo contains the backend (written in Python using Flask) for Random Eats. It uses beautifulsoup4 to scrape data from recipe webpages on allrecipes.com and parse them into an organized dict/object. If you are looking for the repo for the frontend, you can access it [here](https://github.com/amitb913/random-eats).

The backend has 4 endpoints:

- /breakfast
- /lunch
- /dinner
- /dessert

Each endpoint can optionally take a query parameter "vegan" as a boolean (true/false) to specify whether or not the recipe should be vegan. If no query parameter is specified, the recipe will be non-vegan.

Ex.: Getting a vegan breakfast recipe

- localhost:8000/breakfast?vegan=true

# Setup/Installation

Anaconda is recommended (with a conda environment). For convenience, my own environment.yml has been attached that can be imported directly to create a conda environment with all the dependencies installed.
Dependencies used:

- requests (2.28.1)
- beautifulsoup4 (4.11.1)
- flask (2.2.2)

Also requires whatever dependencies are required by those mentioned above (should be automatically installed when using conda environments)

# Usage

To run the flask server on port 8000, run the following command in the root directory of the repo:

- flask --app src/main.py run -p 8000

If you need this server to be accessible on the local network (for example, if you need to run the frontend on a physical mobile device or another device on the same network), run the following command instead:

- flask --app src/main.py run -p 8000 -h 0.0.0.0

You can then access the endpoints on the local network by replacing "localhost" with the IPv4 address of the machine running the server.
