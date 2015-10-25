#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 rguerra <rguerra@moxie>
#
# Distributed under terms of the MIT license.

"""

"""
from pepito.CFG import CFG

def generate(start_prod):
    cfg1 = CFG()
    cfg1.add_prod('T', 'frio| normal| calor')
    cfg1.add_weighted_prod('calor', 'calor_texto enfadado$0.40| calor_texto$0.6')
    cfg1.add_prod('calor_texto', 'insoportable calor| calorin| que calor infernal!| me quemo con este clima')
    cfg1.add_weighted_prod('frio', 'frio_texto asqueado$0.40| frio_texto$0.6')
    cfg1.add_prod('frio_texto', 'Vaya frío.| ¡Lo que vamos a tener que pagar de calefacción!| Llevo más capas que una lechuga.| Plan de sofá y mantita.| Esto es cosa del cambio climático.| Esto parece el Polo Norte.')

    cfg1.add_weighted_prod('brusco', 'brusco_texto$0.40| asqueado triste brusco_texto$0.6')
    cfg1.add_prod('brusco_texto', 'Que brusco cambio de temp| Como cambia la temperatura| Sube y Baja de temperatura')
    cfg1.add_weighted_prod('normal', 'alegre alegre alegre$0.8| #chillin$0.2')

    cfg1.add_prod('E', 'enamorado| enfadado| asqueado| triste| alegre| apagado| encendido')
    cfg1.add_weighted_prod('enamorado', '<3$37.5| ;-)$12.5| ;)$12.5| *-)$12.5| *)$12.5| ;-$12.5')
    cfg1.add_weighted_prod('enfadado', 'Arrrgh enfadado$0.2| :@$0.1| me pongo enfadado$0.3| >:($0.1| enfadado enfadado$0.1| toy enfadado$0.2')
    cfg1.add_prod('asqueado', '>:O| :-O| :O| :-o| :o')
    cfg1.add_prod('triste', ':<| :-[| :[| :{')
    cfg1.add_prod('alegre', ':-)| :)| :D| :o)| :]| :3| :c)| :>| =]| 8)| =)| :}| :^)')
    cfg1.add_prod('apagado', ':-X| :X| :-#| :#| :-&| :&')
    cfg1.add_prod('encendido', '%-)| %)| #-)')
    cfg1.add_prod('asustado', 'encendido apagado| asqueado')

    cfg1.add_prod('lugar', 'ya habeis oido hablar de| Un nuevo sitio por descubrir')

    cfg1.add_prod('dia', 'alegre alegre dia_text| encendido dia_texto')
    cfg1.add_prod('dia_texto', 'aprovecho el dia| tranquilo que el dia es largo')
    cfg1.add_prod('noche', 'encendido encendido encendido noche_texto| encendido noche_texto')
    cfg1.add_prod('noche_texto', 'parrandon| #partytonight| me duermo| quiero mi camita')


    cfg1.add_prod('oscuro', 'asustado asustado oscuro_texto| encendido oscuro_texto')
    cfg1.add_prod('oscuro_texto', 'no veo nada| donde estoy esta oscuro| espero que aqui no espanten')

    cfg1.add_prod('luz', 'E E luz_texto| luz_texto')
    cfg1.add_prod('luz_texto', 'Me tienen iluminado| como hay de luz')

    cfg1.add_prod('baja', 'asustado baja_texto| baja_texto')
    cfg1.add_prod('baja_texto', 'Got electricity?| alguien que me conecte al enchufe')

    cfg1.add_prod('muy_baja', 'asustado muy_baja_texto| muy_baja_texto')
    cfg1.add_prod('muy_baja_texto', 'Adios mundo cruel!| Apenas puedo encender mi led| AAAhhh asustado asustado')

    cfg1.add_prod('muy_alta', 'super energizado!| despues de un desayuno de campeones| listo para todo')


    return cfg1.gen_random_convergent(start_prod)
