from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import json


todos_los_juegos = pd.read_csv('static/Reports.csv', sep=';')

numero_partidas = max(todos_los_juegos['Result'])
informacion_partidas, labels = [], ['Partida', 'Cantidad To']
for numero_torre in range(6):
    labels += [f'Categoria To {numero_torre+1}', f'PosiciónX To {numero_torre+1}', f'PosiciónY To {numero_torre+1}']
labels += ['Cantidad Tr']
for numero_tropa in range(10):
    labels += [f'Categoria Tr {numero_tropa+1}', f'PosiciónX Tr {numero_tropa+1}', f'PosiciónY Tr {numero_tropa+1}']

for numero_partida in range(numero_partidas):
    partida = todos_los_juegos[todos_los_juegos['Result'] == numero_partida + 1]
    # Torres
    torres = partida[partida['Type'] == 1].values
    cantidadTorres = len(torres)
    informacion_torres = [numero_partida+1, cantidadTorres]
    for numero_torre in range(6):
        # categoria, posicionX, posicionY = float('nan'), float('nan'), float('nan')
        categoria, posicionX, posicionY = 0, 0, 0
        if numero_torre < cantidadTorres:
            categoria = int(torres[numero_torre][2])
            posicionX = torres[numero_torre][3]
            posicionY = torres[numero_torre][4]     
        informacion_torres += [categoria, posicionX, posicionY]
    # Tropas
    tropas = partida[partida['Type'] == 0].values
    cantidadTropas = len(tropas)
    informacion_tropas = [cantidadTropas]
    for numero_tropa in range(10):
        # categoria, posicionX, posicionY = float('nan'), float('nan'), float('nan')
        categoria, posicionX, posicionY = 0, 0, 0
        if numero_tropa < cantidadTropas:
            categoria = int(tropas[numero_tropa][2])
            posicionX = tropas[numero_tropa][3]
            posicionY = tropas[numero_tropa][4]     
        informacion_tropas += [categoria, posicionX, posicionY]
    informacion_partidas.append(informacion_torres + informacion_tropas)


juegos = pd.DataFrame(informacion_partidas, columns=labels)
torres = juegos.loc[:, 'Cantidad To':'PosiciónY To 6']
tropas = juegos.loc[:, 'Cantidad Tr':]


def convert_json_to_array_towers(json_towers):
    towers_info = [int(json_towers['amount'][0])]
    for item in eval(json_towers['towers']):
        towers_info += item['info']
    for i in range(6 - len(eval(json_towers['towers']))):
        towers_info += [0, 0, 0]

    return [towers_info]



def predict_troop_conf(tower_conf):
    X_towers = convert_json_to_array_towers(tower_conf)

    model = RandomForestRegressor()
    model.fit(torres, tropas)
    yhat = model.predict(X_towers)

    salida = []
    tropaSalida = [round(yhat[0][0])]
    for i, number in enumerate(yhat[0][1:]):
        if i % 3 == 0:
            salida.append(tropaSalida)
            tropaSalida = [round(number)]
        else:
            tropaSalida.append(float(f'{number:.4f}'))
    salida.append(tropaSalida)
    
    amount = salida[0][0]
    category = [s[0] for s in salida[1:]]
    positionX = [s[1] for s in salida[1:]]
    positionY = [s[2] for s in salida[1:]]

    return {
        'amount': amount,
        'category': category,
        'positionX': positionX,
        'positionY': positionY,
    }