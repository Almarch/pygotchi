FROM openresty/openresty:1.27.1.2-1-focal

RUN apt update && apt install -y build-essential libreadline-dev unzip wget \
    && rm -rf /var/lib/apt/lists/*

ENV LUAROCKS_VERSION=3.12.2

RUN wget https://luarocks.org/releases/luarocks-${LUAROCKS_VERSION}.tar.gz \
    && tar zxpf luarocks-${LUAROCKS_VERSION}.tar.gz \
    && cd luarocks-${LUAROCKS_VERSION} \
    && ./configure --with-lua=/usr/local/openresty/luajit \
    && make && make install \
    && cd .. && rm -rf luarocks-${LUAROCKS_VERSION} luarocks-${LUAROCKS_VERSION}.tar.gz

COPY lua/ /usr/local/openresty/lualib/

RUN luarocks install lua-resty-http 0.17.1 \
    && luarocks install lua-resty-session 4.1.1 \
    && luarocks install lua-resty-jwt 0.2.2 \
    && luarocks install lua-resty-openidc 1.8.0-1

CMD ["openresty", "-g", "daemon off;"]
