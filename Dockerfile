FROM continuumio/miniconda3:4.8.2

LABEL version="1"
LABEL maintaner="Christoffer Bech (cbe@trifork)"

RUN /opt/conda/bin/conda install jupyter -y

WORKDIR /app

RUN mkdir git

WORKDIR /app/git

# Get the latest donkeycar from Github.
RUN git clone https://github.com/autorope/donkeycar

WORKDIR /app/git/donkeycar

# Checkout git master
RUN git checkout master

# Install donkey envs
RUN conda env create -f ./install/envs/ubuntu.yml --force

# Set the default docker build shell to run as the conda wrapped process
SHELL ["conda", "run", "-n", "donkey", "/bin/bash", "-c"]

RUN pip install -e .[pc]

# Create donkey car
RUN donkey createcar --path ./../../car

WORKDIR /app/car

SHELL ["/bin/bash", "-c"]

# start the jupyter notebook
CMD /opt/conda/bin/jupyter notebook --no-browser --ip 0.0.0.0 --port 8888 --allow-root --notebook-dir=/app/car

# Port for jupyter notebook
EXPOSE 8888
