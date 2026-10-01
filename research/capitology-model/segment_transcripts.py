"""Pass 3 transcript segmentation and triage scoring.

Produces broad topic/content-mode labels and review-priority scores. It does not
extract strategic claims or evaluate gameplay. All scores are transparent triage
heuristics for prioritizing later human/model review.
"""
import csv
import json
import math
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SEG_DIR = ROOT / 'captions' / 'segments'
OUTLINE_DIR = ROOT / 'pass03-outlines'

STOP = set('''a an and are as at be because been but by can could did do does doing for from get gets got had has have he her here hers him his how i if in into is it its just like me more most my no not of on one or our out really so some than that the their them then there these they this those to too up us very was we were what when where which who why will with would you your youre weve dont isnt arent thats im ive hes shes theyre gonna wanna kind lot okay ok right actually basically thing things way well yeah um uh also now'''.split())

TOPICS = {
 'macro_space_tempo': {'space','tempo','timing','rotate','rotation','angle','angles','lane','lanes','choke','highground','backline','frontline','pressure','initiative','turn','turns','engage','disengage','stage','staging','map','position','positioning','control','push','pull','setup'},
 'composition_matchups': {'comp','comps','composition','compositions','matchup','matchups','counter','counters','swap','swaps','dive','rush','brawl','poke','split','symmetra','meta','hero','heroes','tankline','backline'},
 'fight_execution_review': {'fight','fights','kill','kills','death','dies','died','target','focus','cooldown','cooldowns','ultimate','ult','ults','engagement','reengage','trade','trades','fightplan','overextend','reset'},
 'player_decisions_mechanics': {'aim','mechanic','mechanics','crosshair','movement','duel','duels','ability','abilities','player','players','decision','decisions','mistake','mistakes','reaction','reactions','accuracy','damage','healing','survive','positioning'},
 'coaching_learning': {'coach','coaching','learn','learning','practice','improve','improvement','review','vod','scrim','scrims','habit','habits','question','questions','understand','explain','concept','rule','rules','rank','ranked'},
 'pro_team_analysis': {'roster','owcs','owl','tournament','korea','korean','falcons','fuel','liquid','nrg','t1','geekay','toronto','washington','raccoon','vendetta','stageplay','contenders'},
 'game_design_meta': {'balance','balanced','design','patch','meta','ban','bans','format','role','roles','season','developer','developers','rework','broken','buff','nerf','fix','system'},
 'career_community_personal': {'career','job','life','content','channel','community','discord','twitter','patreon','video','videos','announcement','personal','burnout','hate','love','creator','youtube'},
}

ANALYTIC = {'because','therefore','means','meaning','reason','result','causes','caused','allows','forces','requires','instead','however','difference','example','concept','rule','pattern','problem','solution','advantage','disadvantage','option','tradeoff','condition','unless','depends','explain','understand','notice'}
DOMAIN = set().union(*TOPICS.values()) | {'overwatch','support','tank','dps','winston','tracer','sojourn','brig','brigitte','genji','echo','hazard','dva','ana','lucio','mercy','bastion','moira','freja','hitscan','wolverine'}
FILLER = {'um','uh','like','basically','literally','honestly','actually','okay','yeah','right','whatever','stuff','thing','things','kinda','sorta'}
ENTERTAIN = {'joke','joking','funny','laugh','lmao','crazy','insane','stupid','dumb','hate','love','bro','guys','chat','meme','cooked','yapping','yap'}
PROMO = {'subscribe','patreon','discord','twitter','sponsor','sponsored','channel','comment','comments','link','description','membership','members','video','videos'}
DEICTIC = {'here','there','this','that','these','those','look','watch','see','screen','left','right','top','bottom','behind','front','angle','cursor','clip','replay'}
TRANSITIONS = ('all right','alright','now ','next ','so ','anyway','moving on','let us','lets ','but ','okay ','the next','another thing','first ','second ','third ','finally')

