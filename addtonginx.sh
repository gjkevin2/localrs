#!/bin/bash
echo "please input the full domain for RSS"
read domain
basedomian=${domain#*.}

~/.acme.sh/acme.sh --installcert -d $basedomian \
        --key-file   $(pwd)/privkey.pem \
        --fullchain-file $(pwd)/fullchain.pem

# 443端口复用时，修改/etc/nginx/nginx.conf，加上map及upstream(注意有proxy时要2次upstream去除)内容，下面的443换成其他的端口，和upstream一致
cat >/etc/nginx/conf.d/RSS.conf<<-EOF
server {
        listen 80;
        server_name $domain;
        location / {
            rewrite  ^(.*)  https://\$server_name\$request_uri permanent;
     }
}

server {
        listen 443 ssl;
        server_name $domain;
        ssl_certificate  $(pwd)/fullchain.pem;
        ssl_certificate_key $(pwd)/privkey.pem;
        ssl_session_timeout 5m;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_prefer_server_ciphers on;
        location / {
               alias /usr/share/nginx/html/RSS/;
       }

}

EOF
nginx -s reload
systemctl stop nginx
systemctl start nginx


# other hosts set
tee -a /etc/hosts <<-EOF
47.102.227.214 www.thepaper.cn
EOF