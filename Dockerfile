FROM python:3.9

ADD app.py .
ADD requirements.txt .

# RUN python -m venv venv

# RUN exec ./venv/bin/activate

RUN pip install -r requirements.txt

CMD python ./app.py 