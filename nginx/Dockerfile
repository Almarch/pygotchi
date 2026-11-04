ARG OPENRESTY_VERSION=1.27.1.2-1

# ---- Build stage: the fat variant ships luarocks and a C toolchain ----
FROM openresty/openresty:${OPENRESTY_VERSION}-alpine-fat AS builder

# Install into a dedicated tree so the output location is explicit
RUN luarocks --tree=/rocks install lua-resty-http 0.17.1 \
 && luarocks --tree=/rocks install lua-resty-session 4.1.1 \
 && luarocks --tree=/rocks install lua-resty-jwt 0.2.2 \
 && luarocks --tree=/rocks install lua-resty-openidc 1.8.0-1

# ---- Runtime stage: minimal image, no toolchain ----
FROM openresty/openresty:${OPENRESTY_VERSION}-alpine

# site/lualib is in OpenResty's default package.path and package.cpath
COPY --from=builder /rocks/share/lua/5.1/ /usr/local/openresty/site/lualib/
COPY --from=builder /rocks/lib/lua/5.1/   /usr/local/openresty/site/lualib/

CMD ["openresty", "-g", "daemon off;"]