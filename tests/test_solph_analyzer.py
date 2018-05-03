
from nose.tools import eq_
from energysystems_for_testing import es_with_invest
from oemof.outputlib import processing
from oemof.solph import analyzer


class Analyzer_Tests:
    def setup(self):
        self.results = processing.results(
            es_with_invest.optimization_model)
        self.param_results = processing.param_results(
            es_with_invest.optimization_model)
        analyzer.init(
            self.results,
            self.param_results,
            iterator=analyzer.FlowNodeIterator
        )

    def test_simple_analyzer(self):
        analyzer.clean()
        a = analyzer.SequenceFlowSumAnalyzer()
        analyzer.analyze()
        eq_(len(a.result), 5)

    def test_requirements(self):
        pass

    def test_bus_balance_analyzer(self):
        analyzer.clean()
        a = analyzer.SequenceFlowSumAnalyzer()
        _ = analyzer.FlowTypeAnalyzer()
        c = analyzer.BusBalanceAnalyzer()
        analyzer.analyze()

        eq_(len(a.result), 5)
        eq_(len(c.result), 3)

    def test_invest_analyzer(self):
        analyzer.clean()
        invest = analyzer.InvestAnalyzer()
        analyzer.analyze()
        # print(invest.result)
