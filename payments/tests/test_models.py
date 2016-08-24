# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django.test import TestCase

from .factories import (WorkshopFactory, InstructorFactory, OrderItemFactory,
                        OrderFactory)
from ..models import Workshop, Instructor, Order


class WorkshopTestCase(TestCase):
    def test_creation(self):
        w = WorkshopFactory()
        self.assertTrue(isinstance(w, Workshop))
        self.assertEqual(str(w), w.title)

    def test_total_tickets_sold(self):
        # Create a single order item (ticket)
        oi = OrderItemFactory(order__billed_total='100.00')
        self.assertEqual(1, oi.rate.workshop.total_tickets_sold)

        oi = OrderItemFactory(order__billed_total='')
        self.assertEqual(0, oi.rate.workshop.total_tickets_sold)

    def test_is_at_capacity(self):
        oi = OrderItemFactory(order__billed_total='asdf', rate__capacity=5,
                              rate__workshop__capacity=5)
        self.assertEqual(False, oi.rate.workshop.is_at_capacity)


class InstructorTestCase(TestCase):
    def test_creation(self):
        i = InstructorFactory(workshops=[WorkshopFactory() for i in range(5)])
        self.assertTrue(isinstance(i, Instructor))
        self.assertEqual(str(i), i.name)
        self.assertEqual(len(i.workshops.all()), 5)


class OrderTestCase(TestCase):
    def test_creation(self):
        o = OrderFactory()
        self.assertTrue(isinstance(o, Order))
        o_str = '%s: $%s on %s' % (o.contact_email, o.order_total,
                                   o.order_datetime)
        self.assertEqual(str(o), o_str)
