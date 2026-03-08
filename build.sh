docker build -t docker2.lan:5000/fuelpricecollector:latest . --no-cache
docker login docker2.lan:5000
docker push docker2.lan:5000/fuelpricecollector:latest