### Title
- KPI backend  |  Lab 1
### Author
- IO-14 Bohush Illia

### Starting up flask app

#### Clone github repositiry to your machine

Clone repo
```bash
  git clone https://github.com/bim22614/kpi_backend.git
```

Go to directory
```bash
  cd kpi_backend
```
#### Run through docker compose
(Optional) Change app port
```bash
  nano docker-compose.yaml
```
```bash
   environment:
     PORT: "<your port>"
   ports:
     - "<your port>:8080"
```

Build and run docker compose
```bash
  docker compose build
  docker compose up
```
