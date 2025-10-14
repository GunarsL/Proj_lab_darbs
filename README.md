# 🧠 Proj_lab_darbs
Mācību kursa "Projektēšanas laboratorija(1),25/26-R" repozitorijas izveide.

# 🔍 Līdzīgo risinājumu pārskats

## 🏀 Rithmm — AI NBA izvēles un personalizēti modeļi
**Ko dara:** Rithmm piedāvā AI ģenerētas izvēles NBA (un citos sportos) ar uzvaras varbūtībām, gaidāmo iznākumu un tirgus koeficientus. Ir arī **Model Builder** — rīks, kur var salikt savu prognožu modeli bez koda.

**Kā strādā:** uzņēmums skaidro, ka AI modeļi ir apmācīti uz vairāku gadu NBA datiem un **simulē spēles tūkstošiem reižu**, iekļaujot spēlētāju statistiku, spēles kontekstu, traumas, vēsturisko sniegumu u.c.

**Ko saņem lietotājs:** dienas labākos AI izvēli, **varbūtības** (piem., uzvaras procents), gaidāmo rezultātu, kā arī **paskaidrojumu**, kāpēc izvēle ir vērtīga (salīdzinājumā ar tirgu).


## ⚙️ Dimers — simulāciju dzinējs pret tirgu
**Ko dara:** Dimers rāda **uzvaras varbūtības katrai spēlei** un atrod situācijas, kur viņu aprēķinātās varbūtības **atšķiras no citu profesionāļu rezultātiem** (tas ir, atrod vērtību).

**Kā strādā:** DimersBOT **veic vairāk nekā 10 000 simulācijas uz notikumu**, izmanto datus/analītiku, un pēc simulācijām izceļ labākos tirgus (moneyline, spread, totals, props u.c.).

**Ko saņem lietotājs:** spēļu lapās — varbūtības, ieteiktie “best bets”, salīdzinājums ar dažādu totalizatoru koeficientiem, trendi un projekcijas.


## 📊 Wise Prediction — AI “dashboard” ar vairākām līgām
**Ko dara:** Wise Prediction uztur **Basketbola prognožu paneli**, kurā redzamas ikdienas spēles ar AI ģenerētām prognozēm dažādās līgās (globāli).

**Kā strādā:** platforma norāda uz **mašīnmācīšanās** pamatotu analīzi un **ikdienas prognozēm**, kas balstās uz datu modeļiem (detalizācija nav publiski ļoti izvērsta, taču pozicionēts kā ML produkts).

**Ko saņem lietotājs:** centralizēts panelis ar **šodienas spēļu sarakstu**, rezultātu skatījumu.


## 🤖 Leans.AI — “REMI” AI picks ar "pārliecinātām" vienībām
**Ko dara:** Leans.AI katru dienu publicē AI ģenerētus variantus vairākiem sportiem, t.sk. **NBA** un **koledžu basketbolam (CBB)**; rāda **uzticamības (unit) reitingu** un piedāvā virkni skaidrojošu rakstu par AI metodēm.

**Kā strādā:** viņu modelis (“REMI”) **apkopo miljoniem datu punktu** no vēsturiskajiem un aktuālajiem avotiem, veic statistiskus aprēķinus/apmācības un **dinamiski atjaunojas**, lai ģenerētu izvēles ar norādītu uzvaras % diapazonu. (Konkrētas modeļu arhitektūras netiek atklātas.)

**Ko saņem lietotājs:** bezmaksas dienas izvēles variantus + abonementā pilns klāsts (vairāki izvēļu varianti, confidence units, prop/parlay idejas, e‑pasta piegāde).


## 📈 ATS Wins — tūkstošu simulāciju pieeja vairākām līgām
**Ko dara:** ATS Wins ir **AI vadīta prognožu platforma**, kas sedz NBA un citas lielās līgas; nodrošina **projekcijas, player props, publisko likmju sadalījumu, ikdienas picks** un peļņas izsekošanas rīkus.

**Kā strādā:** platforma norāda, ka **katru dienu veic tūkstošiem simulāciju** dažādām līgām un apvieno **AI algoritmus ar ekspertu ieskatu**. (Metodes nav pilnībā atklātas, bet uzsvars uz simulācijām un datu apjomu.)

**Ko saņem lietotājs:** pieeju spēļu/propu **projekcijām un ieteikumiem** vienā vietā, ar fokusu uz lietošanas vienkāršību gan iesācējiem, gan “sporta entuziastiem”.

### 🧩 Kopsavilkums par līdzīgiem risinājumiem
Lielākoties visi risinājumi izmanto kaut kāda veida mākslīga intelekta vai algoritmu darbību, balstoties no vēsturisko datu apkopojuma. Tiek paredzēti rezultāti un sniegta papildus statistika.
No bezmaksas skatu punkta gandrīz nekas lietderīgs netiek sniegts un lielākoties ir jāveic ikmēneša maksas par šādiem pakalpojumiem.
Basketbola spēles ir sezonāls sporta veids, tāpēc lielākoties katrs līdzīgais risinājums piedāvā iespēju arī aplūkot citus sporta veidus un veikt prognozes ar AI modeļiem vai algoritmiem.
Netika atrasts specifiski vizuāls attēlojums grafa formā vai kaut kādos šablonos. Reti kurš risinājums sniedz padziļinātu statistiku par spēlēm nākošajo sezonu, pirms tā ir sākusies, kas visticamāk liecina, ka dati, kuri tiek atspoguļoti, sākotnēji tiek ievākti sezonu sākumos un tad salīdzināti ar vēsturiskajiem. Parastam lietotājam lielākoties interesētu tikai turnīru spēles jeb Finals, kur šie algoritmi jau ir satrennēti un ieguvuši lielu datu apjomu.

## 🧩 Konceptu modelis

![Konceptu modelis](/modelis.png)

*Attēls: Projekta konceptu modelis.*


## ⚙️ Tehnoloģiju steks

| Komponents | Tehnoloģija |
|-------------|--------------|
| **Serveris** | Azure |
| **Operētājsistēma** | Linux (Debian vai Ubuntu) |
| **Web serveris** | Apache vai Nginx |
| **Backend** | Python Flask |
| **Datubāze** | SQLAlchemy |
| **Frontend** | HTML, CSS, JavaScript |
| **Datu vizualizācija** | Chart.js |
