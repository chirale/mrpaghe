# mrpaghe
Fun with Italian payroll and taxation on individuals for educational purposes.

## Usage

```python
from paghe.cedolino import Cedolino
from paghe.ccnl import Ccnl
metalmeccanico = Ccnl(
    id=42, 
    ore_sett=40, 
    ore_ccnl=40, 
    gg_ccnl=26, 
    provincia="Torino"
)
maria_romano = Cedolino(ccnl=metalmeccanico, livello=4, giorni_mese=31, straord_15=0, straord_35=0, festivita_settimanale=0, festivita_domenicale=0)
```

## Example

![Example](https://github.com/chirale/mrpaghe/blob/main/mrpaghe.png)