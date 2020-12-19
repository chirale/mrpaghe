# mrpaghe
Fun with Italian payroll and taxation on individuals for educational purposes.

## Usage

```python
from paghe.cedolino import Cedolino
from paghe.ccnl import Ccnl
commercio = Ccnl(
    id=42, 
    ore_sett=40, 
    ore_ccnl=40, 
    gg_ccnl=26, 
    provincia="Torino"
)
maria_romano = Cedolino(
    ccnl=commercio, 
    livello=4, 
    giorni_mese=31, 
    straord_15=0, # straordinario al 15%
    straord_35=0, # straordinario al 35%
    festivita_settimanale=0, 
    festivita_domenicale=0
)
```

## Agli italofoni

Questo è un esercizio nato per divertimento, senza pretese di precisione, aggiornamento o completezza. Esistono 
applicativi professionali a tal scopo.

Se però vuoi giocare con il calcolo dell'IRPEF, i livelli di CCNL e le bizzarrie del calendario sei nel posto giusto! 

L'idea di tradurre (alcune de)le complesse procedure per il calcolo dei cedolini in classi Python 3 è stata svilppata a 
margine di un corso [Forma.Temp](http://www.formatemp.it/) nel [2018](https://it.wikipedia.org/wiki/2018).

Buon divertimento!

## Variables

![Example](https://github.com/chirale/mrpaghe/blob/main/mrpaghe.png)
