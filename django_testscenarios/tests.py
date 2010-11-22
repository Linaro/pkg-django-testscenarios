# Copyright (C) 2010 Linaro Limited
#
# Author: Zygmunt Krynicki <zygmunt.krynicki@linaro.org>
#
# This file is part of django-testscenarios.
#
# django-testscenarios is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation
#
# django-testscenarios is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with django-testscenarios.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models, transaction

from django_testscenarios import (
    TestCaseWithScenarios,
    TransactionTestCaseWithScenarios,
)


class TestModel(models.Model):
    """
    Model for testing database configuration/initialization
    """


class DjangoTestCaseWithScenarios(TestCaseWithScenarios):

    scenarios = [
        ('scenario_a', {'attr': 'foo'}),
        ('scenario_b', {'attr': 'bar'}),
    ]

    def setUp(self):
        super(DjangoTestCaseWithScenarios, self).setUp()
        assert getattr(self, 'attr') is not None

    def test_database_is_empty_at_start_of_test(self):
        self.assertEqual(TestModel.objects.all().count(), 0)
        stream = TestModel.objects.create()

    def test_attr_is_set(self):
        self.assertNotEqual(getattr(self, 'attr'), None)


class DjangoTestCaseWithScenariosAndTransactions(TransactionTestCaseWithScenarios):

    scenarios = [
        ('scenario_a', {'attr': 'foo'}),
        ('scenario_b', {'attr': 'bar'}),
    ]

    def setUp(self):
        super(DjangoTestCaseWithScenariosAndTransactions, self).setUp()
        assert getattr(self, 'attr') is not None

    def test_database_is_empty_at_start_of_test(self):
        self.assertEqual(TestModel.objects.all().count(), 0)
        stream = TestModel.objects.create()

    def test_attr_is_set(self):
        self.assertNotEqual(getattr(self, 'attr'), None)


class DjangoTestCaseWithoutScenarios(TestCaseWithScenarios):

    def test_database_is_empty_at_start_of_test_first(self):
        self.assertEqual(TestModel.objects.all().count(), 0)
        obj = TestModel.objects.create()
        transaction.commit()

    def test_database_is_empty_at_start_of_test_second(self):
        self.assertEqual(TestModel.objects.all().count(), 0)
        obj = TestModel.objects.create()
        transaction.commit()
