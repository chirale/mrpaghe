# from paghe import ccnl


class Cedolino:

    detrazioni = {}
    ore_straord = {'15%': 0, '35%': 0}
    totale_detrazioni = 0

    def __init__(self, **kwargs):
        self.ccnl = kwargs.get('ccnl')  # istanza di Ccnl
        # Scaglioni IRPEF
        self.irpef_scaglione = (0, 0.23, 0.27, 0.38, 0.41, 0.43)
        self.livello = kwargs.get('livello')
        self.giorni_mese = kwargs.get('giorni_mese')  # Giorni totali del mese del Cedolino
        self.ore_straord['15%'] = kwargs.get('straord_15', 0)
        self.ore_straord['35%'] = kwargs.get('straord_35', 0)
        self.festivita_settimanale = kwargs.get('festivita_settimanale', 0)
        self.festivita_domenicale = kwargs.get('festivita_domenicale', 0)
        # Calcoli
        self.importo_ordinario = self.ccnl.importo_ordinario(livello=self.livello)
        # Calcolo straordinario
        self.importo_straordinario = 0
        for tipo in ['15%', '35%']:
            self.importo_straordinario += round(self.ccnl.importo_straordinario_orario(
                tipo=tipo,
                livello=self.livello
            ) * self.ore_straord[tipo], 2)
        self.importo_straordinario = round(self.importo_straordinario, 2)
        # Calcolo festività
        self.importo_festivita_settimanale = round(self.festivita_settimanale * self.ccnl.base_giornaliera(livello=self.livello), 2)
        self.importo_festivita_domenicale = round(self.festivita_domenicale * self.ccnl.base_giornaliera(livello=self.livello), 2)
        self.totale_competenze = round(self.importo_ordinario + self.importo_straordinario +
                                       self.importo_festivita_domenicale + self.importo_festivita_settimanale, 2)
        self.imponibile_previdenziale = round(self.totale_competenze, 0)
        self.ctr_previdenziale = round(self.imponibile_previdenziale * 0.0919, 2)
        self.tot_ctr_previd = self.ctr_previdenziale
        self.imponibile_fiscale = round(self.totale_competenze - self.tot_ctr_previd, 2)
        # Fisco
        self.irpef_lorda = self.calcola_irpef_lorda()
        self.reddito_complessivo_annuo = round(self.imponibile_fiscale * self.ccnl.mensilita, 2)
        # Detrazioni personali
        self.detrazioni['lav'] = self.calcola_detraz_lav()
        """
        # Detrazioni famigliari a carico
        # 1) Detrazioni coniuge
        self.detrazioni['coniuge'] = self.calcola_detraz_coniuge()
        # 2) Detrazioni figli
        self.detrazioni['figli'] = self.calcola_detraz_figli()
        # 3) Detrazioni altri famigliari
        self.detrazioni['altri fam'] = self.calcola_detraz_altri_fam()
        # self.irpef_netta = self.irpef_lorda - self.detraz_lav - - self.detraz_coniuge self.detraz_figli - self.detraz_altri_fam
        self.totale_detrazioni = 0
        """
        for k, v in self.detrazioni.items():
            self.totale_detrazioni += v
        self.irpef_netta = self.irpef_lorda - self.totale_detrazioni
        self.totale_trattenute = self.tot_ctr_previd + self.irpef_netta
        self.netto_a_pagare = round(self.totale_competenze - self.totale_trattenute, 0)
        self.arrotondamento = round(self.netto_a_pagare - (self.totale_competenze - self.totale_trattenute), 2)

    def calcola_irpef_lorda(self):
        """ Calcola l'IRPEF in base all'imponibile fiscale """
        if self.imponibile_fiscale < 1250:
            # I scaglione
            importo = self.imponibile_fiscale * self.irpef_scaglione[1]
        elif 1250 < self.imponibile_fiscale <= 2333.33:
            # II scaglione
            importo = round(1250 * self.irpef_scaglione[1], 2) + ((self.imponibile_fiscale - 1250) * self.irpef_scaglione[2])
        elif 2333.33 < self.imponibile_fiscale <= 4583.33:
            # III scaglione
            importo = round(1250 * self.irpef_scaglione[1], 2) + round((2333.33 - 1250) * self.irpef_scaglione[2], 2) + \
                      ((self.imponibile_fiscale - 2333.33) * self.irpef_scaglione[3])
        elif 4583.33 < self.imponibile_fiscale <= 6250:
            # IV scaglione
            importo = round(1250 * self.irpef_scaglione[1], 2) + round((2333.33 - 1250) * self.irpef_scaglione[2], 2) + \
                      round((4583.33 - 2333.33) * self.irpef_scaglione[3], 2) + \
                      ((self.imponibile_fiscale - 4583.33) * self.irpef_scaglione[4])
        elif self.imponibile_fiscale < 6250:
            # V scaglione
            importo = round(1250 * self.irpef_scaglione[1], 2) + round((2333.33 - 1250) * self.irpef_scaglione[2], 2) + \
                      round((4583.33 - 2333.33) * self.irpef_scaglione[3], 2) + \
                      ((6250 - 4583.33) * self.irpef_scaglione[4]) + (self.imponibile_fiscale - 6250) * self.irpef_scaglione[5]
        return round(importo, 2)

    def tronca_coeff_detraz(self, value):
        # 4 cifre dopo la virgola troncate
        return int((value * 10000)) / 10000

    def calcola_detraz_lav(self):
        if self.reddito_complessivo_annuo <= 8000:
            annuale = 1880  # in realtà non meno di 1380 T. indet. e 690 T. det.
        elif 8000 < int(self.reddito_complessivo_annuo) <= 28000:
            coefficiente = (28000 - self.reddito_complessivo_annuo) / 20000
            annuale = 978 + (902 * self.tronca_coeff_detraz(coefficiente))
        elif 28000 < int(self.reddito_complessivo_annuo) <= 55000:
            coefficiente = (55000 - self.reddito_complessivo_annuo) / 27000
            annuale = 978 + (self.tronca_coeff_detraz(coefficiente))
        elif int(self.reddito_complessivo_annuo) <= 55000:
            annuale = 0
        return round((annuale / 365) * self.giorni_mese, 2)

    def calcola_detraz_coniuge(self):
        if self.reddito_complessivo_annuo <= 15000:
            importo = 800 - (110 * (self.reddito_complessivo_annuo / 15000))
        elif 15000 < self.reddito_complessivo_annuo <= 40000:
            importo = 690
        elif 40000 < self.reddito_complessivo_annuo <= 80000:
            importo = 690 * (80000 - self.reddito_complessivo_annuo / 40000)
        else:
            importo = 0
        # Detrazioni aggiuntive
        if 29000 < self.reddito_complessivo_annuo <= 29200:
            importo += 10
        elif 29200 < self.reddito_complessivo_annuo < 34700:
            importo += 20
        elif 34700 < self.reddito_complessivo_annuo < 35000:
            importo += 30
        elif 35000 < self.reddito_complessivo_annuo < 35100:
            importo += 20
        elif 35100 < self.reddito_complessivo_annuo < 35200:
            importo += 10
        return importo

    def calcola_detraz_figli(self):
        pass