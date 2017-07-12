import pandas as pd

# denue = gpd.read_file("datos/DENUE_INEGI_09_.shp")
# agebs = gpd.read_file("datos/ageb_urb.shp")


def clasifica(codigo):
    """Clasifica las actividades."""
    comercio = ['461', '462', '463', '464', '465', '466']
    oficinas = ['51', '521', '523', '524', '5312', '5313', '541', '55']
    ocio = ['711121', '71212', '7132', '7139', '7211', '7224', '7225']
    usos = {'comercio': comercio, 'oficinas': oficinas, 'ocio': ocio}
    for actividad, claves in usos.items():
        for c in claves:
            if str(codigo).startswith(c):
                return actividad


def concatena_claves(x):
    """Concatena claves para generar CVEGEO."""
    return '{}{}{}{}'.format(x['cve_ent'], x['cve_mun'],
                             x['cve_loc'], x['ageb'])


def preprocesa(puntos, poligonos):
    """Procesa los datos y regresa el merge."""
    puntos.loc[:, 'clase'] = puntos['codigo_act'].apply(clasifica)
    puntos = puntos.loc[puntos['clase'].notnull()]
    puntos.loc[:, 'cve_geo'] = puntos.apply(concatena_claves, axis=1)
    variables = puntos[['cve_geo', 'clase']]
    variables = pd.get_dummies(variables, columns=['clase'])
    por_ageb = variables.groupby(['cve_geo']).sum()
    poligonos = poligonos[['CVEGEO', 'geometry']]
    usos_suelo = poligonos.merge(por_ageb, left_on='CVEGEO',
                                 right_index=True, how='inner')
    print('si')
    return usos_suelo
