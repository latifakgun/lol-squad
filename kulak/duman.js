// Duman testi: Latif'in ses kanalına gir, 25 sn dinle, her konuşmayı kayit/duman/ altına WAV yaz, çık.
// Amaç tek: DAVE altında gelen ses çözülebiliyor mu?
const fs = require("node:fs");
const path = require("node:path");
const { Client, GatewayIntentBits } = require("discord.js");
const { joinVoiceChannel, entersState, VoiceConnectionStatus, EndBehaviorType } = require("@discordjs/voice");
const prism = require("prism-media");

process.loadEnvFile(path.join(__dirname, "..", "bot", ".env"));
const OUT = path.join(__dirname, "kayit", "duman");
fs.mkdirSync(OUT, { recursive: true });

function wav(pcm) {
  const h = Buffer.alloc(44);
  h.write("RIFF", 0); h.writeUInt32LE(36 + pcm.length, 4); h.write("WAVEfmt ", 8);
  h.writeUInt32LE(16, 16); h.writeUInt16LE(1, 20); h.writeUInt16LE(2, 22); h.writeUInt32LE(48000, 24);
  h.writeUInt32LE(48000 * 4, 28); h.writeUInt16LE(4, 32); h.writeUInt16LE(16, 34);
  h.write("data", 36); h.writeUInt32LE(pcm.length, 40);
  return Buffer.concat([h, pcm]);
}

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildVoiceStates] });
client.once("clientReady", async () => {
  const guild = await client.guilds.fetch(process.env.DISCORD_GUILD_ID);
  const vs = guild.voiceStates.cache.find(v => v.channelId && v.member && /latif/i.test(`${v.member.user.username} ${v.member.displayName}`));
  if (!vs) { console.log("Latif bir ses kanalında değil."); return client.destroy(); }
  console.log("Kanal:", vs.channel.name);
  const conn = joinVoiceChannel({ channelId: vs.channelId, guildId: guild.id, adapterCreator: guild.voiceAdapterCreator, selfDeaf: false, selfMute: true });
  await entersState(conn, VoiceConnectionStatus.Ready, 20_000);
  console.log("Bağlandı, 25 sn dinliyorum.");
  const busy = new Set();
  conn.receiver.speaking.on("start", userId => {
    if (busy.has(userId)) return;
    busy.add(userId);
    const name = guild.members.cache.get(userId)?.displayName ?? userId;
    const t0 = Date.now(), chunks = [];
    const dec = new prism.opus.Decoder({ rate: 48000, channels: 2, frameSize: 960 });
    dec.on("error", e => console.log("çözme hatası:", name, e.message));
    conn.receiver.subscribe(userId, { end: { behavior: EndBehaviorType.AfterSilence, duration: 1000 } }).pipe(dec);
    dec.on("data", c => chunks.push(c));
    dec.on("end", () => {
      busy.delete(userId);
      const pcm = Buffer.concat(chunks);
      const f = path.join(OUT, `${name.replace(/\W+/g, "_")}_${t0}.wav`);
      fs.writeFileSync(f, wav(pcm));
      console.log("kayıt:", path.basename(f), (pcm.length / 192000).toFixed(1), "sn");
    });
  });
  setTimeout(() => { conn.destroy(); client.destroy(); console.log("Bitti."); }, 25_000);
});
client.login(process.env.KULAK_TOKEN);
