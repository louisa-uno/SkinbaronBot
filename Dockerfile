FROM ubuntu:20.04
COPY . /app
WORKDIR /app

RUN apt-get update
RUN apt-get install -y --no-install-recommends g++ gcc libc6-dev make pkg-config libffi-dev python3.6 python3-pip python3-setuptools python3-dev

# RUN pip3 install pipenv
RUN pip3 install selenium==3.141.0
# RUN pipenv install

# CMD pipenv run python3 ./skinbaron.py
CMD python3 ./skinbaron.py