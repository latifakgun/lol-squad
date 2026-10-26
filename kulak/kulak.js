// Kulak: /gel ile ses kanalına girer, ekipten konuşan herkesi ayrı ayrı kaydeder; /git ile çıkar.
// Her konuşma: kayit/<gün>/<Ad>_<epoch ms>.wav (16 kHz mono). /bitti tarafı maç aralığındaki klipleri yazıya döker.
const fs = require("node:fs");
const { spawn } = require("node:child_process");
const path = require("node:path");
const { Client, GatewayIntentBits } = require("discord.js");
const { joinVoiceChannel, getVoiceConnection, entersState, VoiceConnectionStatus, EndBehaviorType } = require("@discordjs/voice");
const OpusScript = require("opusscript");

process.loadEnvFile(path.join(__dirname, "..", "bot", ".env"));
const KAYIT = path.join(__dirname, "kayit");
// Discord kullanıcı adı ya da görünen ad → konuşmada geçen ad. Listede olmayan kaydedilmez.
const SQUAD = [[/latif/i, "Latif"], [/feared/i, "Patrick"], [/swag/i, "Swag"], [/pretty when you cry/i, "Minte"], [/yilmaz/i, "Yılmaz"], [/g[öo]rkem/i, "Görkem"]];
const PYTHON = process.env.KULAK_PYTHON || "python"; // bot/konusma.py'yi çalıştıracak, lolbot paketleri kurulu olan python
let since = null; // açık oturumun başlangıcı (ms)

// Oturumu kapat: kanaldan çık, kayıtları yazıya döküp Argon'a notlat (bot/konusma.py → kulak/konusmalar/).
function stop(guildId, why) {
  getVoiceConnection(guildId)?.destroy();
  if (since === null) return false;
  const start = since, end = Date.now();
  since = null;
  log(why, "→ konuşmalar işleniyor");
  const p = spawn(PYTHON, ["-u", "konusma.py", String(start), String(end)], { cwd: path.join(__dirname, "..", "bot"), env: { ...process.env, PYTHONUTF8: "1" } });
  p.stdout.on("data", d => log("konusma.py:", String(d).trim()));
  p.stderr.on("data", d => log("konusma.py hata:", String(d).trim().slice(-300)));
  return true;
}
const MIN_SN = 0.5; // daha kısası nefes/tık, yazıya dökmeye değmez

const log = (...a) => console.log(new Date().toLocaleTimeString("tr-TR"), ...a);
const who = m => m && SQUAD.find(([re]) => re.test(`${m.user.username} ${m.displayName}`))?.[1];

function wav16k(pcm48) {
  // 48 kHz mono → 16 kHz: üç örneğin ortalaması. ponytail: kaba ama konuşma tanıma için yeterli; sorun çıkarsa gerçek resampler.
  const n = Math.floor(pcm48.length / 6), out = Buffer.alloc(n * 2);
  for (let i = 0; i < n; i++) out.writeInt16LE(Math.round((pcm48.readInt16LE(i * 6) + pcm48.readInt16LE(i * 6 + 2) + pcm48.readInt16LE(i * 6 + 4)) / 3), i * 2);
  const h = Buffer.alloc(44);
  h.write("RIFF", 0); h.writeUInt32LE(36 + out.length, 4); h.write("WAVEfmt ", 8);
  h.writeUInt32LE(16, 16); h.writeUInt16LE(1, 20); h.writeUInt16LE(1, 22); h.writeUInt32LE(16000, 24);
  h.writeUInt32LE(32000, 28); h.writeUInt16LE(2, 32); h.writeUInt16LE(16, 34);
  h.write("data", 36); h.writeUInt32LE(out.length, 40);
  return Buffer.concat([h, out]);
}

