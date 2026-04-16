const mineflayer = require('mineflayer');
const express = require('express');
const app = express();

const options = {
  host: 'BackOnTrack.aternos.me',
  port: 46429,             
  username: 'AFKBOT',         // Your bot's name
  version: '1.21.11',              
  // password: 'password'      // Add if using /login
};
const PORT = process.env.PORT || 3000;
app.get('/', (req, res) => {
  res.send('Bot is running!');
});
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
let bot;

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
    // Increased timeout to prevent spam-blocking
    setTimeout(createBot, 10000); 
  });

  bot.on('error', (err) => {
    if (err.code === 'ECONNREFUSED') {
      console.log(`Failed to connect to ${err.address}. Is the server offline?`);
    } else {
      console.log(`Error: ${err.message}`);
    }
  });
}

  bot.on('end', (reason) => {
    console.log(`Bot disconnected: ${reason}`);
    setTimeout(createBot, 5000);
  });

  bot.on('error', (err) => {
    console.log(`Error: ${err.message}`);
    bot.end();
  });
  
  bot.on('kicked', console.log)
}

-
function startAntiAfk() {
  setInterval(() => {
    if (bot && bot.entity) {
      bot.setControlState('jump', true);
      bot.look(Math.random() * 180, 0); // Look in random direction
      setTimeout(() => {
        bot.setControlState('jump', false);
      }, 500); // Jump for 0.5 seconds
    }
  }, 30000); // Run every 30 seconds
}

createBot();
