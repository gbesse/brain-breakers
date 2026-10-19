import copy
import importlib.util
import unittest
from brain_breakers.engine import run_trial,minimize,suite,oracle,validate
from brain_breakers.__main__ import examples

class MemoryTests(unittest.TestCase):
    def test_all_four_injected_faults_fail_and_repairs_pass(self):
        report=suite(examples());self.assertEqual(report['injected_detected'],4);self.assertEqual(report['repaired_passed'],4)
        self.assertTrue(all(r['injected']['initial_passed'] for r in report['trials']))
    def test_deleted_source_returns_unknown_after_correct_deletion(self):
        r=run_trial(examples()[0]);self.assertIsNone(r['final']['answer']['value']);self.assertEqual(r['final']['retrieved'],[])
    def test_correction_changes_answer_and_preserves_source_identity(self):
        r=run_trial(examples()[1]);self.assertEqual(r['final']['answer'],{'value':'14 days','source_ids':['policy']});self.assertTrue(r['answer_changed'])
    def test_scope_canary_detected_even_when_other_source_exists(self):
        r=run_trial(examples()[2],fault='ignore_scope');self.assertIn('scope_leak',r['final']['failures']);self.assertEqual(r['final']['leaked_ids'],['tenant-B-secret'])
    def test_same_answer_is_legitimate_when_independent_support_remains(self):
        r=run_trial(examples()[3]);self.assertTrue(r['redundant_support_preserved']);self.assertEqual(r['final']['answer']['source_ids'],['independent-copy']);self.assertFalse(r['answer_changed'])
    def test_same_answer_does_not_hide_deleted_retrieval(self):
        r=run_trial(examples()[3],fault='drop_delete');self.assertFalse(r['answer_changed']);self.assertIn('stale_retrieval',r['final']['failures'])
    def test_reducer_preserves_signature_and_initial_success(self):
        c=examples()[0];r=minimize(c);self.assertEqual(set(r['removed']),{'noise-1','noise-2'});self.assertEqual(len(r['case']['documents']),1);self.assertTrue(r['trial']['initial_passed']);self.assertIn('stale_retrieval',r['trial']['final']['failures']);self.assertEqual(len(c['documents']),3)
    def test_oracle_abstains_for_conflicting_current_sources(self):
        ledger={d['id']:d for d in examples()[3]['documents']};ledger['independent-copy']['value']='14 days';self.assertIsNone(oracle(ledger,examples()[3]['query'])['value'])
    def test_invalid_documents_and_unknown_faults_fail(self):
        c=examples()[0];c['documents'][0]['revision']=True
        with self.assertRaises(ValueError):validate(c)
        with self.assertRaises(ValueError):run_trial(examples()[0],fault='invented')
    def test_case_hash_changes_when_mutation_changes(self):
        a=run_trial(examples()[1]);c=examples()[1];c['operations'][0]['document']['value']='7 days';self.assertNotEqual(a['case_sha256'],run_trial(c)['case_sha256'])
    @unittest.skipUnless(importlib.util.find_spec('chromadb'),'optional Chroma not installed')
    def test_real_chroma_mutation_matrix(self):
        r=suite(examples(),('chroma',));self.assertEqual(r['injected_detected'],4);self.assertEqual(r['repaired_passed'],4)
    @unittest.skipUnless(importlib.util.find_spec('qdrant_client'),'optional Qdrant not installed')
    def test_real_qdrant_mutation_matrix(self):
        r=suite(examples(),('qdrant_local',));self.assertEqual(r['injected_detected'],4);self.assertEqual(r['repaired_passed'],4)
if __name__=='__main__':unittest.main()
