"""All writable text follows the language boundary; credentials and saved evidence remain intact."""
import copy
import json
import unittest
from unittest.mock import patch
import test_server as base
from test_text_filter import BLOCKED, ALLOWED
from human_text import valid_payload, display_safe, MESSAGE, TEXT_KEYS, SKIP


def stable_state(state):
    state=copy.deepcopy(state);state.get('pipFood',{}).pop('asOf',None);return state


class LanguageTests(unittest.TestCase):
    setUp=base.PilotTests.setUp
    tearDown=base.PilotTests.tearDown
    learner=base.PilotTests.learner

    def test_nested_fields_and_credentials(self):
        for field in TEXT_KEYS-SKIP:
            self.assertFalse(valid_payload({'data':{field:BLOCKED[0]}}),field)
        self.assertFalse(valid_payload({'answers':{'question-one':BLOCKED[0]}}))
        self.assertFalse(valid_payload({'scenarioLab':{'1':{'tasks':{'message':{'text':BLOCKED[0]}}}}}))
        for text in ALLOWED:
            self.assertTrue(valid_payload({'reflection':text}),text)
        credentials={'passphrase':BLOCKED[0], 'previousPassphrase':BLOCKED[0], 'password':BLOCKED[0], 'code':BLOCKED[0], 'recovery':BLOCKED[0], 'token':BLOCKED[0]}
        self.assertTrue(valid_payload(credentials));self.assertEqual(display_safe(credentials),credentials)

    def test_draft_rejection_does_not_change_revision_or_saved_work(self):
        learner,_=self.learner('Language test')
        draft={'phase':1,'reflection':'Meet at the library at four.', 'scenarioLab':{'1':{'tasks':{'invite':{'text':'Bring your notebook.'}}}}}
        status,saved,_=learner.request('/api/draft',{'unit':'writing-1','revision':0,'data':draft})
        self.assertEqual(status,200,saved)
        before=learner.request('/api/drafts')[1]
        for path in ('reflection','scenario'):
            changed=copy.deepcopy(draft)
            if path=='reflection':changed['reflection']=BLOCKED[0]
            else:changed['scenarioLab']['1']['tasks']['invite']['text']=BLOCKED[0]
            status,result,_=learner.request('/api/draft',{'unit':'writing-1','revision':1,'data':changed})
            self.assertEqual((status,result),(400,{'error':MESSAGE}))
            self.assertEqual(learner.request('/api/drafts')[1],before)
        draft['reflection']='Meet at the library at five.'
        status,result,_=learner.request('/api/draft',{'unit':'writing-1','revision':1,'data':draft})
        self.assertEqual(status,200,result);self.assertEqual(result['revision'],2)

    def test_submissions_reject_language_before_awards_and_can_be_corrected(self):
        learner,_=self.learner()
        attempt=learner.request('/api/attempt',{'unit':'math-1'})[1]
        clean={'id':attempt['id'],'answers':base.right_answers('math-1',attempt),'reflection':'I counted each carton and checked the total.','support':'myself','ink':[]}
        before=learner.request('/api/me')[1]
        for field in ('reflection','answer'):
            data=copy.deepcopy(clean)
            if field=='reflection':data['reflection']=BLOCKED[0]
            else:data['answers'][next(iter(data['answers']))]=BLOCKED[0]
            status,result,_=learner.request('/api/submit',data)
            self.assertEqual((status,result),(400,{'error':MESSAGE}))
            self.assertEqual(stable_state(learner.request('/api/me')[1]),stable_state(before))
        status,result,_=learner.request('/api/submit',clean)
        self.assertEqual(status,200,result);self.assertTrue(result['report']['passed'])

    def test_notes_and_narration_cannot_bypass_forms(self):
        learner,_=self.learner()
        before=learner.request('/api/me')[1]
        for path,data in [('/api/device-work',{'unit':'digital-pc-save','revision':0,'status':'help','note':BLOCKED[0]}),
                          ('/api/project/finish',{'revision':0,'explanation':BLOCKED[0],'accessNote':'Readable text','backupNote':'Saved copy'}),
                          ('/api/mentor/review',{'id':'synthetic','note':BLOCKED[0]}),
                          ('/api/starting-point',{'revision':0,'data':{'answers':{'writing':BLOCKED[0]}}})]:
            client=self.mentor if path.startswith('/api/mentor') else learner
            self.assertEqual(client.request(path,data)[:2],(400,{'error':MESSAGE}),path)
        with patch.object(self.app.voice,'speak') as speak:
            self.assertEqual(learner.request('/api/read-aloud',{'text':BLOCKED[0]})[:2],(400,{'error':MESSAGE}))
            speak.assert_not_called()
        self.assertEqual(stable_state(learner.request('/api/me')[1]),stable_state(before))

    def test_legacy_work_is_masked_in_reports_but_remains_editable(self):
        learner,me=self.learner()
        draft={'phase':1,'reflection':BLOCKED[0]}
        attempt=learner.request('/api/attempt',{'unit':'math-1'})[1]
        data={'id':attempt['id'],'answers':base.right_answers('math-1',attempt),'reflection':'I checked the total.','support':'myself','ink':[]}
        self.assertEqual(learner.request('/api/submit',data)[0],200)
        store=self.app.accounts.by_name['test-mentor']
        with store.db() as db:
            db.execute('INSERT INTO drafts(learner,unit,revision,content,updated) VALUES(?,?,?,?,?)',(me['id'],'writing-1',1,json.dumps(draft),1))
            row=db.execute('SELECT report FROM attempts WHERE id=?',(attempt['id'],)).fetchone()
            report=json.loads(row['report']);report['reflection']=BLOCKED[0];report['questions'][0]['answer']=BLOCKED[0]
            db.execute('UPDATE attempts SET report=?,note=? WHERE id=?',(json.dumps(report),BLOCKED[0],attempt['id']))
        self.assertEqual(learner.request('/api/drafts')[1]['writing-1']['data'],draft)
        current=learner.request('/api/me')[1]['attempts'][0]
        self.assertEqual(current['note'],'Text needs revision.')
        self.assertEqual(current['report']['reflection'],'Text needs revision.')
        self.assertEqual(current['report']['questions'][0]['answer'],'Text needs revision.')
        shared=self.mentor.request('/api/mentor')[1]['reports'][0]
        self.assertEqual(shared['report']['reflection'],'Text needs revision.')
        with store.db() as db:
            raw=db.execute('SELECT report FROM attempts WHERE id=?',(attempt['id'],)).fetchone()['report']
        self.assertEqual(json.loads(raw)['reflection'],BLOCKED[0])
        self.assertEqual(json.loads(raw)['questions'][0]['answer'],BLOCKED[0])


if __name__=='__main__':unittest.main()