def clamp(x): return int(round(max(0, min(100, x))))
def tokens(text): return re.findall(r"[a-z0-9][a-z0-9’'-]*", text.lower())
def count_set(ts, vocab): return sum(t in vocab for t in ts)
def fmt(ms):
    s=max(0,ms//1000); return f'{s//3600:02}:{s%3600//60:02}:{s%60:02}'

def similarity(a,b):
    aa=Counter(t for t in tokens(a) if t not in STOP);bb=Counter(t for t in tokens(b) if t not in STOP)
    if not aa or not bb:return 0
    dot=sum(aa[k]*bb.get(k,0) for k in aa)
    return dot/(math.sqrt(sum(v*v for v in aa.values()))*math.sqrt(sum(v*v for v in bb.values())))

def boundary_score(ss, idx, target_ms):
    current=ss[idx];nxt=ss[idx+1] if idx+1<len(ss) else current
    gap=max(0,nxt['start_ms']-current['end_ms'])/1000
    phrase=nxt['text'].lower().strip()
    cue=max((3 if phrase.startswith(c) else 0 for c in TRANSITIONS),default=0)
    before=' '.join(s['text'] for s in ss[max(0,idx-10):idx+1])
    after=' '.join(s['text'] for s in ss[idx+1:min(len(ss),idx+12)])
    shift=1-similarity(before,after)
    proximity=1-abs(current['end_ms']-target_ms)/90000
    return 2.5*min(gap,8)/8 + cue + 2*shift + proximity

def divide(ss, duration_ms):
    if not ss:return []
    if duration_ms<=100000:return [(0,len(ss))]
    groups=[];start=0
    while start<len(ss):
        begin=ss[start]['start_ms'];remain=ss[-1]['end_ms']-begin
        if remain<=270000:
            groups.append((start,len(ss)));break
        low=begin+120000; high=begin+250000; target=begin+185000
        candidates=[i for i in range(start,len(ss)-1) if low<=ss[i]['end_ms']<=high]
        if not candidates:
            candidates=[min(range(start,len(ss)-1),key=lambda i:abs(ss[i]['end_ms']-target))]
        cut=max(candidates,key=lambda i:boundary_score(ss,i,target))
        if cut<start:cut=start
        groups.append((start,cut+1));start=cut+1
    # Avoid a tiny final tail by merging it into its predecessor.
    if len(groups)>1:
        a,b=groups[-1]
        if ss[b-1]['end_ms']-ss[a]['start_ms']<70000:
            groups[-2]=(groups[-2][0],b);groups.pop()
    return groups

def keywords(ts,n=8):
    uni=Counter(t for t in ts if t not in STOP and len(t)>2)
    # Favor recurring domain-specific words; keep names/other terms available.
    scored=[(c*(1.7 if w in DOMAIN else 1),w) for w,c in uni.items()]
    return [w for _,w in sorted(scored,reverse=True)[:n]]

def score_segment(text,title,duration,short=False):
    ts=tokens(text); n=max(1,len(ts)); per100=lambda c:100*c/n
    topic_scores={k:sum(1 for t in ts if t in vocab)+2*sum(1 for t in tokens(title) if t in vocab) for k,vocab in TOPICS.items()}
    ordered=sorted(topic_scores.items(),key=lambda x:(x[1],x[0]),reverse=True)
    primary=ordered[0][0] if ordered[0][1] else 'mixed_other'
    tags=[k for k,v in ordered if v>=max(2,ordered[0][1]*0.45)][:3]
    analytic=per100(count_set(ts,ANALYTIC));domain=per100(count_set(ts,DOMAIN));filler=per100(count_set(ts,FILLER));ent=per100(count_set(ts,ENTERTAIN));promo=per100(count_set(ts,PROMO));deictic=per100(count_set(ts,DEICTIC))
    causal=sum(1 for t in ts if t in {'because','means','reason','therefore','allows','forces','requires','depends','unless','instead','however'})
    specificity=len(set(t for t in ts if t in DOMAIN))
    word_rate=60*n/max(1,duration)
    seriousness=clamp(60+3.7*analytic+0.75*domain+0.6*causal-1.4*ent-1.1*promo-0.55*filler)
    density=clamp(30+1.65*domain+3.2*analytic+1.2*causal+0.9*min(specificity,20)-0.9*filler)
    base={'macro_space_tempo':82,'composition_matchups':80,'fight_execution_review':80,'player_decisions_mechanics':76,'coaching_learning':72,'pro_team_analysis':69,'game_design_meta':55,'career_community_personal':28,'mixed_other':45}[primary]
    relevance=clamp(base+0.7*domain+0.5*analytic-1.5*promo)
    weird_rate=max(0,word_rate-230)/5+max(0,85-word_rate)/4
    repeated=sum(a==b for a,b in zip(ts,ts[1:]))*100/n
    very_short=sum(len(s)<=2 for s in ts)*100/n
    confidence=clamp(89-0.6*weird_rate-1.2*repeated-0.25*very_short-(5 if short and n<40 else 0))
    visual=clamp(0.42*relevance+0.22*density+2.2*deictic+0.16*(100-confidence))
    if primary=='career_community_personal':visual=clamp(visual-18)
    if promo>2:visual=clamp(visual-10)
    if short: visual=clamp(visual+5)
    speaker_markers=text.count('>>')
    if promo>2 and relevance<45:mode='promotion_housekeeping'
    elif primary=='career_community_personal':mode='personal_editorial'
    elif speaker_markers>=3 and ('ft.' in title.lower() or 'gang watches' in title.lower()):mode='collaborative_discussion'
    elif 'pro_team_analysis' in tags and analytic<1.0 and deictic>2.5:mode='match_commentary'
    elif short:mode='short_analysis_or_highlight'
    elif seriousness>=63 and density>=50:mode='analytical_explanation'
    elif ent>2.5 and analytic<1.0 and density<50:mode='entertainment_banter'
    else:mode='mixed_discussion'
    return {'primary_topic':primary,'topic_tags':tags,'content_mode':mode,'seriousness':seriousness,
            'information_density':density,'strategic_relevance':relevance,'transcript_confidence':confidence,
            'visual_review_priority':visual,'keywords':keywords(ts),
            'features':{'words':n,'words_per_minute':round(word_rate,1),'analytic_markers_per_100w':round(analytic,2),
                        'domain_terms_per_100w':round(domain,2),'filler_per_100w':round(filler,2),
                        'entertainment_markers_per_100w':round(ent,2),'promotion_markers_per_100w':round(promo,2),
                        'visual_reference_terms_per_100w':round(deictic,2)}}

def main():
    inv=json.loads((ROOT/'pass01_public_index.json').read_text())
    all_rows=[]; videos=[]; OUTLINE_DIR.mkdir(exist_ok=True)
    for video in inv['videos']:
        doc=json.loads((SEG_DIR/(video['video_id']+'.json')).read_text());ss=doc['segments'];groups=divide(ss,video['duration_seconds']*1000);rows=[]
        for number,(a,b) in enumerate(groups,1):
            chunk=ss[a:b];text=' '.join(s['text'].replace('\n',' ') for s in chunk);start=chunk[0]['start_ms'];end=chunk[-1]['end_ms'];scores=score_segment(text,video['title'],max(1,(end-start)/1000),video['duration_seconds']<=90)
            excerpt=re.sub(r'\s+',' ',text).strip()[:280]
            row={'segment_id':f'{video["video_id"]}:{number:03}','video_id':video['video_id'],'video_title':video['title'],'upload_date':video['upload_date'],'segment_number':number,
                 'start_ms':start,'end_ms':end,'start':fmt(start),'end':fmt(end),'duration_seconds':round((end-start)/1000,3),'excerpt':excerpt,
                 **scores,'source_segment_file':f'captions/segments/{video["video_id"]}.json'}
            rows.append(row);all_rows.append(row)
        def avg(k):return round(sum(r[k]*r['duration_seconds'] for r in rows)/sum(r['duration_seconds'] for r in rows),1)
        videos.append({'video_id':video['video_id'],'title':video['title'],'upload_date':video['upload_date'],'duration_seconds':video['duration_seconds'],'segment_count':len(rows),
                       **{f'average_{k}':avg(k) for k in ['seriousness','information_density','strategic_relevance','transcript_confidence','visual_review_priority']},
                       'primary_topics':Counter(r['primary_topic'] for r in rows).most_common(4),'content_modes':Counter(r['content_mode'] for r in rows).most_common()})
        lines=[f'# {video["title"]}','',f'Video ID: `{video["video_id"]}`  ',f'Upload date: {video["upload_date"]}  ',f'Duration: {video["duration"]}  ',f'Segments: {len(rows)}','',
               '| # | Time | Topic | Mode | Serious | Density | Relevance | Transcript | Visual | Keywords |','|---:|---|---|---|---:|---:|---:|---:|---:|---|']
        for r in rows:lines.append(f'| {r["segment_number"]} | {r["start"]}–{r["end"]} | {r["primary_topic"]} | {r["content_mode"]} | {r["seriousness"]} | {r["information_density"]} | {r["strategic_relevance"]} | {r["transcript_confidence"]} | {r["visual_review_priority"]} | {", ".join(r["keywords"][:5])} |')
        (OUTLINE_DIR/(video['video_id']+'.md')).write_text('\n'.join(lines)+'\n')
    with (ROOT/'pass03_segments.jsonl').open('w') as f:
        for r in all_rows:f.write(json.dumps(r,ensure_ascii=False)+'\n')
    cols=['segment_id','video_id','video_title','upload_date','segment_number','start','end','duration_seconds','primary_topic','topic_tags','content_mode','seriousness','information_density','strategic_relevance','transcript_confidence','visual_review_priority','keywords','excerpt','source_segment_file']
    with (ROOT/'pass03_segments.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=cols);w.writeheader()
        for r in all_rows:
            d={k:r[k] for k in cols};d['topic_tags']=';'.join(d['topic_tags']);d['keywords']=';'.join(d['keywords']);w.writerow(d)
    result={'schema_version':1,'pass':3,'status':'generated_pending_audit','method':'deterministic transcript-boundary and transparent lexical triage scoring; no gameplay/claim analysis',
            'score_scale':'0-100; intended for relative corpus triage, not calibrated probabilities or quality grades',
            'summary':{'videos':len(videos),'segments':len(all_rows),'duration_seconds':sum(v['duration_seconds'] for v in inv['videos']),
                       'topic_counts':Counter(r['primary_topic'] for r in all_rows),'mode_counts':Counter(r['content_mode'] for r in all_rows)},
            'videos':videos}
    (ROOT/'pass03_video_index.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
