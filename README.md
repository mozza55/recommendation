## DNBN_recommendation
매칭을 위한 API 서버로 추천 목록과 로그에 대한 리포트를 웹서버에 전달한다.

### 개발환경
- Amazon AWS EC2
- ubuntu 18.04 LTS
- nginx 1.14.0
- anaconda3
- python 3.7.4
- flask
- uwsgi
### Library
#### for API Server
- flask-restplus
- sqlalchemy
- flask-sqlalchemy
- flask-sqlacodegen
- libmysqlcient-dev
- mysqlclient
#### for recommendation
- surprise
#### for GA
- oauth2client
- google-api-python-client

## system architecture
<img src="./data/image/system_architecture.png?raw=true" alt="system_architecture.png"></img>
