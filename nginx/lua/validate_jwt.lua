local openidc = require("resty.openidc")

local opts = {
    discovery = "https://keycloak:8443/realms/game/.well-known/openid-configuration",
    client_id = "game_client",
    ssl_verify = "no",  -- Disable SSL verification (adjust for production)
    cache = ngx.shared.jwks  -- Enable JWKS key caching
}

-- Extract JWT and validate it
local res, err = openidc.bearer_jwt_verify(opts)

if err then
    ngx.status = ngx.HTTP_UNAUTHORIZED
    ngx.say("Unauthorized: ", err)
    ngx.exit(ngx.HTTP_UNAUTHORIZED)
end

-- Add user information from JWT to request headers for the backend
ngx.req.set_header("X-User", res.sub)  -- User ID
ngx.req.set_header("X-User-Roles", table.concat(res.roles or {}, ","))  -- User roles (if available)