function record(conn, guild) {
  const busy = new Set();
  conn.receiver.speaking.on("start", userId => {
    const name = who(guild.members.cache.get(userId));
    if (!name || busy.has(userId)) return;
    busy.add(userId);
    const t0 = Date.now(), chunks = [];
    const opus = conn.receiver.subscribe(userId, { end: { behavior: EndBehaviorType.AfterSilence, duration: 1000 } });
    const dec = new OpusScript(48000, 1);
    let bad = 0;
    const done = () => {
      if (!busy.delete(userId)) return; // bir kez
      dec.delete();
      if (bad) log("atlanan bozuk paket:", name, bad);
      const pcm = Buffer.concat(chunks);
      if (pcm.length / 96000 < MIN_SN) return;
      const dir = path.join(KAYIT, new Date(t0).toISOString().slice(0, 10));
      fs.mkdirSync(dir, { recursive: true });
      fs.writeFileSync(path.join(dir, `${name}_${t0}.wav`), wav16k(pcm));
    };
    // Paketleri tek tek çöz: prism'in Decoder akışı tek bozuk pakette kendini kapatıyor (duman testinde Minte hiç kaydedilmedi).
    opus.on("data", p => { try { chunks.push(Buffer.from(dec.decode(p))); } catch { bad++; } });
    opus.on("end", done); opus.on("close", done); opus.on("error", done);
  });
}

async function join(channel) {
  const old = getVoiceConnection(channel.guild.id);
  if (old?.joinConfig.channelId === channel.id) return;
  old?.destroy();
  const conn = joinVoiceChannel({ channelId: channel.id, guildId: channel.guild.id, adapterCreator: channel.guild.voiceAdapterCreator, selfDeaf: false, selfMute: true });
  conn.on(VoiceConnectionStatus.Disconnected, async () => {
    try { await Promise.race([entersState(conn, VoiceConnectionStatus.Signalling, 5000), entersState(conn, VoiceConnectionStatus.Connecting, 5000)]); }
    catch { stop(channel.guild.id, "kanaldan atıldım ya da bağlantı koptu"); }
  });
  await entersState(conn, VoiceConnectionStatus.Ready, 20_000);
  since ??= Date.now();
  record(conn, channel.guild);
  log("dinliyorum:", channel.name);
}

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildVoiceStates] });
client.once("clientReady", async () => {
  const guild = await client.guilds.fetch(process.env.DISCORD_GUILD_ID);
  await guild.commands.set([
    { name: "gel", description: "Kulak bulunduğun ses kanalına gelir ve ekibi kaydetmeye başlar" },
    { name: "git", description: "Kulak ses kanalından çıkar, kayıt durur" },
  ]);
  log("hazır:", client.user.tag, "· /gel /git");
});
client.on("interactionCreate", async i => {
  if (!i.isChatInputCommand()) return;
  if (i.commandName === "git") {
    const had = stop(i.guildId, `/git: ${i.user.username}`);
    return i.reply(had ? "👋 Çıktım. Konuşmaları yazıya döküp Argon'a veriyorum, /bitti bunları kullanacak." : "Zaten bir kanalda değilim.");
  }
  const channel = i.member?.voice?.channel;
  if (!channel) return i.reply({ content: "Önce bir ses kanalına gir, oraya geleyim.", ephemeral: true });
  await i.deferReply();
  try { await join(channel); await i.editReply(`🔴 ${channel.name} kanalındayım, ekibi kaydediyorum. Göndermek için /git.`); }
  catch (e) { await i.editReply(`Giremedim: ${e.message}`); }
});
client.on("voiceStateUpdate", (before, after) => {
  // Latif kulağın olduğu kanaldan çıkarsa kulak da çıkar.
  const conn = getVoiceConnection(after.guild.id);
  if (conn && who(after.member) === "Latif" && before.channelId === conn.joinConfig.channelId && after.channelId !== before.channelId) {
    stop(after.guild.id, "Latif çıktı, ben de çıktım");
  }
});
client.login(process.env.KULAK_TOKEN);
