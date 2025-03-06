-- auth.lua

local openidc = require("resty.openidc")

-- Function to handle authentication
local function authenticate()
    local res, err = openidc.authenticate(opts)
    if err then
        ngx.status = ngx.HTTP_FORBIDDEN
        ngx.say("Authentication failed: ", err)
        ngx.exit(ngx.HTTP_FORBIDDEN)
    end
    -- At this point, the user is authenticated, and you can access user info via res.id_token
end

-- Execute authentication
authenticate()
