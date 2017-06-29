FROM ubuntu:14.04

USER root
RUN apt-get update && apt-get install -y \
    python3 \
    curl && \
    rm -rf /var/lib/apt/lists/*
RUN groupadd -r nonroot && \
    useradd -r -g nonroot -d /home/nonroot -s /sbin/nologin -c "Nonroot User" nonroot && \
    mkdir /home/nonroot && \
    chown -R nonroot:nonroot /home/nonroot

USER nonroot
WORKDIR /home/nonroot/

Add . /home/nonroot/

USER nonroot
EXPOSE 3000
WORKDIR /home/nonroot/
CMD ["python3", "-m", "http.server", "3000"]

