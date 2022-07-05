FROM python:3.10
WORKDIR /Website-Gym-Franchise-/app
COPY . .
RUN pip install --no-cache-dir -r src/requirements.txt
EXPOSE 5000
RUN python3 db_populate.py
CMD ["python3", "./__main__.py"]