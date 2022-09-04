FROM python:3.8

COPY techtrends /app
WORKDIR /app

# Install the requirements
RUN pip install -r requirements.txt

# Initialize the DB
RUN python init_db.py

EXPOSE 3111

# command to run on container start
CMD [ "python", "app.py" ]

