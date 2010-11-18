"""
Django-compatible testscenarios.TestWithScenarios

It is required to have a special class because of the way
testscenarios.TestCase is implemented. It's using
testtools.clone_test_with_new_id() that calls copy.deepcopy() of the
initialized test case object. Unfortunately django's TestCase instances
have a client (django.test.Client) that uses cStringIO which cannot be
copied.

To work around the problem we implement a custom __deepcopy__ (ideally
this would be upstream in django.test.TestCase) that re-instantiates the
test Client() as a way of copying it's pristine state.
"""

import copy
import django.test
import testscenarios


class _EmptyNewStyleClass(object):
    """
    Empty new-style class similar to copy._EmptyClass
    """


class _ScenarioMixIn(object):

    def __deepcopy__(self, memo):
        self_copy = _EmptyNewStyleClass()
        self_copy.__class__ = self.__class__
        for attr in self.__dict__:
            value = getattr(self, attr)
            if isinstance(value, django.test.Client):
                value_copy = django.test.Client()
            else:
                value_copy = copy.deepcopy(value, memo)
            setattr(self_copy, attr, value_copy)
        return self_copy

    def __str__(self):
        """
        Override unitest.TestCase.__str__ to print the ID (that now
        contains the scenario name).
        """
        return self.id()


class TestCaseWithScenarios(
    _ScenarioMixIn,
    testscenarios.TestWithScenarios,
    django.test.TestCase):
    """
    Django TestCase with scenario support
    """


class TransactionTestCaseWithScenarios(
    _ScenarioMixIn,
    testscenarios.TestWithScenarios,
    django.test.TransactionTestCase):
    """
    Django TransactionTestCase with scenario support
    """
