
from nose.tools import eq_, raises
from . import optimization_model, energysystem
from oemof.outputlib import processing, views


class Filter_Test():
    def setup(self):
        self.results = processing.results(optimization_model)
        self.param_results = processing.parameter_as_dict(optimization_model)

    def test_filter_all_(self):
        nodes = views.filter_nodes(self.results)
        eq_(len(nodes), 19)

    def test_filter_all_without_busses(self):
        nodes = views.filter_nodes(self.results, exclude_busses=True)
        eq_(len(nodes), 19 - 7)

    def test_filter_only_sources(self):
        nodes = views.filter_nodes(
            self.results,
            option=views.NodeOption.HasOnlyOutputs,
            exclude_busses=True
        )
        eq_(len(nodes), 3)

    def test_filter_only_sinks(self):
        nodes = views.filter_nodes(
            self.results,
            option=views.NodeOption.HasOnlyInputs,
            exclude_busses=True
        )
        eq_(len(nodes), 3)

    def test_filter_no_sources(self):
        nodes = views.filter_nodes(
            self.results,
            option=views.NodeOption.HasInputs,
            exclude_busses=True
        )
        eq_(len(nodes), 9)

    def test_filter_has_outputs(self):
        nodes = views.filter_nodes(
            self.results,
            option='has_outputs'
        )
        eq_(len(nodes), 16)

    @raises(ValueError)
    def test_filter_has_something(self):
        views.filter_nodes(
            self.results,
            option='has_something'
        )

    def test_get_node_by_name(self):
        node = views.get_node_by_name(self.results, 'heat_pump')
        eq_(
            energysystem.groups['heat_pump'],
            node
        )

    def test_get_multiple_nodes_by_name(self):
        node1, node2 = views.get_node_by_name(self.results, 'b_el', 'pp_oil')
        eq_(
            energysystem.groups['b_el'],
            node1
        )
        eq_(
            energysystem.groups['pp_oil'],
            node2
        )

    def test_get_node_by_name_with_wrong_attribute(self):
        node1, node2 = views.get_node_by_name(self.results, 'b_el', 'wrong')
        eq_(
            energysystem.groups['b_el'],
            node1
        )
        eq_(
            None,
            node2
        )
