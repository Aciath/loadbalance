# loadbalance


Download (pull) docker images nginx dan haproxy.

$ docker pull nginx

Untuk download images haproxy caranya sedikit berbeda. Karena images haproxy memerlukan file haproxy.cfg maka kita perlu membuat Dockerfile saat pull images haproxy.
$ touch haproxy.cfg


Konfigurasi High Availability Web Service
Step 1 - Buat direktory untuk docker compose.
mkdir /docker
touch /docker/docker-compose.yml

Step 2 - Buat direktory untuk konfigurasi haproxy.
mkdir /docker/haproxy
touch /docker/haproxy/haproxy.cfg

Tambahkan perintah berikut pada file /docker/haproxy/haproxy.cfg.

Step 3 - Jalankan docker compose.
docker-compose up -d

Sampai di sini kita sudah bisa menambahkan script html, sebagai contoh buat script index.html sederhana pada folder 
www01 dan www02 pada direktory /docker/nginx/. 
