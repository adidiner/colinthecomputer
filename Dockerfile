FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update 
RUN apt-get install -y python3.8 python3-pip git npm
RUN apt-get install -y --no-install-recommends ca-certificates make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
RUN git clone https://github.com/pyenv/pyenv.git /pyenv
ENV PATH "/pyenv:${PATH}"
ENV PYENV_ROOT "/pyenv"
RUN /pyenv/bin/pyenv install -v 3.8.0
RUN /pyenv/bin/pyenv global 3.8.0
RUN pip3 install --upgrade pip
ADD requirements.txt /requirements.txt
RUN pip3.8 install -r /requirements.txt
ADD colinthecomputer /colinthecomputer
RUN apt-get install -y sudo npm
RUN sudo npm install -g npm@latest
RUN sudo npm install colinthecomputer/gui/gui-react
RUN python3 -m virtualenv .env --prompt "[colin] "
RUN find .env -name site-packages -exec bash -c 'echo "../../../../" > {}/self.pth' \;
ENV PYTHONPATH "/"
ENTRYPOINT ["python3.8", "-m"]