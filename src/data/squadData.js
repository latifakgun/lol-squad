export const squadData = {
  lastUpdated: "2026-10-24",
  players: {
    l4cg: {
      riotId: "l4cg#TR1",
      tag: "Mid / Support",
      summary: "Demir II (Tek/Çift 39 LP · Esnek 33 LP, 46. seviye). Son 10 maçında %60 galibiyet oranı (6G 4M) yakaladı; Xerath ile Tek/Çift'te 13/4/14, Seraphine ile Esnek'te 5/4/20 ve 3/10/21 asist katkısıyla ekibin orta koridor ve destek yükünü sırtlıyor.",
      kpis: [
        { val: "%60", lbl: "Son 10 Maç WR (6G 4M)" },
        { val: "%55", lbl: "Son 20 Maç WR (2.19 KDA)" },
        { val: "%57", lbl: "Sezon Xerath WR (7 Maç)" },
        { val: "6.4–7.1", lbl: "Mid Zirve CS/dk (Veigar/Xerath)" }
      ],
      good: [
        "<strong>Koridor Yönetimi ve Roam Zekâsı:</strong> Rakibi kestikten sonra dalgayı kuleye sokup (<em>Crash</em>) minyon kaybettirerek alt ve üst koridora zamanında rotasyon yapıyor.",
        "<strong>Yüksek Minyon Toplama Tavanı:</strong> Son maçlarında Xerath ile 271 CS, Veigar ile 247 CS ve 217 CS (7.1 CS/dk) barajlarına ulaşarak geç oyunda ciddi altın üstünlüğü kurdu.",
        "<strong>Geç Oyun ve Takım Savaşı Etkisi:</strong> 30. dakikayı geçen maçlarda kazanma oranı <strong>+%9.8</strong> artıyor; Seraphine ile Esnek maçlarında 20 ve 21 asist üreterek takım savaşlarını çeviriyor."
      ],
      bad: [
        "<strong>Veigar ve Xerath'ta Cam Topu Dizilimi:</strong> Suikastçı ve üstüne atlayan rakiplere karşı 0 Can/Kalkan (<em>Luden + Yıldırım Asası + Gölgealev</em>) çıktığı maçlarda çok fazla ölüm veriyor (Xerath 10/23/12, Veigar 9/11/6 ve 14/12/14).",
        "<strong>Sıfır Kontrol Totemi Alışkanlığı:</strong> Maçların tamamında <em>No Control Wards</em> etiketi bulunuyor; nehir ve çalı görüşü eksik kaldığı için baskınlara açık kalıyor.",
        "<strong>Seraphine'de Yanlış Eşya ve Çizme Tercihi:</strong> <em>Zaz'Zak + Sihirbaz Pabuçları</em> çıktığında yetenek hızı düşük kalıyor, W kalkanı geç dönüyor ve 3/10/21 gibi yüksek ölüm sayılarına çıkıyor.",
        "<strong>Üst Koridor Denemeleri:</strong> Sezon genelinde Quinn (6 maç %0 WR, 0.64 KDA) ve Trundle (%50 WR, 1.16 KDA) seçimleri dereceli puanını aşağı çekiyor."
      ],
      fix: [
        "<strong>Veigar Hayatta Kalma Reçetesi:</strong> Zed, Yone, Sylas ve Akali gibi suikastçılara karşı <em>Aery'yi Çağır + Kemik Zırh</em> rününe ve <strong>Başmelek Asası → İonia Çizmesi → Rabadon'un Şapkası → Zhonya/Banshee</strong> sırasına geç; arabalı minyonları mutlaka Q ile (+3 stack) al.",
        "<strong>Xerath Görüş ve Mesafe Koruması:</strong> 9. seviyede anında <strong>Mavi Totem (Uzak Görüş)</strong> al; suikastçılara karşı <em>Sıçra + Bariyer/Bitkinlik</em> seçip 3. eşyada Zhonya veya Banshee'yi ihmal etme.",
        "<strong>Seraphine Rylai + Kızağı Sinerjisi:</strong> Destek eşyasında Zaz'Zak yerine <strong>Gündönümü Kızağı</strong>, çizmede <strong>İonia Çizmesi</strong> al; ardından <strong>Rylai'nin Kristal Asası + İmparatorun Fermanı</strong> ile tekli E yeteneğini doğrudan mıhlamaya (<em>Root</em>) çevir."
      ],
      builds: [
        {
          champ: "Veigar",
          note: "Mid · Geç Oyun Canavarı (61B Ustalık)",
          variants: [
            {
              title: "Zor Eşleşme: Suikastçı & Dash Şampiyonları",
              kind: "danger",
              enemies: "Zed, Katarina, Akali, Sylas, Yasuo, Yone, Fizz, Irelia",
              keystone: "Aery'yi Çağır",
              runes: ["Mana Akışı Yüzüğü", "Yücelik", "Kızart", "Kemik Zırh", "Aşırı Büyüme"],
              spells: ["Sıçra + Bitkinlik"],
              items: [
                { name: "Başmelek Asası", note: "Can kurtaran kalkan" },
                { name: "İonia Çizmesi", note: "Kafes (E) süresi düşer" },
                { name: "Rabadon'un Şapkası", note: "Pasif AP'yi %30 katlar" },
                { name: "Zhonya / Banshee", note: "AD=Zhonya, AP=Banshee" },
                { name: "Kriptçiçek", note: "%Büyü nüfuzu + can" }
              ]
            },
            {
              title: "Rahat Eşleşme: Menzilli Büyücüler",
              kind: "standard",
              enemies: "Ahri, Vex, Lux, Brand, Mel, Viktor, Malzahar",
              keystone: "Sihirli Komet",
              runes: ["Mana Akışı Yüzüğü", "Yücelik", "Yaklaşan Fırtına", "İkinci Şans", "Aşırı Büyüme"],
              spells: ["Sıçra + Işınlanma"],
              items: [
                { name: "Başmelek Asası", note: "Mana + güvence" },
                { name: "Sihirbaz Pabuçları", note: "+18 büyü nüfuzu" },
                { name: "Rabadon'un Şapkası", note: "2. eşya şart" },
                { name: "Gölgealev / Kriptçiçek", note: "Tekleme hasarı" },
                { name: "Zhonya / Banshee", note: "Geç oyun sigortası" }
              ]
            }
          ]
        },
        {
          champ: "Xerath",
          note: "Mid / Support · Uzun Menzil Topçusu (64B Ustalık)",
          variants: [
            {
              title: "Karşıda Suikastçı / Üstüne Uçan Varsa",
              kind: "danger",
              enemies: "Zed, Fizz, Katarina, Yone, Yasuo, Kayn, Nocturne, Zac",
              keystone: "Sihirli Komet",
              runes: ["Mana Akışı Yüzüğü", "Yücelik", "Kızart", "Kemik Zırh", "Aşırı Büyüme"],
              spells: ["Sıçra + Bariyer"],
              items: [
                { name: "Luden'in Silahı", note: "Dürtme + dalga eritme" },
                { name: "Sihirbaz Pabuçları", note: "Erken büyü nüfuzu" },
                { name: "Ufukgetiren", note: "%10 ekstra hasar + görüş" },
                { name: "Zhonya / Banshee", note: "Suikastçı sigortası" },
                { name: "Rabadon'un Şapkası", note: "Tam infaz" }
              ]
            },
            {
              title: "Karşıda Kırılgan / Hantal Şampiyonlar Varsa",
              kind: "standard",
              enemies: "Veigar, Lux, Orianna, Mel, Brand, Vex, Hantal Tanklar",
              keystone: "Sihirli Komet",
              runes: ["Mana Akışı Yüzüğü", "Mutlak Odak", "Yaklaşan Fırtına", "Ucuz Atış", "Hazine Avcısı"],
              spells: ["Sıçra + Işınlanma"],
              items: [
                { name: "Luden'in Silahı", note: "Ana başlangıç" },
                { name: "Sihirbaz Pabuçları", note: "Erken nüfuz" },
                { name: "Ufukgetiren / Gölgealev", note: "Uzaktan patlama" },
                { name: "Rabadon'un Şapkası", note: "Maksimum AP" },
                { name: "Hiçlik Değneği", note: "Büyü direnci kırma" }
              ]
            }
          ]
        },
        {
          champ: "Seraphine",
          note: "Support · Kalkan + Kitle Kontrol Motoru (31B Ustalık)",
          variants: [
            {
              title: "Rylai + Ferman (Yakalama & CC) Buildi",
              kind: "standard",
              enemies: "Briar ve Jhin/MF ile rakipleri olduğu yere mıhlamak için",
              keystone: "Aery'yi Çağır",
              runes: ["Mana Akışı Yüzüğü", "Yücelik", "Yaklaşan Fırtına", "Kemik Zırh", "Canlandır"],
              spells: ["Sıçra + Bitkinlik"],
              items: [
                { name: "Gündönümü Kızağı", note: "E tutunca can + hız" },
                { name: "İonia Çizmesi", note: "Yetenek hızı şart" },
                { name: "Rylai'nin Kristal Asası", note: "Tek E bile mıhlar" },
                { name: "İmparatorun Fermanı", note: "Mıhlanan hedefe patlama" },
                { name: "Aytaşı Yenileyici", note: "Takım kalkanı" }
              ]
            },
            {
              title: "Tam Koruma / Ölümsüz Briar (Enchanter) Buildi",
              kind: "danger",
              enemies: "Ağır suikastçı veya yüksek dürtme kompozisyonlarına karşı",
              keystone: "Aery'yi Çağır",
              runes: ["Mana Akışı Yüzüğü", "Yücelik", "Suda Yürüyen", "Yaşam Kaynağı", "Canlandır"],
              spells: ["Sıçra + Bitkinlik"],
              items: [
                { name: "Hayalperest", note: "Destek kalkan yükseltmesi" },
                { name: "İonia Çizmesi", note: "Daha sık W kalkanı" },
                { name: "Aytaşı Yenileyici", note: "W kalkanını takıma yayar" },
                { name: "Helia'nın Yankıları", note: "İyileştirme + hasar" },
                { name: "Kefaret", note: "Alan iyileştirmesi" }
              ]
            }
          ]
        }
      ],
      matches: [
        {
          date: "2026-10-24",
          queue: "Normal",
          champ: "Veigar",
          role: "Mid",
          result: "loss",
          kda: "8/7/12",
          cs: 154,
          duration: null,
          items: [],
          verdict: "Swag (Miss Fortune 11/8/10) ile girilen normal maçta 20 skor katkısı üretilse de orta oyundaki takım savaşları kaybedildi.",
          premade: ["swag"]
        },
        {
          date: "2026-10-24",
          queue: "Esnek",
          champ: "Xerath",
          role: "Mid",
          result: "loss",
          kda: "10/23/12",
          cs: 271,
          duration: null,
          items: [],
          verdict: "271 CS ile yüksek farm yapıldı ancak 23 ölümle hayatta kalma eşyası (Zhonya/Banshee) eksikliği çok ağır hissedildi.",
          premade: ["swag", "patrick"]
        },
        {
          date: "2026-10-24",
          queue: "Esnek",
          champ: "Veigar",
          role: "Mid",
          result: "win",
          kda: "14/12/14",
          cs: 247,
          duration: null,
          items: [],
          verdict: "247 CS ve 28 skor katkısıyla geç oyunda Patrick'in 28 kill'lik Rengar'ıyla birlikte maçı kapattı.",
          premade: ["swag", "patrick"]
        },
        {
          date: "2026-10-23",
          queue: "Dereceli Tek/Çift",
          champ: "Xerath",
          role: "Mid",
          result: "win",
          kda: "13/4/14",
          cs: 134,
          duration: null,
          items: [],
          verdict: "6.75 KDA ve OP Score 9.2 ile uzaktan pozisyon bozmadan tek başına taşınan kusursuz bir Tek/Çift galibiyeti.",
          premade: []
        },
        {
          date: "2026-10-23",
          queue: "Esnek",
          champ: "Seraphine",
          role: "Support",
          result: "win",
          kda: "3/10/21",
          cs: 50,
          duration: null,
          items: [],
          verdict: "10 kez ölünmesine rağmen 21 asist ve kitle kontrol zinciriyle Minte ve Swag'e takım savaşlarında alan açıldı.",
          premade: ["minte", "swag"]
        },
        {
          date: "2026-10-23",
          queue: "Esnek",
          champ: "Seraphine",
          role: "Support",
          result: "win",
          kda: "5/4/20",
          cs: 31,
          duration: null,
          items: [],
          verdict: "6.25 KDA (OP Score 7.7, maç 2.'si) ile Minte'nin 14/3/5 Briar'ını ölümsüz kılan harika bir destek performansı.",
          premade: ["minte", "swag"]
        },
        {
          date: "2026-10-23",
          queue: "Esnek",
          champ: "Veigar",
          role: "Mid",
          result: "loss",
          kda: "9/11/6",
          cs: 184,
          duration: null,
          items: [
            { name: "Luden'in Silahı", flag: "bad" },
            { name: "Yıldırım Asası", flag: "bad" },
            { name: "Gölgealev", flag: "bad" }
          ],
          verdict: "Cam topu eşya dizilimi yüzünden 11 ölüm verildi; üst koridorda Minte'nin Mordekaiser'i (4/13/5) çökünce maç koptu.",
          premade: ["minte", "swag"]
        },
        {
          date: "2026-10-22",
          queue: "Dereceli Tek/Çift",
          champ: "Veigar",
          role: "Mid",
          result: "win",
          kda: "7/2/5",
          cs: 217,
          duration: null,
          items: [],
          verdict: "Sadece 2 ölüm ve 217 CS (7.1 CS/dk) ile disiplinli koridor yönetimiyle alınan temiz galibiyet.",
          premade: []
        },
        {
          date: "2026-10-22",
          queue: "Dereceli Tek/Çift",
          champ: "Veigar",
          role: "Mid",
          result: "loss",
          kda: "0/7/1",
          cs: 108,
          duration: null,
          items: [],
          verdict: "Erken oyunda suikastçı baskısına karşı kalkan/savunma olmayınca koridor aşamasında koptu.",
          premade: []
        },
        {
          date: "2026-10-22",
          queue: "Esnek",
          champ: "Xerath",
          role: "Support",
          result: "win",
          kda: "3/5/10",
          cs: 137,
          duration: null,
          items: [],
          verdict: "Uzaktan dürtme ve 10 asistle Minte'nin 23/5/7 Briar şovuna güvenli zemin hazırladı.",
          premade: ["minte"]
        }
      ]
    },
    minte: {
      riotId: "minte#000",
      tag: "Jungle · Briar OTP",
      summary: "Altın IV (96 LP) Tek/Çift ve Gümüş III (78 LP) Esnek oyuncusu (112. seviye). 577.479 ustalık puanıyla sezonun %88'ini ormanda (65 maç Briar, 12.9/7.4/5.5 KDA, 7.0 CS/dk) geçiriyor; Briar aldığında ekibin birincil taşıyıcısı konumunda.",
      kpis: [
        { val: "Altın IV", lbl: "Tek/Çift (96 LP)" },
        { val: "577B", lbl: "Briar Ustalık (#1,637 TR)" },
        { val: "7.0", lbl: "Sezon Briar CS/dk (65 Maç)" },
        { val: "%50", lbl: "Son 10 Maç WR (5G 5M)" }
      ],
      good: [
        "<strong>Elit Briar Farm Hızı ve Taşıyıcılık:</strong> Sezon genelinde 65 Briar maçında ortalama <strong>12.9 Kill ve 7.0 CS/dk</strong> (521.3 altın/dk) üretiyor; son maçlarında 29/6/6 (276 CS), 23/5/7 (266 CS) ve 14/3/5 (204 CS) ile MVP (OP Score 10) aldı.",
        "<strong>Baron ve Kule Hakimiyeti:</strong> Öne geçtiği her maçta <em>Good Baron Usage</em> ve <em>Turrets Destroyer</em> madalyalarını toplayarak harita hedeflerini hızla eritiyor.",
        "<strong>Seri Yakalama İvmesi:</strong> Günün ilk galibiyetinden sonra kazanma oranı <strong>+%7.2</strong>, ikinci maçında <strong>+%11.2</strong> yükseliyor."
      ],
      bad: [
        "<strong>Orman Dışı Koridor Denemeleri:</strong> Üst koridorda Mordekaiser (4/13/5) ve Cho'Gath (7/13/6) aldığında Briar'daki can çalma alışkanlığıyla takasa girip 13 kez ölüyor.",
        "<strong>Geriye Düşünce Tam Suikastçı Eşyasında Israr:</strong> 6/9/2 gibi geriye düştüğü Briar maçlarında savunma almak yerine 2. eşya <em>Tahsildar (The Collector)</em> çıktığı için W bastığında anında eriyor.",
        "<strong>Kontrol Totemi ve Erken Teslimiyet:</strong> Maçlarda 0 pembe totem (<em>No Control Wards</em>) kullanıyor ve erken oyunda skor gerideyse (+%24.2 FF oranı) maçı kafada çabuk bitiriyor."
      ],
      fix: [
        "<strong>Derecelide %100 Orman Disiplini:</strong> Sezon verisinde %88 orman rolü dışındaki tüm denemeler (Cho'Gath %0 WR, Vayne/Jinx/Ezreal %0 WR) kaybettiriyor; Briar yasaklanırsa <strong>Amumu, Diana veya Warwick</strong> seç.",
        "<strong>Geriye Düşülen Maçlarda Dövüşçü (Bruiser) Briar:</strong> Maça 0/3 başlandığında <em>Kâfir Hidra + Tahsildar</em> yerine <strong>Haşmetli Hidra / Mahvolmuş Kralın Kılıcı → Kara Balta → Sterak'ın Güvencesi</strong> dizilimine dön.",
        "<strong>Vadi'nin Alameti ve Görüş Kontrolü:</strong> İlk dönüşte 1 Kontrol Totemi alıp 14. dakikadaki Vadi'nin Alameti'ni orta koridor (l4cg) kulesini açmak için kullan."
      ],
      builds: [
        {
          champ: "Briar",
          note: "Jungle · Ana Taşıyıcı (577B Ustalık · 65 Maç)",
          variants: [
            {
              title: "Öndeyken: Kartopu & Suikastçı Dizilimi",
              kind: "standard",
              enemies: "Kırılgan nişancı ve büyücü ağırlıklı rakipler",
              keystone: "Keskin Sağanak",
              runes: ["Ani Darbe", "Gözyuvarı Koleksiyonu", "Hazine Avcısı", "Zafer", "Efsane: Çeviklik"],
              spells: ["Sıçra + Çarp"],
              items: [
                { name: "Kâfir Hidra", note: "Hızlı orman + patlama" },
                { name: "Çelik Kaplamalı Çizme", note: "Fiziksel hasar azaltma" },
                { name: "Tahsildar", note: "%5 infaz + altın" },
                { name: "Ölümün Dansı", note: "Kanama geciktirme" },
                { name: "Sterak'ın Güvencesi", note: "Takım savaşı kalkanı" }
              ]
            },
            {
              title: "Gerideyken veya Tank/CC Rakiplere Karşı: Dövüşçü (Bruiser)",
              kind: "danger",
              enemies: "Rammus, Amumu, Leona, Mordekaiser, Ağır Kitle Kontrol",
              keystone: "Yenilmez",
              runes: ["Zafer", "Efsane: Çeviklik", "Son Direniş", "Kemik Zırh", "Canlandır"],
              spells: ["Sıçra + Çarp"],
              items: [
                { name: "Haşmetli Hidra / Mahvolmuş Kral", note: "Can + sürekli hasar" },
                { name: "Merkür'ün Adımları", note: "Sıvışma (CC azaltma)" },
                { name: "Kara Balta", note: "Zırh kırma + can + hız" },
                { name: "Sterak'ın Güvencesi", note: "Patlama koruması" },
                { name: "Ruh Gömleği / Ölümün Dansı", note: "İyileşme artışı" }
              ]
            }
          ]
        },
        {
          champ: "Diana",
          note: "Jungle · Takıma AP Lazım Olduğunda (62B Ustalık)",
          variants: [
            {
              title: "Standart AP Orman Dövüşçü/Suikastçı",
              kind: "standard",
              enemies: "Takımda tam AD olunduğunda veya kırılgan arka saflara karşı",
              keystone: "Yenilmez",
              runes: ["Zafer", "Efsane: Çeviklik", "Son Direniş", "Ani Darbe", "Hazine Avcısı"],
              spells: ["Sıçra + Çarp"],
              items: [
                { name: "Nashor'un Dişi", note: "Maksimum orman dönme hızı" },
                { name: "Sihirbaz Pabuçları", note: "Büyü nüfuzu" },
                { name: "Lich Boğan / Vadiyaran", note: "Patlama veya hayatta kalma" },
                { name: "Zhonya'nın Kumsaati", note: "Ulti sonrası koruma" },
                { name: "Rabadon'un Şapkası", note: "Geç oyun infazı" }
              ]
            }
          ]
        }
      ],
      matches: [
        {
          date: "2026-10-23",
          queue: "Esnek",
          champ: "Cho'Gath",
          role: "Top",
          result: "win",
          kda: "7/13/6",
          cs: 206,
          duration: null,
          items: [],
          verdict: "Koridorda 13 kez ölünmesine rağmen 206 CS ve ön saf tanklığıyla Seraphine + Jhin ikilisinin maçı taşımasına alan açtı.",
          premade: ["l4cg", "swag"]
        },
        {
          date: "2026-10-23",
          queue: "Esnek",
          champ: "Briar",
          role: "Jungle",
          result: "win",
          kda: "14/3/5",
          cs: 204,
          duration: null,
          items: [
            { name: "Kâfir Hidra", flag: "good" },
            { name: "Tahsildar", flag: "good" },
            { name: "Ölümün Dansı", flag: "good" }
          ],
          verdict: "6.33 KDA ve 204 CS ile l4cg'nin Seraphine kalkanları altında vadiyi domine etti.",
          premade: ["l4cg", "swag"]
        },
        {
          date: "2026-10-23",
          queue: "Esnek",
          champ: "Mordekaiser",
          role: "Top",
          result: "loss",
          kda: "4/13/5",
          cs: 149,
          duration: null,
          items: [],
          verdict: "Orman dışına çıkıp üst koridorda Mordekaiser ile 13 ölüm verilince harita kontrolü tamamen kaybedildi.",
          premade: ["l4cg", "swag"]
        },
        {
          date: "2026-10-22",
          queue: "Esnek",
          champ: "Briar",
          role: "Jungle",
          result: "win",
          kda: "23/5/7",
          cs: 266,
          duration: null,
          items: [
            { name: "Kâfir Hidra", flag: "good" },
            { name: "Tahsildar", flag: "good" },
            { name: "Ölümün Dansı", flag: "good" }
          ],
          verdict: "OP Score 10 (Maç 1.'si)! 23 kill ve 266 CS ile l4cg'nin Xerath'ıyla birlikte kusursuz bir orman-destek zaferi.",
          premade: ["l4cg"]
        },
        {
          date: "2026-10-22",
          queue: "Normal",
          champ: "Cho'Gath",
          role: "Top",
          result: "win",
          kda: "10/10/15",
          cs: 230,
          duration: null,
          items: [],
          verdict: "230 CS ve 25 skor katkısıyla geç oyunda dev can havuzuyla takım savaşlarını önde tuttu.",
          premade: []
        },
        {
          date: "2026-10-22",
          queue: "Normal",
          champ: "Briar",
          role: "Jungle",
          result: "win",
          kda: "29/6/6",
          cs: 276,
          duration: null,
          items: [
            { name: "Kâfir Hidra", flag: "good" },
            { name: "Tahsildar", flag: "good" },
            { name: "Ölümün Dansı", flag: "good" }
          ],
          verdict: "OP Score 10 (Maç 1.'si)! 29 kill ve 276 CS ile tek başına haritayı süpürdüğü imza Briar maçı.",
          premade: []
        },
        {
          date: "2026-10-21",
          queue: "Normal",
          champ: "Briar",
          role: "Jungle",
          result: "loss",
          kda: "6/9/2",
          cs: 122,
          duration: null,
          items: [
            { name: "Tahsildar", flag: "bad" }
          ],
          verdict: "Gerideyken dövüşçü eşyası yerine suikastçı (Tahsildar) çıkınca takım savaşlarında kitle kontrol altında eridi.",
          premade: []
        },
        {
          date: "2026-10-21",
          queue: "Normal",
          champ: "Briar",
          role: "Jungle",
          result: "loss",
          kda: "2/2/1",
          cs: 118,
          duration: null,
          items: [],
          verdict: "Erken oyunda diğer koridorlar düşünce 20. dakika civarında erken teslim (FF) ile biten maç.",
          premade: []
        },
        {
          date: "2026-10-21",
          queue: "Normal",
          champ: "Shaco",
          role: "Jungle",
          result: "loss",
          kda: "4/1/3",
          cs: 167,
          duration: null,
          items: [],
          verdict: "7.00 KDA ve sadece 1 ölümle iyi başlansa da takım geri düşünce çevrilemedi.",
          premade: []
        },
        {
          date: "2026-10-21",
          queue: "Normal",
          champ: "Mordekaiser",
          role: "Top",
          result: "loss",
          kda: "2/2/1",
          cs: 117,
          duration: null,
          items: [],
          verdict: "Kısa süren normal maçta koridor aşamasından sonra erken FF verildi.",
          premade: []
        }
      ]
    },
    swag: {
      riotId: "swagisback#333",
      tag: "ADC / Support",
      summary: "Seviye 26–30 nişancı ve destek oyuncusu (Morgana 35B, Jhin 13B, Garen 13B, Miss Fortune 8.6B ustalık). Son 10 maçında %50 galibiyet oranı (5G 5M) yakaladı; l4cg'nin Seraphine/Veigar kitle kontrolünün üstüne Miss Fortune ve Jhin ultileriyle iyi skor topluyor ancak orta oyunda minyon kesmeyi bırakması ve yanlış ilk eşya seçimleri hasarını düşürüyor.",
      kpis: [
        { val: "%50", lbl: "Son 10 Maç WR (5G 5M)" },
        { val: "35.8B", lbl: "Morgana Ustalık (Sv. 6)" },
        { val: "13.5B", lbl: "Jhin Ustalık (Sv. 4)" },
        { val: "3.4/7.6/7.4", lbl: "Genel KDA Ortalaması" }
      ],
      good: [
        "<strong>Bozulmayan Mental (Bounces Back):</strong> Mağlubiyetten sonraki maçta kazanma oranı <strong>+%9.9</strong> artıyor; tilt olmadan bir sonraki oyuna odaklanabiliyor.",
        "<strong>Baskınlardan Kaçış (Ungankable):</strong> Koridor aşamasında Jhin, Miss Fortune ve Garen oynarken rakip ormancı baskınlarına karşı güvenli pozisyon alıyor.",
        "<strong>Takım Savaşı Ulti Takibi:</strong> Seraphine, Veigar ve Briar'ın yakaladığı hedeflere Miss Fortune (11/17/17, 4/9/15) ve Jhin (4/9/13) ile yüksek asist katkısı veriyor."
      ],
      bad: [
        "<strong>15. Dakikadan Sonra Minyon Kesmeyi Bırakma (Stopped CSing):</strong> Kuleler yıkıldıktan sonra koridor dalgalarını toplamayı bırakıp sürekli kavga arıyor (100 CS, 102 CS, 53 CS); altın geri kaldığı için <em>Low Damage</em> etiketi alıyor.",
        "<strong>Jhin ve MF'ye İlk Eşya Hubris (Kibir) Çıkma Hatası:</strong> Kritik vuruş nişancılarına suikastçı eşyası <em>Hubris</em> çıktığında %0 kritik şansıyla tanklara hasar vuramıyor.",
        "<strong>Aşırı Ölüm ve Suikastçı/Kritik Denemeleri:</strong> Son Esnek maçlarında Jhin ile 3/20/7, Miss Fortune ile 11/17/17 gibi çok yüksek ölüm sayılarına çıktı; ayrıca Garen'e <em>Hayalet Dansçı + A.M.K. Kılıcı</em> çıkıp 4/13/4 veya Zed alıp 0/7/2 oynadığı maçlar var."
      ],
      fix: [
        "<strong>Jhin Doğru Eşya Sırası:</strong> Hubris'i tamamen bırakıp <strong>1. Tahsildar → 2. Atiklik Çizmesi → 3. Ebedi Kılıç → 4. Bombardıman Topu → 5. Dominik Efendi'nin Hürmetleri</strong> dizilimini sabitle.",
        "<strong>Miss Fortune Doğru Eşya Sırası:</strong> <strong>1. Tahsildar (veya Kanlı Kılıç) → 2. Savaşçı Çizmeleri → 3. Ebedi Kılıç → 4. Dominik Efendi'nin Hürmetleri</strong> sırasından şaşma.",
        "<strong>Orta Oyunda En Az 5.5 CS/dk Kuralı ve Garen Dövüşçü Dizilimi:</strong> Dakika 15 sonrası orta koridorda boş beklemek yerine yan koridor dalgalarını temizle; Garen oynarken kritik yerine <strong>Hızkesen → Kara Balta → Ölü Adamın Zırhı</strong> çık."
      ],
      builds: [
        {
          champ: "Jhin",
          note: "ADC · 4. Mermi Kritik İnfazcısı (13B Ustalık)",
          variants: [
            {
              title: "Standart Kritik & Yakalama Dizilimi (Hubris Yok!)",
              kind: "standard",
              enemies: "Tüm takım kompozisyonlarına karşı ana dizilim",
              keystone: "Çevik Ayak İzi",
              runes: ["Şifa Taşkını", "Efsane: Kan", "Son Darbe", "Sürat", "Yaklaşan Fırtına"],
              spells: ["Sıçra + Şifa"],
              items: [
                { name: "Tahsildar", note: "Erken hasar + %25 kritik" },
                { name: "Atiklik Çizmesi", note: "Kite + hareket hızı" },
                { name: "Ebedi Kılıç", note: "4. mermi dev kritik" },
                { name: "Bombardıman Topu", note: "Uzaktan güvenli vuruş" },
                { name: "Dominik Efendi'nin Hürmetleri", note: "%Zırh delme" }
              ]
            }
          ]
        },
        {
          champ: "Miss Fortune",
          note: "ADC · Alan Hasarı & Ulti Kombo (8.6B Ustalık)",
          variants: [
            {
              title: "Seraphine & Veigar İle Tam Kombo (Kritik + Zırh Deşme)",
              kind: "standard",
              enemies: "Takım savaşı ve dar koridor kavgaları",
              keystone: "İlk Vuruş",
              runes: ["Sihirli Pabuçlar", "Üçlü Tonik", "Kozmik Sezgi", "Mana Akışı Yüzüğü", "Yaklaşan Fırtına"],
              spells: ["Sıçra + Şifa"],
              items: [
                { name: "Tahsildar", note: "Ultide %5 can infazı" },
                { name: "Savaşçı Çizmeleri", note: "Saldırı hızı" },
                { name: "Ebedi Kılıç", note: "Kritik Q ve R hasarı" },
                { name: "Dominik Efendi'nin Hürmetleri", note: "Tank eritme" },
                { name: "Kanlı Kılıç", note: "Can çalma + kalkan" }
              ]
            }
          ]
        },
        {
          champ: "Garen",
          note: "Top · Dövüşçü & Ön Saf (13B Ustalık)",
          variants: [
            {
              title: "Doğru Dövüşçü Dizilimi (Hayalet Dansçı Yok!)",
              kind: "danger",
              enemies: "Üst koridor yakın dövüşçüleri ve menzilli rakipler",
              keystone: "Yenilmez",
              runes: ["Zafer", "Efsane: Çeviklik", "Son Direniş", "İkinci Şans", "Aşırı Büyüme"],
              spells: ["Sıçra + Tutuştur"],
              items: [
                { name: "Hızkesen", note: "Rakibi yavaşlatıp E döndürme" },
                { name: "Çelik Kaplamalı / Savaşçı Çizmesi", note: "Duruma göre bot" },
                { name: "Kara Balta", note: "E ile anında zırh kırma" },
                { name: "Ölü Adamın Zırhı", note: "Hareket hızı + zırh" },
                { name: "Sterak / Doğanın Kudreti", note: "Büyü direnci + kalkan" }
              ]
            }
          ]
        }
      ],
      matches: [
        {
          date: "2026-10-24",
          queue: "Normal",
          champ: "Miss Fortune",
          role: "ADC",
          result: "loss",
          kda: "11/8/10",
          cs: 141,
          duration: null,
          items: [],
          verdict: "l4cg (Veigar) ile girilen maçta 11 kill ve 10 asist üretilse de geç oyunda maç tutulamadı.",
          premade: ["l4cg"]
        },
        {
          date: "2026-10-24",
          queue: "Esnek",
          champ: "Jhin",
          role: "ADC",
          result: "loss",
          kda: "3/20/7",
          cs: 168,
          duration: null,
          items: [
            { name: "Kibir (Hubris)", flag: "bad" }
          ],
          verdict: "20 kez ölerek pozisyon hatası yapılan ve kritik eşya eksikliği yüzünden hasarın yetmediği ağır Esnek yenilgisi.",
          premade: ["l4cg", "patrick"]
        },
        {
          date: "2026-10-24",
          queue: "Esnek",
          champ: "Miss Fortune",
          role: "ADC",
          result: "win",
          kda: "11/17/17",
          cs: 145,
          duration: null,
          items: [],
          verdict: "17 kez ölünmesine rağmen takım savaşlarında 28 skor katkısı (11 kill, 17 asist) vererek Veigar ve Rengar'la maçı kazandı.",
          premade: ["l4cg", "patrick"]
        },
        {
          date: "2026-10-24",
          queue: "Normal",
          champ: "Miss Fortune",
          role: "ADC",
          result: "win",
          kda: "9/11/3",
          cs: 53,
          duration: null,
          items: [],
          verdict: "Patrick (Rengar 8/4/5) ile girilen hızlı maçta 9 kill alındı ancak 53 CS ile minyon takibi düşük kaldı.",
          premade: ["patrick"]
        },
        {
          date: "2026-10-24",
          queue: "Normal",
          champ: "Zed",
          role: "Mid",
          result: "loss",
          kda: "0/7/2",
          cs: 63,
          duration: null,
          items: [],
          verdict: "Alışık olmadığı suikastçı Zed denemesinde 0/7/2 ve 63 CS ile koridor aşamasında ezildi.",
          premade: ["patrick"]
        },
        {
          date: "2026-10-23",
          queue: "Esnek",
          champ: "Jhin",
          role: "ADC",
          result: "win",
          kda: "4/9/13",
          cs: 162,
          duration: null,
          items: [
            { name: "Kibir (Hubris)", flag: "bad" }
          ],
          verdict: "l4cg'nin Seraphine (21 asist) kitle kontrolü üstüne W ve R takibiyle 17 skor katkısı vererek kazandı.",
          premade: ["l4cg", "minte"]
        },
        {
          date: "2026-10-23",
          queue: "Esnek",
          champ: "Miss Fortune",
          role: "ADC",
          result: "win",
          kda: "4/9/15",
          cs: 100,
          duration: null,
          items: [
            { name: "Kibir (Hubris)", flag: "bad" }
          ],
          verdict: "100 CS'de kalmasına rağmen Seraphine ve Briar kombosunun üstüne attığı ultilerle 15 asist topladı.",
          premade: ["l4cg", "minte"]
        },
        {
          date: "2026-10-23",
          queue: "Esnek",
          champ: "Miss Fortune",
          role: "ADC",
          result: "loss",
          kda: "5/9/13",
          cs: 102,
          duration: null,
          items: [],
          verdict: "15. dakikadan sonra minyon kesmeyi bırakınca (102 CS) eşya olarak geride kaldı.",
          premade: ["l4cg", "minte"]
        },
        {
          date: "2026-10-22",
          queue: "Normal",
          champ: "Garen",
          role: "Top",
          result: "win",
          kda: "2/5/10",
          cs: 80,
          duration: null,
          items: [],
          verdict: "Patrick'in 20/4/1 Yasuo şov yaptığı maçta 10 asistle takıma eşlik etti.",
          premade: ["patrick"]
        },
        {
          date: "2026-10-22",
          queue: "Normal",
          champ: "Garen",
          role: "Top",
          result: "loss",
          kda: "4/13/4",
          cs: 68,
          duration: null,
          items: [
            { name: "Hayalet Dansçı", flag: "bad" },
            { name: "A.M.K. Kılıcı", flag: "bad" }
          ],
          verdict: "Garen'e tank/dövüşçü yerine kritik ve saldırı hızı çıkınca 13 kez ölerek koridoru kaybetti.",
          premade: ["patrick"]
        }
      ]
    },
    patrick: {
      riotId: "Patrick Cem#OMEN",
      tag: "395 Sv. Kelle Ödülü Vakfı",
      summary: "395 hesap seviyesi, sezonda 507 maç (71 Tek/Çift + 436 Esnek) ve kağıt üstünde Altın III (Tek/Çift 20 LP · Esnek 75 LP). 46 ve 30 seviyeli Demir/Bronz arkadaşlarının lobisine girdiğinde beklenti vadide terör estirmesi; gerçekteyse 1.65 sezon KDA'sı (8.1 kill / 8.4 ölüm), %49 Esnek WR'si (213G 223M) ve 36 kill aldığı Rengar maçında bile 20 kere ölerek karşı takımı ihya etmesi.",
      kpis: [
        { val: "Beklenen: 4+ KDA", lbl: "Gerçek: 1.65 Sezon (Son 20: 1.86)" },
        { val: "8.4 Ölüm/Maç", lbl: "507 Sezon Maçı (8.1 Kill / 8.4 Ölüm)" },
        { val: "%49 WR", lbl: "436 Esnek Maçı (213G 223M · Altın III)" },
        { val: "395 Sv.", lbl: "287B Vayne · 271B Zed · 203B Yasuo" },
        { val: "%37 KP", lbl: "Son 20 Maç Skor Katkısı (%55 WR)" }
      ],
      good: [
        "<strong>Demir Lobisinde Karın Doyuran Mekanik Tavan:</strong> 395 seviyenin hakkını nadiren hatırladığında Esnek'te Rengar ile <strong>28/10/6 (298 CS)</strong> ve <strong>36/20/6 (388 CS)</strong>, Normal maçta Yasuo ile <strong>20/4/1</strong> kesebiliyor — tabii 36 kill'in yanına 20 ölümü sıkıştırıp bütün haritaya hayır hasenat dağıtmasa tam taşıyacak.",
        "<strong>500 Maçta Tutturduğu İki İstatistik:</strong> 162 maç Vayne (%54 WR, 6.7 CS/dk) ve 9 maç Gnar (%56 WR, 7.8 CS/dk) oynarken minyon kesmeyi unutmuyor; Cho'Gath (<strong>14/12/15, 252 CS</strong>) aldığında da 12 kez ölmesine rağmen etten duvar olup l4cg ve Swag'e nefes aldırıyor."
      ],
      bad: [
        "<strong>400 Level'lık Hesapla Demir/Bronz Lobisine Feed:</strong> Altın III apoletiyle girdiği maçlarda beklenti koridoru 10 dakikada kapatmasıyken; Tek/Çift'te Ekko ile <strong>2/10/1 (OP Score 1.4 — Maç 10.'su!)</strong>, 203.223 ustalık puanlı Yasuo'suyla <strong>3/12/14 (OP Score 3.9 — Maç 7.'si)</strong> oynayarak adeta 'ustalık puanı var, oyun bilgisi yok' dersi veriyor.",
        "<strong>Yürüyen Kelle Ödülü (Shutdown) Bankası:</strong> Sezon genelinde 507 maçta maç başı <strong>8.1 kill alıp 8.4 kez ölüyor</strong> (1.65 KDA). 24 Ekim Esnek maçında Rengar ile <strong>36 kill ve 388 CS</strong> yapıp <strong>20 kez ölerek</strong> rakip takıma binlerce altınlık <em>Shutdown</em> ikram etti ve 36 kill'li maçı kaybettirmeyi başardı.",
        "<strong>436 Esnek Maçında Negatif Winrate (%49 WR):</strong> Bütün sezonu Esnek kademesinde (213G 223M) geçirip hâlâ %50'nin altında kalmak büyük istikrar; son 20 maçta da sadece <strong>%37 skor katkısı (KP)</strong> ile takım savaşları yerine haritanın öbür ucunda 1v3 av peşinde koşuyor.",
        "<strong>287B Ustalıklı Üst Koridor Vayne Sendromu:</strong> Takımda zaten Veigar/Xerath ve Jhin/MF gibi kırılganlar varken üst koridora inatla 162 maç Vayne veya suikastçı çekip ön safı bomboş bırakıyor; girdiği son Vayne maçından da <strong>10/7/6</strong> mağlubiyetle çıktı.",
        "<strong>Son 10 Maçta 98 Ölüm (Maç Başı 9.8 Ölüm!):</strong> Son 10 maçının sadece 2'sinde (20/4/1 Yasuo ve 8/4/5 Rengar) 6'nın altında öldü; geri kalanlarda <strong>20, 12, 12, 10, 10, 7, 7, 6 ölüm</strong> dizerek gri ekran izleme rekoru kırdı."
      ],
      fix: [
        "<strong>395 Seviye Gibi Oyna, Kelle Ödülünü Bağışlama:</strong> Rengar veya Yasuo ile 10+ kill'e ulaştığında üzerinde <strong>1000 altınlık Shutdown</strong> varken karanlık ormana 1v3 atlamayı bırak; 3. veya 4. eşyada <strong>Ölümün Dansı / Koruyucu Melek / Sterak'ın Güvencesi</strong> alıp Baron ve Ejder etrafında oyna.",
        "<strong>5'li Esnekte Ön Saf (Tank/Dövüşçü) Zorunluluğu:</strong> Ormanda Minte (Briar), ortada l4cg (Veigar/Xerath) ve altta Swag (Jhin/MF) varken üst koridora Vayne veya suikastçı çekme; <strong>Cho'Gath, Darius (%60 WR), Garen (%60 WR) veya Gnar (7.8 CS/dk)</strong> alıp takımın ön safını tut.",
        "<strong>%37 Skor Katkısını %55+ Seviyesine Çıkar:</strong> Dakika 20'den sonra yan koridorda tek başına yakalanıp 40 saniye gri ekran beklemek yerine <em>Işınlanma</em> veya ulti temposunu takımın kitle kontrolüyle (Seraphine R / Veigar E) birleştir.",
        "<strong>0/2 Başladığın Koridorda Freni Bul:</strong> Ekko (2/10/1) ve Yasuo (3/12/14) maçlarındaki gibi ilk iki ölümden sonra hâlâ kule altına dalmak yerine minyonu kulenin önünde dondur ve ormancıyı bekle."
      ],
      builds: [
        {
          champ: "Vayne",
          note: "Top / ADC · 287B Ustalık (162 Maç %54 WR — Ön Safımız Yokken Alma!)",
          variants: [
            {
              title: "Üst Koridor & Geç Oyun İsabet (On-Hit) Dizilimi",
              kind: "standard",
              enemies: "Tanklar ve hantal üst koridor dövüşçüleri",
              keystone: "Ölümcül Tempo",
              runes: ["Zafer", "Efsane: Çeviklik", "Son Direniş", "Kemik Zırh", "Aşırı Büyüme"],
              spells: ["Sıçra + Hayalet"],
              items: [
                { name: "Mahvolmuş Kralın Kılıcı", note: "Can çalma + %can hasarı" },
                { name: "Savaşçı Çizmeleri", note: "Saldırı hızı" },
                { name: "Guinsoo'nun Hiddeti", note: "Çift Gümüş Ok tetiklemesi" },
                { name: "Sonlandırma (Terminus)", note: "Zırh/büyü direnci + delme" },
                { name: "Jak'Sho, Çok Yüzlü", note: "Takım savaşında tek yememe sigortası" }
              ]
            }
          ]
        },
        {
          champ: "Yasuo",
          note: "Mid / Top · 203B Ustalık (50 Maç %56 WR — 0/10 Güç Patlaması Garantili)",
          variants: [
            {
              title: "Standart Kritik & Hayatta Kalma Dizilimi (3/12 Oynamamak İçin)",
              kind: "standard",
              enemies: "Menzilli büyücüler ve dövüşçüler",
              keystone: "Ölümcül Tempo",
              runes: ["Emici Hayat", "Efsane: Çeviklik", "Son Direniş", "İkinci Şans", "Yeşeren Can"],
              spells: ["Sıçra + Tutuştur"],
              items: [
                { name: "Savaşçı Çizmeleri", note: "Q bekleme süresi" },
                { name: "Mahvolmuş Kralın Kılıcı", note: "Düello + yavaşlatma" },
                { name: "Ölümsüz Kalkanyay", note: "%100 kritik + kalkan" },
                { name: "Ebedi Kılıç", note: "Maksimum kritik hasarı" },
                { name: "Ölümün Dansı / Koruyucu Melek", note: "Shutdown vermemek için şart" }
              ]
            }
          ]
        },
        {
          champ: "Cho'Gath",
          note: "Top · Dev Ön Saf Tankı (Ekibin Gerçekten İhtiyacı Olan Çar)",
          variants: [
            {
              title: "Tam Tank & Takım Koruması",
              kind: "danger",
              enemies: "Premade maçlarda takıma ön saf gerektiğinde",
              keystone: "Hortlağın Pençesi",
              runes: ["Tahrip", "İkinci Şans", "Aşırı Büyüme", "Yaklaşım Hızı", "Bisküvi Teslimatı"],
              spells: ["Sıçra + Işınlanma"],
              items: [
                { name: "Çelik Yürek", note: "Sonsuz can + ulti hasarı" },
                { name: "Çelik Kaplamalı / Merkür Çizmesi", note: "Rakibe göre direnç" },
                { name: "Günateşi Kalkanı / Oklukır", note: "Dalga itme + zırh" },
                { name: "Kaenic Rookern", note: "Büyücülere karşı dev kalkan" },
                { name: "Jak'Sho, Çok Yüzlü", note: "Çift direnç katlama" }
              ]
            }
          ]
        }
      ],
      matches: [
        {
          date: "2026-10-24",
          queue: "Esnek",
          champ: "Rengar",
          role: "Jungle",
          result: "loss",
          kda: "36/20/6",
          cs: 388,
          duration: null,
          items: [],
          verdict: "36 kill ve 388 CS ile maçın 1.'si (OP Score 6.6) olsa da 20 kez ölünce verilen kelle ödülleri ve arka safın (Xerath 10/23, Jhin 3/20) erimesiyle maç kaybedildi.",
          premade: ["l4cg", "swag"]
        },
        {
          date: "2026-10-24",
          queue: "Esnek",
          champ: "Rengar",
          role: "Jungle",
          result: "win",
          kda: "28/10/6",
          cs: 298,
          duration: null,
          items: [],
          verdict: "28 kill ve 298 CS (OP Score 7.8) ile l4cg'nin Veigar'ı ve Swag'in Miss Fortune'uyla birlikte maçı domine etti.",
          premade: ["l4cg", "swag"]
        },
        {
          date: "2026-10-24",
          queue: "Normal",
          champ: "Rengar",
          role: "Jungle",
          result: "win",
          kda: "8/4/5",
          cs: 141,
          duration: null,
          items: [],
          verdict: "Swag (Miss Fortune 9/11/3) ile girilen hızlı maçta 3.25 KDA ile temiz bir galibiyet aldı.",
          premade: ["swag"]
        },
        {
          date: "2026-10-24",
          queue: "Normal",
          champ: "Rengar",
          role: "Jungle",
          result: "loss",
          kda: "7/6/3",
          cs: 92,
          duration: null,
          items: [],
          verdict: "Swag'in 0/7/2 Zed oynadığı kısa maçta orta koridor çökünce oyun erken koptu.",
          premade: ["swag"]
        },
        {
          date: "2026-10-23",
          queue: "Dereceli Tek/Çift",
          champ: "Cho'Gath",
          role: "Top",
          result: "win",
          kda: "14/12/15",
          cs: 252,
          duration: null,
          items: [],
          verdict: "252 CS ve 29 skor katkısıyla üst koridorda devleşerek Tek/Çift maçını taşıdı.",
          premade: []
        },
        {
          date: "2026-10-23",
          queue: "Dereceli Tek/Çift",
          champ: "Yasuo",
          role: "Top",
          result: "win",
          kda: "3/12/14",
          cs: 162,
          duration: null,
          items: [],
          verdict: "Koridorda zorlanıp 12 kez ölse de takım savaşlarında 14 asist üreterek galibiyete katkı verdi.",
          premade: []
        },
        {
          date: "2026-10-23",
          queue: "Dereceli Tek/Çift",
          champ: "Vayne",
          role: "Top",
          result: "loss",
          kda: "10/7/6",
          cs: 171,
          duration: null,
          items: [],
          verdict: "10 kill ve 171 CS ile iyi dirense de takımın geri kalanı düşünce mağlup oldu.",
          premade: []
        },
        {
          date: "2026-10-22",
          queue: "Dereceli Tek/Çift",
          champ: "Ekko",
          role: "Mid",
          result: "loss",
          kda: "2/10/1",
          cs: 117,
          duration: null,
          items: [],
          verdict: "Erken oyunda geri düşüp 10 ölüm verince harita etkisi kuramadı.",
          premade: []
        },
        {
          date: "2026-10-22",
          queue: "Normal",
          champ: "Yasuo",
          role: "Mid",
          result: "win",
          kda: "20/4/1",
          cs: 129,
          duration: null,
          items: [],
          verdict: "Swag (Garen 2/5/10) ile girilen maçta 20 kill ve 5.25 KDA ile rakibi tek başına süpürdü.",
          premade: ["swag"]
        },
        {
          date: "2026-10-22",
          queue: "Normal",
          champ: "Yasuo",
          role: "Mid",
          result: "loss",
          kda: "10/7/6",
          cs: 142,
          duration: null,
          items: [],
          verdict: "Swag'in kritik Garen (4/13/4) denediği maçta 10 kill almasına rağmen üst koridor farkı kapanmadı.",
          premade: ["swag"]
        }
      ]
    }
  },
  premade: {
    summary: "Son 10'ar maçlık kesitte tespit edilen 11 ortak premade maçta ekip %55 galibiyet oranı (6G 5M; Esnek kademesinde 6 maçta 4G 2M · %67 WR) yakaladı. Ormanda Minte (Briar) veya Patrick (Rengar) skor yükünü çekerken l4cg'nin Seraphine/Veigar/Xerath kitle kontrolü ve Swag'in MF/Jhin ulti takibi Esnek maçlarını kazandırıyor.",
    kpis: [
      { val: "%67", lbl: "Esnek Premade WR (4G 2M)" },
      { val: "%55", lbl: "Toplam Premade WR (6G 5M)" },
      { val: "+%10", lbl: "30. Dakika Sonrası WR Artışı" },
      { val: "11 Maç", lbl: "İncelenen Ortak Maç" }
    ],
    good: [
      "<strong>Briar + Seraphine/Xerath + MF/Jhin Sinerjisi:</strong> Minte'nin 23/5/7 ve 14/3/5 oynadığı Briar maçlarında l4cg'nin 20+ asistlik Seraphine/Xerath desteği ve Swag'in uzaktan ulti takibi Esnek maçlarını rahat kazandırıyor.",
      "<strong>Geç Oyun Geri Dönüş Gücü (30+ Dakika +%10 WR):</strong> Takımda Veigar, Xerath, Seraphine ve Briar/Rengar bulunduğundan 25. dakikayı geçen maçlarda tek bir takım savaşıyla 1000 altınlık kelle ödüllerini (<em>Shutdown</em>) toplayıp oyunu çevirebiliyorlar.",
      "<strong>Esnek Kademesinde Yüksek Uyum:</strong> Son 6 Dereceli Esnek ortak maçının 4'ü kazanıldı (%67 WR); özellikle 3'lü premade (l4cg + minte + swag ve l4cg + swag + patrick) kurgularında skor paylaşımı çok dengeli."
    ],
    bad: [
      "<strong>Aşırı Ölüm ve Cam Topu Dizilimleri:</strong> Kaybedilen 24 Ekim Esnek maçında l4cg (10/23/12), Swag (3/20/7) ve Patrick (36/20/6) toplamda <strong>63 kez öldü</strong>; savunma eşyası çıkmamak (Zhonya/Banshee/Ölümün Dansı eksikliği) öndeki maçları bile riske atıyor.",
      "<strong>Ana Rol Dışı Denemeler:</strong> Minte'nin orman yerine Mordekaiser Top (4/13/5) veya Swag'in ADC yerine Zed Mid (0/7/2) ve kritik Garen (4/13/4) denediği maçlar doğrudan mağlubiyetle sonuçlanıyor.",
      "<strong>20. Dakika Erken FF Sendromu:</strong> Bir koridor 0/7 başladığında 20. dakikada erken teslim oylaması başlatılıyor (20 dk WR: -%9 ile -%13 arası), oysa ekibin asıl gücü 30. dakikada açılıyor."
    ],
    fix: [
      "<strong>İdeal 4'lü / 5'li Premade Rol Dağılımı:</strong> <strong>Top:</strong> Patrick Cem (Cho'Gath / Gwen / Darius / Vayne) · <strong>Jungle:</strong> minte (Briar / Diana / Amumu) · <strong>Mid:</strong> l4cg (Veigar / Xerath) · <strong>ADC:</strong> swagisback (Jhin / Miss Fortune) · <strong>Support:</strong> l4cg (Seraphine) veya Patrick (Pyke).",
      "<strong>25. Dakikayı Görmeden FF Vermemek:</strong> Demir–Altın eloda karşı takım 7/0 olsa bile kule altına tek başına girip kelle ödülü veriyor; Veigar kafesi + Seraphine Rylai E'si + Briar/Rengar atlamasıyla o hedefi 1 kez kesip oyunu çevirin.",
      "<strong>Eşya Disiplini ve Kontrol Totemi:</strong> Swag Jhin/MF'de <em>Hubris</em> yerine <strong>Tahsildar + Ebedi Kılıç</strong> çıkacak; l4cg Veigar'da <strong>Başmelek Asası</strong> ve Seraphine'de <strong>Gündönümü Kızağı + Rylai</strong> alacak; herkes Baron/Ejder öncesi 1 Pembe Totem taşıyacak."
    ],
    matches: [
      {
        date: "2026-10-24",
        queue: "Normal",
        result: "loss",
        duration: null,
        players: [
          { key: "l4cg", champ: "Veigar", role: "Mid", kda: "8/7/12", cs: 154 },
          { key: "swag", champ: "Miss Fortune", role: "ADC", kda: "11/8/10", cs: 141 }
        ],
        verdict: "l4cg ve Swag ikilisi toplam 19 kill üretse de orta oyundaki takım savaşlarında ön saf eksikliği yüzünden maç kaybedildi."
      },
      {
        date: "2026-10-24",
        queue: "Esnek",
        result: "loss",
        duration: null,
        players: [
          { key: "patrick", champ: "Rengar", role: "Jungle", kda: "36/20/6", cs: 388 },
          { key: "l4cg", champ: "Xerath", role: "Mid", kda: "10/23/12", cs: 271 },
          { key: "swag", champ: "Jhin", role: "ADC", kda: "3/20/7", cs: 168 }
        ],
        verdict: "Patrick Rengar ile 36 kill ve 388 CS'e ulaştı ancak üçlünün toplam 63 ölümü (Xerath 23, Jhin 20, Rengar 20 ölüm) geç oyunda uzun dirilme süreleriyle maçı kaybettirdi."
      },
      {
        date: "2026-10-24",
        queue: "Esnek",
        result: "win",
        duration: null,
        players: [
          { key: "patrick", champ: "Rengar", role: "Jungle", kda: "28/10/6", cs: 298 },
          { key: "l4cg", champ: "Veigar", role: "Mid", kda: "14/12/14", cs: 247 },
          { key: "swag", champ: "Miss Fortune", role: "ADC", kda: "11/17/17", cs: 145 }
        ],
        verdict: "Patrick (28 kill) ve l4cg (14 kill, 247 CS) geç oyunda muazzam hasara ulaştı; Veigar kafesi üstüne Miss Fortune ultisiyle takım savaşları kazanıldı."
      },
      {
        date: "2026-10-24",
        queue: "Normal",
        result: "win",
        duration: null,
        players: [
          { key: "patrick", champ: "Rengar", role: "Jungle", kda: "8/4/5", cs: 141 },
          { key: "swag", champ: "Miss Fortune", role: "ADC", kda: "9/11/3", cs: 53 }
        ],
        verdict: "Patrick'in Rengar baskınları ve Swag'in erken skorlarıyla hızlı kopan galibiyet."
      },
      {
        date: "2026-10-24",
        queue: "Normal",
        result: "loss",
        duration: null,
        players: [
          { key: "patrick", champ: "Rengar", role: "Jungle", kda: "7/6/3", cs: 92 },
          { key: "swag", champ: "Zed", role: "Mid", kda: "0/7/2", cs: 63 }
        ],
        verdict: "Swag'in Zed denemesi 0/7/2 ile sonuçlanınca Patrick'in 7 kill'lik Rengar çabası yetmedi."
      },
      {
        date: "2026-10-23",
        queue: "Esnek",
        result: "win",
        duration: null,
        players: [
          { key: "l4cg", champ: "Seraphine", role: "Support", kda: "3/10/21", cs: 50 },
          { key: "swag", champ: "Jhin", role: "ADC", kda: "4/9/13", cs: 162 },
          { key: "minte", champ: "Cho'Gath", role: "Top", kda: "7/13/6", cs: 206 }
        ],
        verdict: "Minte Cho'Gath ile önde hasarı emerken l4cg (21 asist Seraphine) ve Swag (Jhin 162 CS) arka saftan kitle kontrol zinciriyle maçı çevirdi."
      },
      {
        date: "2026-10-23",
        queue: "Esnek",
        result: "win",
        duration: null,
        players: [
          { key: "minte", champ: "Briar", role: "Jungle", kda: "14/3/5", cs: 204 },
          { key: "l4cg", champ: "Seraphine", role: "Support", kda: "5/4/20", cs: 31 },
          { key: "swag", champ: "Miss Fortune", role: "ADC", kda: "4/9/15", cs: 100 }
        ],
        verdict: "İmza üçlü kombo: Minte (14/3/5 Briar) içeri uçtu, l4cg (5/4/20 Seraphine) kalkan ve ultiyle rakipleri mıhladı, Swag MF ultisiyle süpürdü."
      },
      {
        date: "2026-10-23",
        queue: "Esnek",
        result: "loss",
        duration: null,
        players: [
          { key: "l4cg", champ: "Veigar", role: "Mid", kda: "9/11/6", cs: 184 },
          { key: "swag", champ: "Miss Fortune", role: "ADC", kda: "5/9/13", cs: 102 },
          { key: "minte", champ: "Mordekaiser", role: "Top", kda: "4/13/5", cs: 149 }
        ],
        verdict: "Minte orman yerine üst koridor Mordekaiser'e geçip 13 kez ölünce ve Veigar savunmasız yakalanınca harita kontrolü kaybedildi."
      },
      {
        date: "2026-10-22",
        queue: "Normal",
        result: "win",
        duration: null,
        players: [
          { key: "patrick", champ: "Yasuo", role: "Mid", kda: "20/4/1", cs: 129 },
          { key: "swag", champ: "Garen", role: "Top", kda: "2/5/10", cs: 80 }
        ],
        verdict: "Patrick Yasuo ile 20/4/1 oynayarak maçı tek başına domine etti, Swag Garen ile 10 asist katkısı verdi."
      },
      {
        date: "2026-10-22",
        queue: "Normal",
        result: "loss",
        duration: null,
        players: [
          { key: "patrick", champ: "Yasuo", role: "Mid", kda: "10/7/6", cs: 142 },
          { key: "swag", champ: "Garen", role: "Top", kda: "4/13/4", cs: 68 }
        ],
        verdict: "Swag'in kritik Garen dizilimi 4/13/4 ile çökünce Patrick'in 10 kill'lik Yasuo performansı galibiyete yetmedi."
      },
      {
        date: "2026-10-22",
        queue: "Esnek",
        result: "win",
        duration: null,
        players: [
          { key: "minte", champ: "Briar", role: "Jungle", kda: "23/5/7", cs: 266 },
          { key: "l4cg", champ: "Xerath", role: "Support", kda: "3/5/10", cs: 137 }
        ],
        verdict: "Minte 23/5/7 ve 266 CS (OP Score 10) ile vadiyi yok ederken l4cg Xerath ile uzaktan 10 asistlik tam destek sağladı."
      }
    ]
  }
};
