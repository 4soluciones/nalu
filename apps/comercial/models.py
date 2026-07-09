from django.db import models
from apps.users.models import Subsidiary


class Owner(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Nombre', max_length=100, unique=True)
    associated = models.CharField('Asociado', max_length=100, null=True, blank=True)
    ruc = models.CharField(max_length=11)
    address = models.CharField('Dirección', max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Propietario'
        verbose_name_plural = 'Propietarios'


class TruckBrand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Nombre', max_length=45, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Marca de tracto'
        verbose_name_plural = 'Marcas de tractos'


class TruckModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Nombre', max_length=45, unique=True)
    truck_brand = models.ForeignKey('TruckBrand', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Modelo de tracto'
        verbose_name_plural = 'Modelos de tractos'


class Truck(models.Model):
    DRIVE_TYPE_CHOICES = (('C', 'FURGON'), ('S', 'SEMITRAILER'), ('A', 'CAMION'),)
    FUEL_TYPE_CHOICES = (('1', 'DIESEL'), ('2', 'GASOLINA'), ('3', 'GAS'),)
    CONDITION_OWNER_CHOICES = (('P', 'PROPIO'), ('A', 'APOYO'),)
    id = models.AutoField(primary_key=True)
    license_plate = models.CharField('Placa', max_length=10)
    num_axle = models.IntegerField('Numero de Ejes', null=True, default=0)
    year = models.CharField('Fabricación', max_length=4, null=True, blank=True)
    truck_model = models.ForeignKey('TruckModel', on_delete=models.SET_NULL, null=True, blank=True)
    drive_type = models.CharField('Tipo de Unidad', max_length=2,
                                  choices=DRIVE_TYPE_CHOICES, default='A')
    contact_phone = models.CharField(max_length=45, null=True, blank=True)
    certificate = models.CharField(max_length=15, null=True, blank=True)
    nro_passengers = models.CharField(max_length=2, null=True, blank=True)
    engine = models.CharField('Motor', max_length=100, null=True, blank=True)
    chassis = models.CharField('Chasis', max_length=100, null=True, blank=True)
    color = models.CharField(max_length=45, null=True, blank=True)
    fuel_type = models.CharField('Tipo de Combustible', max_length=1,
                                 choices=FUEL_TYPE_CHOICES, default='1')
    owner = models.ForeignKey('Owner', on_delete=models.SET_NULL, null=True, blank=True)
    condition_owner = models.CharField('Condicion', max_length=1,
                                       choices=CONDITION_OWNER_CHOICES, default='P')
    technical_review_expiration_date = models.DateField('Fecha de expiracion de revisión técnica', null=True,
                                                        blank=True)
    soat_expiration_date = models.DateField('Fecha de expiracion del soat', null=True, blank=True)
    capacidad_kg = models.DecimalField('Capacidad (kg)', max_digits=10, decimal_places=2, default=0)
    capacidad_m3 = models.DecimalField('Capacidad (m³)', max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField('Activo', default=True)

    def __str__(self):
        return self.license_plate

    class Meta:
        verbose_name = 'Unidad'
        verbose_name_plural = 'Unidades'


class Programming(models.Model):
    SERVICE_TYPE_CHOICES = (
        ('E', 'Encomiendas'),
        ('M', 'Mudanzas'),
        ('D', 'Delivery'),
        ('C', 'Carga'),
    )
    STATUS_CHOICES = (
        ('P', 'Programado'),
        ('R', 'En ruta'),
        ('E', 'Entregado'),
        ('C', 'Cancelado'),
    )
    TYPE_CHOICES = (('E', 'Encomienda'), ('V', 'Viajes'))
    TURN_CHOICES = (('1', '12:00 AM'),
                    ('2', '12:15 AM'),
                    ('3', '12:30 AM'),
                    ('4', '12:45 AM'),
                    ('5', '01:00 AM'),
                    ('6', '01:15 AM'),
                    ('7', '01:30 AM'),
                    ('8', '01:45 AM'),
                    ('9', '02:00 AM'),
                    ('10', '02:15 AM'),
                    ('11', '02:30 AM'),
                    ('12', '02:45 AM'),
                    ('13', '03:00 AM'),
                    ('14', '03:15 AM'),
                    ('15', '03:30 AM'),
                    ('16', '03:45 AM'),
                    ('17', '04:00 AM'),
                    ('18', '04:15 AM'),
                    ('19', '04:30 AM'),
                    ('20', '04:45 AM'),
                    ('21', '05:00 AM'),
                    ('22', '05:15 AM'),
                    ('23', '05:30 AM'),
                    ('24', '05:45 AM'),
                    ('25', '06:00 AM'),
                    ('26', '06:15 AM'),
                    ('27', '06:30 AM'),
                    ('28', '06:45 AM'),
                    ('29', '07:00 AM'),
                    ('30', '07:15 AM'),
                    ('31', '07:30 AM'),
                    ('32', '07:45 AM'),
                    ('33', '08:00 AM'),
                    ('34', '08:15 AM'),
                    ('35', '08:30 AM'),
                    ('36', '08:45 AM'),
                    ('37', '09:00 AM'),
                    ('38', '09:15 AM'),
                    ('39', '09:30 AM'),
                    ('40', '09:45 AM'),
                    ('41', '10:00 AM'),
                    ('42', '10:15 AM'),
                    ('43', '10:30 AM'),
                    ('44', '10:45 AM'),
                    ('45', '11:00 AM'),
                    ('46', '11:15 AM'),
                    ('47', '11:30 AM'),
                    ('48', '11:45 AM'),
                    ('49', '12:00 PM'),
                    ('50', '12:15 PM'),
                    ('51', '12:30 PM'),
                    ('52', '12:45 PM'),
                    ('53', '01:00 PM'),
                    ('54', '01:15 PM'),
                    ('55', '01:30 PM'),
                    ('56', '01:45 PM'),
                    ('57', '02:00 PM'),
                    ('58', '02:15 PM'),
                    ('59', '02:30 PM'),
                    ('60', '02:45 PM'),
                    ('61', '03:00 PM'),
                    ('62', '03:15 PM'),
                    ('63', '03:30 PM'),
                    ('64', '03:45 PM'),
                    ('65', '04:00 PM'),
                    ('66', '04:15 PM'),
                    ('67', '04:30 PM'),
                    ('68', '04:45 PM'),
                    ('69', '05:00 PM'),
                    ('70', '05:15 PM'),
                    ('71', '05:30 PM'),
                    ('72', '05:45 PM'),
                    ('73', '06:00 PM'),
                    ('74', '06:15 PM'),
                    ('75', '06:30 PM'),
                    ('76', '06:45 PM'),
                    ('77', '07:00 PM'),
                    ('78', '07:15 PM'),
                    ('79', '07:30 PM'),
                    ('80', '07:45 PM'),
                    ('81', '08:00 PM'),
                    ('82', '08:15 PM'),
                    ('83', '08:30 PM'),
                    ('84', '08:45 PM'),
                    ('85', '09:00 PM'),
                    ('86', '09:15 PM'),
                    ('87', '09:30 PM'),
                    ('88', '09:45 PM'),
                    ('89', '10:00 PM'),
                    ('90', '10:15 PM'),
                    ('91', '10:30 PM'),
                    ('92', '10:45 PM'),
                    ('93', '11:00 PM'),
                    ('94', '11:15 PM'),
                    ('95', '11:30 PM'),
                    ('96', '11:45 PM'),)
    id = models.AutoField(primary_key=True)
    departure_date = models.DateField('Fecha Salida', null=True, blank=True)
    arrival_date = models.DateField('Fecha Llegada', null=True, blank=True)
    service_type = models.CharField('Servicio', max_length=1, choices=SERVICE_TYPE_CHOICES, default='E')
    status = models.CharField('Estado', max_length=1, choices=STATUS_CHOICES, default='P')
    turn = models.CharField('Horario', max_length=2, choices=TURN_CHOICES, default='1', )
    type = models.CharField('Tipo', max_length=1, choices=TYPE_CHOICES, null=True, )
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    truck = models.ForeignKey('Truck', verbose_name='Tracto',
                              on_delete=models.SET_NULL, null=True, blank=True)
    subsidiary = models.ForeignKey(Subsidiary, verbose_name='Sede',
                                   on_delete=models.SET_NULL, null=True, blank=True)
    observation = models.CharField(max_length=200, null=True, blank=True)
    order = models.IntegerField('Turno', default=0)
    km_initial = models.CharField('km inicial', max_length=6, null=True, blank=True)
    km_ending = models.CharField('km inicial', max_length=6, null=True, blank=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="children")
    correlative = models.CharField(verbose_name='Correlativo', max_length=45, null=True, blank=True)
    serial = models.CharField(verbose_name='Serie', max_length=4, null=True, blank=True)
    company = models.ForeignKey('users.Company', on_delete=models.SET_NULL, null=True, blank=True)
    truck_exit = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    support_pilot = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def has_parent(self):
        return self.parent is not None

    class Meta:
        verbose_name = 'Programación'
        verbose_name_plural = 'Programaciones'
