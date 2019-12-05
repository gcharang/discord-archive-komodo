#!/home/gcharang/.nvm/versions/node/v10.16.0/bin/node

const fs = require('fs');
const Discord = require("discord.js");
const client = new Discord.Client();
const {
    token,
    serverId
} = require("./config.json");

client.on('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
    const myGuild = client.guilds.get(serverId);
    let textChannels = {}
    /*
    myGuild.channels.forEach(channel => {
        if (channel.type == 'text') {
            console.log(channel.parent.name)
            if (!textChannels[channel.parentID]) {
                textChannels[channel.parentID] = {}
                textChannels[channel.parentID].categoryName = channel.parent
            }
            textChannels[channel.parentID][channel.id].channelName = channel.name
            textChannels[channel.parentID][channel.id].position = channel.position



        } else {
            return 0
        }
    });*/
    const categoryChannels = myGuild.channels.filter(channel => channel.type === "category");

    categoryChannels.forEach(categoryChannel => {
        console.log(categoryChannel.name)
    })

    console.log(textChannels)

    fs.writeFileSync('channels.json', JSON.stringify(textChannels, null, 2))
})

client.once("ready", () => {
    console.log("Ready!");
});
client.once("reconnecting", () => {
    console.log("Reconnecting!");
});
client.once("disconnect", () => {
    console.log("Disconnect!");
});

client
    .login(token)
    .then(console.log)
    .catch(console.error);