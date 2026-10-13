"""Starting recommendations and real-reward boundaries; synthetic accounts only."""
import copy
import unittest
import test_server as fixtures
from test_server import Client
import server
from placement import evaluate
LEGACY=server.STARTING_POINT.get('legacy',server.STARTING_POINT)


def answer_set(right_by_subject=None, age=12, seed=0):
    data=dict(age=age,seed=seed,answers=[])
    for _ in range(10):
        qid=evaluate(server.STARTING_POINT,data)['next']
        q=next(q for q in LEGACY['questions'] if q['id']==qid)
        right=True if right_by_subject is None else right_by_subject[q['subject']][len(data['answers'])%2]
        data['answers'].append(dict(id=qid,answer=q['answer'] if right else -1,heard=False))
    return data


class StartingPointTests(unittest.TestCase):
    setUp=fixtures.PilotTests.setUp
    tearDown=fixtures.PilotTests.tearDown
    learner=fixtures.PilotTests.learner
    check=fixtures.PilotTests.check

    def test_all_routes_and_age_never_determines_level(self):
        for pattern,expected in [([False,False],1),([False,True],4),([True,False],7),([True,True],10)]:
            choices={s:pattern for s in LEGACY['subjects']}
            for seed in (0,1,65535):
                young=evaluate(server.STARTING_POINT,answer_set(choices,age=5,seed=seed))
                adult=evaluate(server.STARTING_POINT,answer_set(choices,age=25,seed=seed))
                self.assertEqual(young,adult)
                self.assertEqual(set(young['levels'].values()),{expected})
                self.assertEqual(young['average'],expected)
        choices=dict(math=[True,True],reading=[False,False],writing=[False,True],science=[True,False],social=[True,True])
        result=evaluate(server.STARTING_POINT,answer_set(choices))
        self.assertEqual(result['levels'],dict(math=10,reading=1,writing=4,science=7,social=10))
        self.assertEqual(result['average'],6)

    def test_private_resume_replay_and_welcome_points_without_mastery(self):
        child,me=self.learner()
        data=answer_set();data['answers']=data['answers'][:3]
        request=dict(learner=me['id'],revision=0,data=data,result=dict(average=12))
        status,saved,_=child.request('/api/starting-point',request)
        self.assertEqual(status,200);self.assertFalse(saved['result']['complete'])
        self.assertIsNone(saved['result']['average'])
        other=Client(self.url);other.request('/api/login',dict(code=me['recovery']))
        self.assertEqual(other.request('/api/me')[1]['startingPoint'],saved)
        self.assertEqual(child.request('/api/starting-point',request)[1],saved)
        report=self.mentor.request('/api/mentor')[1]['learners'][0]['startingPoint']
        self.assertEqual(report,saved)
        stranger,another=self.learner('Sibling')
        self.assertIsNone(stranger.request('/api/me')[1]['startingPoint'])
        self.assertEqual(stranger.request('/api/starting-point',request)[0],409)
        self.assertEqual(Client(self.url).request('/api/starting-point',request)[0],401)
        self.assertEqual(child.request('/api/starting-point',dict(revision=1,data=answer_set()))[0],200)
        state=child.request('/api/me')[1]
        self.assertEqual(state['points'],5);self.assertEqual(state['mastered'],[])
        self.assertEqual(state['progress'],{});self.assertEqual(state['attempts'],[])

    def test_invalid_ages_answers_and_stale_devices(self):
        child,_=self.learner()
        for age in (None,4,100,12.5,True,'12'):
            self.assertEqual(child.request('/api/starting-point',dict(revision=0,data=dict(age=age,seed=0,answers=[])))[0],400)
        valid=answer_set()
        for mutation in ('wrong-id','too-many','invalid-choice','bool-choice','invalid-seed'):
            data=copy.deepcopy(valid)
            if mutation=='wrong-id': data['answers'][0]['id']='reading-3-a'
            if mutation=='too-many': data['answers']+=data['answers'][:1]
            if mutation=='invalid-choice': data['answers'][0]['answer']=4
            if mutation=='bool-choice': data['answers'][0]['answer']=True
            if mutation=='invalid-seed': data['seed']=-1
            self.assertEqual(child.request('/api/starting-point',dict(revision=0,data=data))[0],400)
        self.assertEqual(child.request('/api/starting-point',dict(revision=0,data=valid))[0],200)
        valid['age']=13
        self.assertEqual(child.request('/api/starting-point',dict(revision=0,data=valid))[0],409)

    def test_personal_separation_and_retake_preserves_work(self):
        self.mentor.request('/api/mentor/learn',{})
        self.assertEqual(self.mentor.request('/api/starting-point',dict(revision=0,data=answer_set(age=25)))[0],200)
        child,_=self.learner()
        checked,_=self.check(child)
        child.request('/api/draft',dict(unit='reading-1',revision=0,data=dict(phase=1,ink=[])))
        child.request('/api/starting-point',dict(revision=0,data=answer_set()))
        low=answer_set({s:[False,False] for s in LEGACY['subjects']})
        child.request('/api/starting-point',dict(revision=1,data=low))
        after=child.request('/api/me')[1]
        self.assertEqual(after['points'],checked['me']['points']+5)
        self.assertEqual(after['mastered'],checked['me']['mastered'])
        self.assertEqual(child.request('/api/drafts')[1]['reading-1']['data']['phase'],1)
        self.assertEqual(self.mentor.request('/api/me')[1]['startingPoint']['result']['average'],10)
        inbox=self.mentor.request('/api/mentor')[1]
        self.assertEqual(len(inbox['learners']),1)
        self.assertEqual(inbox['learners'][0]['startingPoint']['result']['average'],1)

    def test_goal_does_not_spend_and_existing_claim_lifecycle(self):
        child,me=self.learner()
        reward=self.mentor.request('/api/mentor/reward',dict(title='Build a model',description='Agreed kit up to five dollars.',cost=20))[1]['id']
        self.assertEqual(child.request('/api/reward-goal',dict(id=reward))[1]['goal'],reward)
        self.assertEqual(child.request('/api/me')[1]['points'],0)
        self.assertEqual(child.request('/api/reward',dict(id=reward))[0],409)
        checked,_=self.check(child)
        self.assertEqual(checked['me']['points'],20)
        claimed=child.request('/api/reward',dict(id=reward))[1]['me']
        self.assertEqual(claimed['points'],0);self.assertEqual(claimed['claims'][0]['status'],'pending')
        claim=claimed['claims'][0]['id']
        self.mentor.request('/api/mentor/claim',dict(id=claim,status='declined',note='Choose a different kit.'))
        self.assertEqual(child.request('/api/me')[1]['points'],20)
        sibling,_=self.learner('Sibling')
        self.assertIsNone(sibling.request('/api/me')[1]['goal'])
        self.assertEqual(sibling.request('/api/reward-goal',dict(id=reward,learner=me['id']))[0],409)
        self.mentor.request('/api/mentor/learn',{})
        self.assertEqual(self.mentor.request('/api/reward-goal',dict(id=reward))[0],400)
        self.assertEqual(self.mentor.request('/api/reward',dict(id=reward))[0],400)


if __name__=='__main__': unittest.main()
