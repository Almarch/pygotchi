FROM openresty/openresty:latest

RUN apt update && apt install -y build-essential libreadline-dev unzip wget
RUN wget https://luarocks.org/releases/luarocks-3.9.2.tar.gz \
    && tar zxpf luarocks-3.9.2.tar.gz \
    && cd luarocks-3.9.2 \
    && ./configure --with-lua=/usr/local/openresty/luajit \
    && make && make install \
    && cd .. && rm -rf luarocks-3.9.2 luarocks-3.9.2.tar.gz

COPY nginx.conf /usr/local/openresty/nginx/conf/nginx.conf
COPY ssl/ /etc/nginx/ssl/
COPY lua/ /usr/local/openresty/lualib/

RUN luarocks install lua-resty-openidc \
    && luarocks install lua-resty-http

CMD ["openresty", "-g", "daemon off;"]
