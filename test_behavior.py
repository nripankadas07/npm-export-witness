import unittest
from npm_export_witness import analyze

def one(exports,sub='.',conditions=None):return analyze({'exports':exports,'queries':[{'subpath':sub,'conditions':conditions or []}]})['queries'][0]
class Behavior(unittest.TestCase):
    def test_order(self):self.assertEqual(one({'default':'./default.js','import':'./import.js'},conditions=['import'])['target'],'./default.js')
    def test_nested_fallback(self):self.assertEqual(one({'node':{'require':'./c.cjs'},'default':'./d.js'},conditions=['node','import'])['trace'],['default'])
    def test_nested_import(self):self.assertEqual(one({'node':{'import':'./i.mjs'}},conditions=['node','import'])['trace'],['node','import'])
    def test_null_blocks(self):self.assertEqual(one({'node':None,'default':'./d.js'},conditions=['node'])['status'],'blocked')
    def test_exact_before_pattern(self):self.assertEqual(one({'./*':'./wild/*.js','./a':'./exact.js'},'./a')['target'],'./exact.js')
    def test_specific_prefix(self):self.assertEqual(one({'./*':'./broad/*.js','./a/*':'./specific/*.js'},'./a/x')['target'],'./specific/x.js')
    def test_suffix_specificity(self):self.assertEqual(one({'./a/*':'./plain/*.js','./a/*.json':'./json/*.js'},'./a/x.json')['target'],'./json/x.js')
    def test_private_null(self):self.assertEqual(one({'./*':'./public/*.js','./private/*':None},'./private/x')['status'],'blocked')
    def test_missing(self):self.assertEqual(one({'./a':'./a.js'},'./b')['status'],'not_exported')
    def test_unsafe_target(self):
        with self.assertRaises(ValueError):one('./../outside.js')
    def test_arrays_unsupported(self):
        with self.assertRaises(ValueError):one(['./a.js'])
    def test_condition_conflict(self):
        with self.assertRaises(ValueError):one('./a.js',conditions=['import','require'])
    def test_encoded_path(self):
        with self.assertRaises(ValueError):one({'./*':'./x/*.js'},'./%2e%2e/x')

if __name__=="__main__":unittest.main()
