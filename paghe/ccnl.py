class Ccnl:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')  # identificativo CCNL numerico
        self.ore_sett = kwargs.get('ore_sett')
        self.ore_ccnl = kwargs.get('ore_ccnl')
        self.gg_ccnl = kwargs.get('gg_ccnl')
        self.provincia = kwargs.get('provincia')
        self.mensilita = data[self.id]['mensilita']

    def importo_ordinario(self, **kwargs):
        """ Calcola la somma di minimo, contingenza (ex scala mobile) e terzo elemento """
        livello = kwargs.get('livello')
        parziale = data[self.id]['livelli'][livello]['minimo'] + data[self.id]['livelli'][livello]['contingenza']
        if self.provincia in data[self.id]['III elemento'].keys():
            parziale += data[self.id]['III elemento'][self.provincia]
        else:
            # fallback
            parziale += data[self.id]['III elemento'][0]
        return round(parziale, 2)

    def importo_straordinario_orario(self, **kwargs):
        """ Quanto cosa un'ora di lavoro straordinario del tipo specificato per il mese specificato? """
        livello = kwargs.get('livello')
        tipo = kwargs.get('tipo')  # es. '15%'
        return round(self.base_oraria(livello=livello) * data[self.id]['straordinario'][tipo], 5)

    def base_giornaliera(self, **kwargs):
        livello = kwargs.get('livello')
        return round(self.importo_ordinario(livello=livello) / self.gg_ccnl, 5)

    def base_oraria(self, **kwargs):
        livello = kwargs.get('livello')
        return round(self.importo_ordinario(livello=livello) / self.ore_ccnl, 5)




data = {
    # CCNL COMMERCIO #
    42: {
        'mensilita': 14,
        'livelli': {
            5: {'minimo': 965.32, 'contingenza': 521.94},
            4: {'minimo': 1068.46, 'contingenza': 524.22},
            3: {'minimo': 1235.39, 'contingenza': 527.90},
            2: {'minimo': 1445.37, 'contingenza': 532.54},
            1: {'minimo': 1670.94, 'contingenza': 537.52}
        },
        'III elemento': {
            'Torino': 6.71,
            'Milano': 11.36,
            'Piacenza': 9.03,
            'Bergamo': 10.33,
            'Brescia': 8.78,
            'Como': 7.75,
            'Varese': 7.75,
            0: 2.07  # altre province
        },
        'straordinario': {
            '15%': 1.15,
            '35%': 1.35
        },
        'divisore fisso': 30,
    }
}
