#Build stage, using slim based-image because alpine cannot use Pandas and Matplotlib
FROM python:3.8.11-slim AS builder

#Copy requirements.txt
COPY requirements.txt .

# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --user -r requirements.txt

# Run stage, using slim based-image because alpine cannot use Pandas and Matplotlib
FROM python:3.8.11-slim
WORKDIR /app

# Set Python buffer to make Docker print every messages instantly.
ENV PYTHONUNBUFFERED=1

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY rdp_apis_console.py .

# update PATH environment variable
ENV PATH=/root/.local:$PATH
ENV USERNAME=DOCKER_CONTAINER

#Run Python
ENTRYPOINT [ "python", "./rdp_apis_console.py" ]
