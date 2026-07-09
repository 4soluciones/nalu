import decimal
from datetime import datetime, time

from django.db.models import Prefetch

from apps.sales.models import (
    Order,
    OrderAction,
    OrderCharge,
    OrderCommodity,
    OrderCommodityAddressee,
    OrderDelivery,
    OrderDetail,
    OrderMoving,
    OrderRoute,
)


def _parse_time(value):
    if not value or value in ('00:00', 'None'):
        return None
    if isinstance(value, time):
        return value
    try:
        return datetime.strptime(str(value), '%H:%M').time()
    except ValueError:
        try:
            return datetime.strptime(str(value), '%H:%M:%S').time()
        except ValueError:
            return None


def sync_commodity_addressees(commodity, addressee_actions):
    """Vincula destinatarios de OrderAction al modelo de encomienda."""
    if not commodity:
        return
    commodity.addressee_links.all().delete()
    for position, action in enumerate(addressee_actions):
        OrderCommodityAddressee.objects.create(
            commodity=commodity,
            client=action.client,
            order_addressee=action.order_addressee,
            position=position,
        )


def _parse_date(value):
    if not value:
        return None
    if hasattr(value, 'year'):
        return value
    try:
        return datetime.strptime(str(value), '%Y-%m-%d').date()
    except ValueError:
        return None


def save_service_for_order(order_obj, service_type, service_extra=None, *,
                           subsidiary_origin=None, subsidiary_destiny=None,
                           sender=None, type_guide='O',
                           arrival_time=None, address_delivery='', code='0000'):
    """Persiste el detalle específico según el tipo de servicio."""
    service_extra = service_extra or {}
    service_type = (service_type or 'E').upper()

    if service_type == 'E':
        return OrderCommodity.objects.create(
            order=order_obj,
            sender=sender,
            office_origin=subsidiary_origin,
            office_destination=subsidiary_destiny,
            type_guide=type_guide or 'O',
            arrival_time=_parse_time(arrival_time),
            address_delivery=address_delivery or '',
            code=(code or '0000').strip() or '0000',
            addressee_name=service_extra.get('addressee_name', '') or '',
        )

    if service_type == 'M':
        OrderMoving.objects.create(
            order=order_obj,
            origin_address=service_extra.get('origin_address', '') or '',
            origin_property_type=service_extra.get('origin_property_type', '') or 'C',
            origin_floors=int(service_extra.get('origin_floors') or 1),
            destination_address=service_extra.get('dest_address', '') or '',
            dest_property_type=service_extra.get('dest_property_type', '') or 'C',
            dest_floors=int(service_extra.get('dest_floors') or 1),
            service_date=_parse_date(service_extra.get('service_date')),
            service_time=_parse_time(service_extra.get('service_time')),
            helpers_count=int(service_extra.get('helpers_count') or 0),
            fare_amount=decimal.Decimal(str(service_extra.get('fare_amount') or order_obj.total or 0)),
            payment_method=service_extra.get('payment_method', '') or 'E',
        )
        return

    if service_type == 'D':
        OrderDelivery.objects.create(
            order=order_obj,
            pickup_address=service_extra.get('origin_address', '') or '',
            delivery_address=service_extra.get('dest_address', '') or '',
            receiver_name=service_extra.get('dest_contact', '') or '',
            receiver_phone=service_extra.get('dest_phone', '') or '',
            dest_reference=service_extra.get('dest_reference', '') or '',
            fare_amount=decimal.Decimal(str(service_extra.get('fare_amount') or order_obj.total or 0)),
            payment_method=service_extra.get('payment_method', '') or 'E',
        )
        return

    if service_type == 'C':
        OrderCharge.objects.create(
            order=order_obj,
            client_ruc=service_extra.get('client_ruc', '') or '',
            client_name=service_extra.get('client_name', '') or '',
            origin_address=service_extra.get('origin_address', '') or '',
            origin_contact=service_extra.get('origin_contact', '') or '',
            origin_phone=service_extra.get('origin_phone', '') or '',
            dest_address=service_extra.get('dest_address', '') or '',
            dest_contact=service_extra.get('dest_contact', '') or '',
            dest_phone=service_extra.get('dest_phone', '') or '',
            fare_amount=decimal.Decimal(str(service_extra.get('fare_amount') or order_obj.total or 0)),
            payment_method=service_extra.get('payment_method', '') or 'E',
        )


def get_service_destiny_label(order_obj):
    """Etiqueta de destino para el reporte según tipo de servicio."""
    if order_obj.service_type == 'E':
        encomienda = getattr(order_obj, 'encomienda', None)
        if encomienda and encomienda.office_destination_id:
            return encomienda.office_destination.short_name or encomienda.office_destination.name
        for route in order_obj.orderroute_set.all():
            if route.type == 'D' and route.subsidiary_id:
                return route.subsidiary.name
        return '—'

    if order_obj.service_type == 'M':
        moving = getattr(order_obj, 'moving', None)
        return (moving.destination_address if moving else '') or '—'

    if order_obj.service_type == 'D':
        delivery = getattr(order_obj, 'delivery', None)
        return (delivery.delivery_address if delivery else '') or '—'

    if order_obj.service_type == 'C':
        cargo = getattr(order_obj, 'cargo', None)
        return (cargo.dest_address if cargo else '') or '—'

    return '—'


def prefetch_orders_for_report(order_set):
    return order_set.prefetch_related(
        Prefetch(
            'orderdetail_set',
            queryset=OrderDetail.objects.select_related('unit'),
        ),
        Prefetch(
            'orderroute_set',
            queryset=OrderRoute.objects.filter(type='D').select_related('subsidiary'),
        ),
        Prefetch(
            'orderaction_set',
            queryset=OrderAction.objects.select_related('client', 'order_addressee'),
        ),
        'encomienda__office_destination',
        'encomienda__office_origin',
        'encomienda__addressee_links__client',
        'encomienda__addressee_links__order_addressee',
        'moving',
        'delivery',
        'cargo',
    ).select_related('user', 'company', 'truck', 'encomienda', 'moving', 'delivery', 'cargo')
