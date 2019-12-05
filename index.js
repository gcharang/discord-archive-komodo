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
    memberRole = myGuild.roles.find(role => role.name === "Member")
    let textChannels = {}

    const categoryChannels = myGuild.channels.filter(channel => channel.type === "category");

    categoryChannels.forEach(categoryChannel => {

        textChannels[categoryChannel.id] = {}
        textChannels[categoryChannel.id].name = categoryChannel.name
        textChannels[categoryChannel.id].position = categoryChannel.position
        textChannels[categoryChannel.id].channels = {}
        categoryChannel.children.forEach(channel => {
            if (channel.type == 'text' &&
                channel.permissionsFor(myGuild.me).has('VIEW_CHANNEL')) {
                //textChannels[categoryChannel.id].channels[channel.id] = {}
                //textChannels[categoryChannel.id].channels[channel.id].name = channel.name
                textChannels[categoryChannel.id].channels[channel.id] = channel.name
            }
        })


    })
    for (let key in textChannels) {
        if (Object.keys(textChannels[key].channels).length === 0 && textChannels[key].channels.constructor === Object) {
            delete textChannels[key]
        }
    }

    //console.log(JSON.stringify(textChannels, null, 2))

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