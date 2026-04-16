const mineflayer = require('mineflayer');
const express = require('express');
const app = express();

const options = {
  host: 'BackOnTrack.aternos.me',
  port: 46429,              
  username: 'AFKBOT',
  version: '1.21.11' 
};

const PORT = process.env.PORT || 10000;

app.get('/', (req, res) => {
  res.send('Bot is running!');
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

let bot;
let afkInterval;

function createBot() {
  bot = mineflayer.createBot(options);

  bot.once('spawn', () => {
    console.log('Bot spawned in the world!');
    startAntiAfk();
  });

  bot.on('chat', (username, message) => {
    if (username === bot.username) return;
    console.log(`${username} said: ${message}`);
  });

  bot.on('end', (reason) => {
    console.log(`Bot disconnected: ${reason}. Reconnecting in 10s...`);
    if (afkInterval) clearInterval(afkInterval); // Stop AFK timer on disconnect
    setTimeout(createBot, 10000); 
  });

  bot.on('error', (err) => {
    console.log(`Error: ${err.message}`);
  });

  bot.on('kicked', (reason) => {
    console.log(`Kicked for: ${reason}`);
  });
}

function startAntiAfk() {
  if (afkInterval) clearInterval(afkInterval);
  
  afkInterval = setInterval(() => {
    if (bot && bot.entity) {
      bot.setControlState('jump', true);
      bot.look(Math.random() * 180, 0); 
      setTimeout(() => {
        if (bot && bot.entity) bot.setControlState('jump', false);
      }, 500); 
    }
  }, 30000); 
}

createBot();
