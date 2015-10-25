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
    cfg1.add_prod('T', 'frio| normal| calor| mucho_frio')
    cfg1.add_prod('calor', 'enfadado calor_texto| calor_texto')
    cfg1.add_prod('calor_texto', 'insoportable #calor| insoportable calor| #calorin| que calor infernal!| toy sudando enfadado #enfadado')
    cfg1.add_prod('frio', 'frio_texto asqueado| frio_texto')
    cfg1.add_prod('frio_texto', 'Un poco #frio.| Un poco frio| No tengo sueter triste| estoy temblando encendido| esto no es clima templado')
    cfg1.add_prod('mucho_frio', 'mucho_frio_texto asqueado| mucho_frio_texto')
    cfg1.add_prod('mucho_frio_texto', 'Vaya frío.| Llevo más capas que una lechuga.| ¡Lo que vamos a tener que pagar de calefacción!| Llevo más capas que una lechuga.| Plan de sofá y mantita.| Esto es cosa del cambio climático.| Esto parece el Polo Norte.| Alguien que me traiga una manta.| Un cafecito quedaria alegre, mucho_frio')

    cfg1.add_prod('brusco', 'brusco_texto| asqueado triste brusco_texto')
    cfg1.add_prod('brusco_texto', 'Que brusco cambio de temp| Como cambia la temperatura| Sube y Baja de temperatura')
    cfg1.add_prod('normal', 'alegre alegre alegre| #chillin| encendido #trankis alegre| me siento fabuloso!!')

    cfg1.add_prod('E', 'enamorado| enfadado| asqueado| triste| alegre| apagado| encendido')
    cfg1.add_weighted_prod('enamorado', '<3$37.5| ;-)$12.5| ;)$12.5| *-)$12.5| *)$12.5| ;-$12.5')
    cfg1.add_weighted_prod('enfadado', 'Arrrgh enfadado$0.2| :@$0.1| me pongo enfadado$0.3| >:($0.1| enfadado enfadado$0.3')
    cfg1.add_prod('asqueado', '>:O| :-O| :O| :-o| :o')
    cfg1.add_prod('triste', ':<| :-[| :[| :{')
    cfg1.add_prod('alegre', ':-)| :)| :D| :o)| :]| :3| :c)| :>| =]| 8)| =)| :}| :^)')
    cfg1.add_prod('apagado', ':-X| :X| :-#| :#| :-&| :&')
    cfg1.add_prod('encendido', '%-)| %)| #-)')
    cfg1.add_prod('asustado', 'encendido apagado| asqueado| AAAAAAAaaa asustado AAAAAaaa| tengo miedo')

    cfg1.add_prod('lugar', 'ya habeis oido hablar de| Un nuevo sitio por descubrir| exploremos| aqui voy| la vida es mas sabrosa en | Twitter estoy en')

    cfg1.add_prod('dia', 'alegre alegre dia_text| encendido dia_texto')
    cfg1.add_prod('dia_texto', 'aprovecho el dia| tranquilo que el dia es largo| hoy me levante tarde')
    cfg1.add_prod('noche', 'encendido encendido encendido noche_texto| encendido noche_texto')
    cfg1.add_prod('noche_texto', 'parrandon| #partytonight| me duermo| quiero mi camita| No voy a poder ir de fiesta| Voy a caer en un coma')


    cfg1.add_prod('oscuro', 'asustado oscuro_texto| encendido oscuro_texto')
    cfg1.add_prod('oscuro_texto', 'mami tengo miedo| no veo nada| esta oscuro| espero que aqui no espanten| Traiganme un linterna asustado| He perdido la vista')

    cfg1.add_prod('luz', 'E E luz_texto| luz_texto')
    cfg1.add_prod('luz_texto', 'Me tienen iluminado| como hay de luz| alumbrado| claridad| #hayluz| resplandece')

    cfg1.add_prod('baja', 'asustado baja_texto| baja_texto')
    cfg1.add_prod('baja_texto', 'Got electricity?| alguien que me conecte al enchufe| electrificame| ayudame| hey tu, tiene electricidad')

    cfg1.add_prod('muy_baja', 'asustado muy_baja_texto| muy_baja_texto')
    cfg1.add_prod('muy_baja_texto', 'Adios mundo cruel!| Apenas puedo encender mi led| AAAhhh asustado asustado| Y ahora quie podra ayudarme?| Followers vengan a ayudarme')

    cfg1.add_prod('muy_alta', 'super energizado!| despues de un desayuno de campeones| listo para todo| me siento como un tigre| manos a la obra| me siento fenomenal')


    return cfg1.gen_random_convergent(start_prod)
