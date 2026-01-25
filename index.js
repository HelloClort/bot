const mineflayer = require('mineflayer');
const express = require('express');
const app = express();

// --- CONFIGURATION ---
const options = {
  host: 'xnextron-mseJ.aternos.me', // e.g., 'play.hypixel.net'
  port: 34723,                 // Default is 25565
  username: 'BotName',         // Your bot's name
  version: false               // Auto-detect version
  // password: 'password'      // Add if using a paid account or /login
};

// --- WEB SERVER (To keep the bot online) ---
const PORT = process.env.PORT || 3000;
app.get('/', (req, res) => {
  res.send('Bot is running!');
});
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

// --- BOT LOGIC ---
let bot;

function createBot() {
  bot = mineflayer.createBot(options);

  bot.on('login', () => {
    console.log('Bot has logged in!');
    bot.chat('Hello! I am online.'); 
    startAntiAfk();
  });

  bot.on('end', (reason) => {
    console.log(`Bot disconnected: ${reason}`);
    console.log('Reconnecting in 5 seconds...');
    setTimeout(createBot, 5000); // Auto-reconnect
  });

  bot.on('error', (err) => {
    console.log(`Error: ${err.message}`);
    bot.end(); // Trigger auto-reconnect
  });
  
  bot.on('kicked', console.log)
}

// --- ANTI-AFK FUNCTION ---
function startAntiAfk() {
  // Make the bot jump and rotate every few seconds to avoid AFK kick
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
