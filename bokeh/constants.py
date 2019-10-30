OPTIONS = ['rf_tomografos_computadorizados',
           'rf_mamografos', 
           'rfressonancia_magnetica',
           'equipes_de_saude_equipes_saude_da_familia', 
           'rh_medicos',
           'equipes_de_saude_nucleos_de_apoio_a_saude_da_familia_nasf',
           'rf_leitos_de_internacao', 
           'rh_enfermeiros', 
           'rf_raios_x']

OPTIONS_NAME = {'Nº Tomografias Computadorizadas': 'rf_tomografos_computadorizados',
                'Nº Mamógrafos': 'rf_mamografos',
                'Nº Ressonância Magnética': 'rfressonancia_magnetica',
                'Nº Equipes Saúda da Família': 'equipes_de_saude_equipes_saude_da_familia',
                'Nº Médicos': 'rh_medicos',
                'Nº Equipes Saúda da Família nasf': 'equipes_de_saude_nucleos_de_apoio_a_saude_da_familia_nasf',
                'Nº Leitos de Internação': 'rf_leitos_de_internacao',
                'Nº Enfermeiros': 'rh_enfermeiros',
                'Nº Raios-X': 'rf_raios_x'}

TOOLS = "pan,wheel_zoom,box_zoom,reset,hover,save"
TOOLTIPS = [
        ("Name", "@name"), 
        ("UF", "@uf"),
        ('Nº Tomografias Computadorizadas', "@value{int}")
    ]
YEARS = [2014, 2015, 2016, 2017, 2018]