function love.load()
  -- Game State
  game_state = "playing"
  score = 0

  -- Knight (PLAYER_CHARACTER)
  knight = {}
  knight.image = love.graphics.newImage("assets/player.png")
  knight.width = knight.image:getWidth()
  knight.height = knight.image:getHeight()
  knight.x = (800 - knight.width) / 2
  knight.y = (600 - knight.height) / 2
  knight.speed = 200

  -- Goblin (ENEMY_SIMPLE_PATROL)
  goblin = {}
  goblin.image = love.graphics.newImage("assets/enemy.png")
  goblin.width = goblin.image:getWidth()
  goblin.height = goblin.image:getHeight()
  goblin.x = 100
  goblin.y = 400
  goblin.speed = 50
  goblin.direction = 1
  goblin.patrol_min_x = 50
  goblin.patrol_max_x = 300

  -- Coin (ITEM_COLLECTIBLE_STATIC)
  coin = {}
  coin.image = love.graphics.newImage("assets/item.png")
  coin.width = coin.image:getWidth()
  coin.height = coin.image:getHeight()
  coin.x = 500
  coin.y = 300
  coin.visible = true
end

function love.update(dt)
  if game_state == "playing" then
    -- Knight Movement
    if love.keyboard.isDown("w") then
      knight.y = knight.y - knight.speed * dt
    end
    if love.keyboard.isDown("s") then
      knight.y = knight.y + knight.speed * dt
    end
    if love.keyboard.isDown("a") then
      knight.x = knight.x - knight.speed * dt
    end
    if love.keyboard.isDown("d") then
      knight.x = knight.x + knight.speed * dt
    end

    -- Knight Boundary Check
    if knight.x < 0 then
      knight.x = 0
    elseif knight.x + knight.width > 800 then
      knight.x = 800 - knight.width
    end
    if knight.y < 0 then
      knight.y = 0
    elseif knight.y + knight.height > 600 then
      knight.y = 600 - knight.height
    end

    -- Goblin Patrol
    goblin.x = goblin.x + goblin.speed * goblin.direction * dt
    if goblin.x < goblin.patrol_min_x or goblin.x + goblin.width > goblin.patrol_max_x then
      goblin.direction = -goblin.direction
    end

    -- Goblin Collision with Knight
    if knight.x < goblin.x + goblin.width and
       knight.x + knight.width > goblin.x and
       knight.y < goblin.y + goblin.height and
       knight.y + knight.height > goblin.y then
      game_state = "game_over"
    end

    -- Coin Collision with Knight
    if coin.visible then
      if knight.x < coin.x + coin.width and
         knight.x + knight.width > coin.x and
         knight.y < coin.y + coin.height and
         knight.y + knight.height > coin.y then
        coin.visible = false
        score = score + 10
      end
    end
  end
end

function love.draw()
  -- Draw Knight
  love.graphics.draw(knight.image, knight.x, knight.y)

  -- Draw Goblin
  love.graphics.draw(goblin.image, goblin.x, goblin.y)

  -- Draw Coin
  if coin.visible then
    love.graphics.draw(coin.image, coin.x, coin.y)
  end

  -- Draw Score
  love.graphics.print("Score: " .. score, 10, 10)

  -- Draw Game Over
  if game_state == "game_over" then
    love.graphics.print("Game Over!", 350, 280)
  end
end

function love.keypressed(key)
  if key == "escape" then
    love.event.quit()
  end
end