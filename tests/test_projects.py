"""Synthetic protocol and artifact checks; browser evidence is recorded separately."""
import copy
import json
import subprocess
import unittest
import urllib.request
import test_server as base
import projects

PLAN=dict(kind='checklist',title='Shift kit',purpose='Remember what to bring to a practice shift.',behaviours=['Add a task','Mark it done','Keep it saved'],label='What to pack',limit=3,goal=5000,accent='teal')

class ProjectTests(unittest.TestCase):
    setUp=base.PilotTests.setUp
    tearDown=base.PilotTests.tearDown
    learner=base.PilotTests.learner

    def call(self,c,action,status=200,**data):
        r=c.request('/api/me')[1]['project']
        code,value,_=c.request('/api/project/'+action,dict(revision=r['revision'] if r else 0,**data))
        self.assertEqual(code,status,value)
        return value

    def built(self):
        c,me=self.learner();base.complete_core_fixture(self.app,c);self.call(c,'save',data=PLAN);self.call(c,'add',label='Bottle',value='');return c,me

    def test_owner_revision_and_independent_grade(self):
        c,me=self.built();other,otherme=self.learner('Other')
        self.assertEqual(other.request('/api/me')[1]['project'],None)
        self.assertEqual(other.request('/api/project/save',dict(learner=me['id'],revision=0,data=PLAN))[0],409)
        r=c.request('/api/me')[1]['project'];payload=dict(revision=r['revision'],label='Keys',value='')
        self.assertEqual(c.request('/api/project/add',payload)[0],200)
        self.assertEqual(c.request('/api/project/add',payload)[0],409)
        self.assertEqual(len(c.request('/api/me')[1]['project']['data']['items']),2)
        self.assertEqual(c.request('/api/me')[1]['points'],0)
        attempt=c.request('/api/attempt',dict(unit='app-build'))[1]
        answers=base.right_answers('app-build',attempt)
        self.assertEqual(c.request('/api/submit',dict(id=attempt['id'],answers=answers,reflection='Synthetic check before project evidence.',support='tool'))[0],400)

    def test_invalid_inputs_keep_items_and_money_exact(self):
        c,me=self.built()
        for label in ('',' '*3,'x'*81):self.call(c,'add',status=400,label=label,value='')
        self.assertEqual(len(c.request('/api/me')[1]['project']['data']['items']),1)
        self.call(c,'save',data=dict(PLAN,kind='savings',goal=2500))
        for amount in ('-3','nan','2.345','ten','0'):
            self.call(c,'add',status=400,label='Saved',value=amount)
        self.call(c,'add',label='First',value='10.50');r=self.call(c,'add',label='Second',value='4.25')
        self.assertEqual(sum(i['value'] for i in r['project']['data']['items']),1475)

    def test_undo_restore_and_forged_evidence(self):
        c,me=self.built();before=c.request('/api/me')[1]['project']['data']
        self.call(c,'save',data=dict(PLAN,title='New title'));r=self.call(c,'undo')
        self.assertEqual(r['project']['data']['title'],'Shift kit')
        backup=dict(format='stepstone-project',version=1,data=copy.deepcopy(before))
        backup['data'].update(tests={k:dict(passed=True) for k in projects.CASES},explanation='Forged completion',review=dict(observed=True))
        r=self.call(c,'restore',backup=backup)
        self.assertNotIn('tests',r['project']['data']);self.assertNotIn('review',r['project']['data'])
        bad=copy.deepcopy(backup);bad['data']['items'].append(dict(bad['data']['items'][0]))
        self.call(c,'restore',status=400,backup=bad)
        self.assertEqual(len(c.request('/api/me')[1]['project']['data']['items']),1)

    def test_prediction_changes_and_mentor_review(self):
        c,me=self.built();r=self.call(c,'test',case='empty',prediction='added')
        self.assertFalse(r['project']['data']['tests']['empty']['passed'])
        for case in projects.CASES:r=self.call(c,'test',case=case,prediction='added' if case=='normal' else 'unchanged')
        r=self.call(c,'explain',explanation='I tested adding a name and rejecting empty names, then checked my backup.',accessNote='Synthetic viewport record.',backupNote='Synthetic backup record.')
        self.assertTrue(projects.ready(r['project']))
        review=dict(learner=me['id'],revision=r['project']['revision'],note='Synthetic review only.',demonstrated=True)
        self.assertEqual(c.request('/api/mentor/project-review',review)[0],401)
        self.assertEqual(self.mentor.request('/api/mentor/project-review',dict(review,demonstrated=1))[0],400)
        self.assertEqual(self.mentor.request('/api/mentor/project-review',review)[0],200)
        self.assertEqual(self.mentor.request('/api/mentor/project-review',review)[0],409)
        r=self.call(c,'add',label='Lunch',value='')
        self.assertFalse(projects.ready(r['project']))
        self.assertLess(r['project']['data']['review']['revision'],r['project']['revision'])

    def test_rule_and_export_parity_for_four_app_types(self):
        vectors=[]
        for kind in projects.KINDS:
            for label,raw in [('Ok','2.50'),('Ok','2'),('','2'),('x'*81,'1'),('Ok','-1'),('Ok','many'),('Ok','0')]:
                data=dict(PLAN,kind=kind,items=[]);expected=copy.deepcopy(data)
                try:projects.add(expected,label,raw);error=None
                except ValueError as e:error=str(e)
                vectors.append(dict(data=data,label=label,value=raw,expected=expected,error=error))
        script="""import {projectRules,projectDocument} from './public/project-runtime.js';let input='';for await(const c of process.stdin)input+=c;const rules=projectRules();const v=JSON.parse(input);for(const row of v){let error=null;try{rules.add(row.data,row.label,row.value);}catch(e){error=e.message;}if(JSON.stringify(row.data)!==JSON.stringify(row.expected)||error!==row.error)throw Error(JSON.stringify({row,error}));}const doc=projectDocument({...v[0].data,title:'</script><img src=x onerror=alert(1)>'},'test');if(doc.includes('</script><img'))throw Error('Unsafe data escape');if(!doc.includes('Restore this backup'))throw Error('Missing recovery');console.log('Four app types and safe standalone export passed.');"""
        r=subprocess.run(['node','--input-type=module','-e',script],input=json.dumps(vectors),text=True,capture_output=True,encoding='utf-8',cwd=base.server.ROOT)
        self.assertEqual(r.returncode,0,r.stderr)

    def test_sandboxed_preview_runs_only_the_hashed_inline_runtime(self):
        # A sandboxed preview has an opaque origin and cannot load a script from the app, so the
        # page inlines the runtime and the policy allows exactly that text by its SHA-256 hash.
        with urllib.request.urlopen(self.url+'/',timeout=20) as page: policy=page.headers['Content-Security-Policy']
        script_src=next(p for p in policy.split(';') if p.strip().startswith('script-src')).split()
        self.assertEqual(script_src,['script-src',"'self'",base.server.PREVIEW_SCRIPT])
        runtime=(base.server.PUBLIC/'project-preview-runtime.js').read_text(encoding='utf-8')
        self.assertNotIn('</script',runtime.lower())
        script="""import {createHash} from 'node:crypto';import {readFileSync} from 'node:fs';import {projectPreviewDocument} from './public/project-runtime.js';const runtime=readFileSync('public/project-preview-runtime.js','utf8').replace(/\\r\\n?/g,'\\n');const doc=projectPreviewDocument({kind:'checklist',title:'</script><img src=x onerror=alert(1)>',purpose:'A safe preview test.',label:'Item',goal:1,limit:3,behaviours:['Add','Mark','Undo'],items:[]},runtime);if(!doc.endsWith('<script>'+runtime+'<\\/script></html>'))throw Error('The preview must inline the runtime unchanged');const inline=runtime;if(doc.includes('</script><img'))throw Error('Unsafe data escape');console.log("'sha256-"+createHash('sha256').update(inline).digest('base64')+"'");"""
        r=subprocess.run(['node','--input-type=module','-e',script],text=True,capture_output=True,encoding='utf-8',cwd=base.server.ROOT)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(r.stdout.strip(),base.server.PREVIEW_SCRIPT)

    def test_personal_reset_keeps_learner_project(self):
        c,me=self.built();own=self.mentor.request('/api/mentor/learn',{})[1];base.complete_tutorial(self.mentor)
        self.call(self.mentor,'save',data=dict(PLAN,title='My own private plan'))
        self.assertEqual(self.mentor.request('/api/mentor/reset-learning',dict(learner=own['id'],confirmation='RESET MY LEARNING'))[0],200)
        self.assertEqual(c.request('/api/me')[1]['project']['data']['title'],'Shift kit')

if __name__=='__main__':unittest.main()
