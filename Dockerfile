FROM python:3.9    

RUN mkdir /marketplace     

WORKDIR /marketplace    

COPY requirements.txt . 

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /marketplace/docker/*.sh
