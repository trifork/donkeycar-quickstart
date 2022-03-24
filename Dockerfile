FROM condaforge/mambaforge:4.9.2-5 as mamba

LABEL version="2"
LABEL maintaner="Jonathan Lüdemann (jolu@trifork)"

WORKDIR /app

RUN mkdir git

WORKDIR /app/git

# Get custom made env-dependencies from jolufan Github.
# could potentially only fetch the yml file
RUN git clone https://github.com/jolufan/donkeycar_test

WORKDIR /app/git/donkeycar_test

# Checkout git master
RUN git checkout master

# Install donkey envs
RUN mamba env create -f install/envs/ubuntu.yml

# Set the default docker build shell to run as the conda wrapped process
SHELL ["mamba", "run", "-n", "donkey", "/bin/bash", "-c"]

RUN pip install -e .[pc]

# Create donkey car
RUN donkey createcar --path ./../../car

WORKDIR /app/car

SHELL ["/bin/bash", "-c"]

ADD requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# Start flask server endpoint to train received data
# Start with docker run -d -p 5000:5000 <name of docker image>
ENTRYPOINT [ "python" ]

CMD ["./src/app.py" ]