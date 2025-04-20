local json = require("dkjson")

function love.load()
    -- 1) Read the JSON via love.filesystem
    local raw, err = love.filesystem.read("assets/player.json")
    if not raw then
        error("Could not read assets/player.json: " .. tostring(err))
    end

    -- 2) Strip UTF‑8 BOM if present
    if raw:byte(1) == 0xEF and raw:byte(2) == 0xBB and raw:byte(3) == 0xBF then
        raw = raw:sub(4)
        print("Stripped BOM from JSON")
    end

    -- 3) Normalize line endings (\r\n -> \n, \r -> \n)
    raw = raw:gsub("\r\n", "\n"):gsub("\r", "\n")

    -- 4) Trim any leading/trailing whitespace or newlines
    raw = raw:match("^%s*(.-)%s*$")

    -- (Optional) Debug: print the cleaned JSON
    print("--- Cleaned JSON Content Start ---")
    print(raw)
    print("--- Cleaned JSON Content End ---\n")

    -- 5) Decode using dkjson
    local jsonData, pos, err = json.decode(raw, 1, nil) -- dkjson returns data, position, error
    if not jsonData then
        error("Failed to decode player.json: " .. tostring(err) .. " near position " .. tostring(pos))
    end

    -- 6) Load the sprite image
    local imageFile = jsonData.meta.image
    playerImage = love.graphics.newImage("assets/" .. imageFile)

    -- 7) Extract frame data (only one frame for now)
    local frameData = jsonData.frames["player_frame_1"].frame

    -- 8) Initialize player
    player = {
        x     = 100,
        y     = 100,
        width = frameData.w,
        height= frameData.h,
        speed = 200,
        image = playerImage,
        quad  = love.graphics.newQuad(
                   frameData.x, frameData.y,
                   frameData.w, frameData.h,
                   playerImage:getDimensions()
               )
    }
end

function love.update(dt)
    if love.keyboard.isDown("left")  then player.x = player.x - player.speed * dt end
    if love.keyboard.isDown("right") then player.x = player.x + player.speed * dt end
    if love.keyboard.isDown("up")    then player.y = player.y - player.speed * dt end
    if love.keyboard.isDown("down")  then player.y = player.y + player.speed * dt end
end

function love.draw()
    love.graphics.draw(player.image, player.quad, player.x, player.y)
end

function love.keypressed(key)
    if key == "escape" then love.event.quit() end
end