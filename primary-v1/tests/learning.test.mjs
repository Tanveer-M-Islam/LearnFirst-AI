import test from 'node:test';
import assert from 'node:assert/strict';
import {lessons,grade,numeric,newSession,questionFor,advance,practiceSet,score,tutorHint} from '../lib/learning.ts';
test('fraction grading accepts equivalent values and rejects invalid or nonfinite input',()=>{
 const q=lessons[0].foundation[1];
 for(const a of ['3/4','6/8','0.75',' 3 / 4 '])assert.equal(grade(q,a),true,a);
 for(const a of ['2/6','1/0','Infinity','NaN','','abc','3/4 because yes','1+1'])assert.equal(grade(q,a),false,a);
 assert.equal(numeric('0/0'),null);
});
test('diagnostic chooses foundational or core practice from actual answers',()=>{
 let low=newSession('math'),high=newSession('math');
 for(let i=0;i<3;i++){low=advance(low,'0');high=advance(high,questionFor(high).answer);}
 assert.equal(low.stage,'practice');assert.equal(practiceSet(low)[0].id,'mf1');
 assert.equal(practiceSet(high)[0].id,'mp1');
});
test('all subjects complete diagnostic, two practices, and three independent checks exactly once',()=>{
 for(const lesson of lessons){let s=newSession(lesson.id);const visited=[];
 while(s.stage!=='done'){const q=questionFor(s);assert.ok(q);visited.push(q.id);s=advance(s,q.answer);}
 assert.equal(s.diagnostic.length,3);assert.equal(s.practice.length,2);assert.equal(s.check.length,3);assert.equal(visited.length,8);
 assert.equal(new Set(visited).size,8);assert.equal(score(s.check),100);assert.ok(s.completedAt);assert.deepEqual(advance(s,'extra'),s);
 }
});
test('hint use resets before the independent check and skipped answers count as incorrect',()=>{
 let s=newSession('science');for(let i=0;i<3;i++)s=advance(s,'');
 s={...s,hintLevel:3,attempts:2};s=advance(s,questionFor(s).answer);assert.equal(s.practice[0].hints,3);assert.equal(s.practice[0].attempts,3);assert.equal(s.hintLevel,0);
 s=advance({...s,hintLevel:2},'');assert.equal(s.stage,'check');assert.equal(s.hintLevel,0);assert.equal(s.attempts,0);
 s=advance(s,'');assert.equal(s.check[0].correct,false);assert.equal(s.check[0].hints,0);
});
test('fraction misconceptions receive targeted guidance',()=>{const q=lessons[0].practice[0];assert.match(tutorHint(q,'2/7',0),/adding both top and bottom/);});
test('every practice item has three teaching hints, every answer grades correctly, and IDs are unique',()=>{const ids=new Set();for(const l of lessons)for(const bank of [l.diagnostic,l.foundation,l.practice,l.check])for(const q of bank){assert.ok(!ids.has(q.id));ids.add(q.id);assert.ok(grade(q,q.answer));if(bank===l.practice||bank===l.foundation)assert.equal(q.hints.length,3);}});
