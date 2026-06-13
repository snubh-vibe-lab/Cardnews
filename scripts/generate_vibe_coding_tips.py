from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap, math, shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '2026' / '06' / 'vibe-coding-agentic-tips'
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920
NAVY = '#102744'
NAVY2 = '#17365a'
CREAM = '#F2EEE5'
INK = '#0E243F'
SLATE = '#40516B'
MUTED = '#9AAAC2'
GREEN = '#22C55E'
MINT = '#DDF8E8'
SKY = '#DCEBFF'
LILAC = '#EEE8FF'
YELLOW = '#FFF3C4'
CORAL = '#FFE2D7'
WHITE = '#FBFAF6'

FONT_REG = '/System/Library/Fonts/AppleSDGothicNeo.ttc'
FONT_MONO = '/System/Library/Fonts/Menlo.ttc'

def font(size, mono=False):
    return ImageFont.truetype(FONT_MONO if mono else FONT_REG, size)

F = {
    'brand': font(52, True), 'mono': font(33, True), 'mono_sm': font(27, True), 'code': font(30),
    'kicker': font(38, True), 'title': font(112), 'title_mid': font(92),
    'title_sm': font(78), 'body': font(56), 'body_sm': font(48),
    'cap': font(38), 'tiny': font(29, True), 'badge': font(34, True)
}

def wrap(text, width):
    lines=[]
    for p in str(text).split('\n'):
        if not p.strip():
            lines.append('')
        else:
            lines += textwrap.wrap(p, width=width, break_long_words=False, replace_whitespace=False)
    return lines

def line_h(fnt, sample='가'):
    b=fnt.getbbox(sample)
    return b[3]-b[1]

def draw_text(d, text, xy, fnt, fill, width=18, gap=12, max_lines=None, align='left'):
    x,y=xy
    lines=wrap(text,width)
    if max_lines and len(lines)>max_lines:
        lines=lines[:max_lines]
        lines[-1]=lines[-1].rstrip(' .,')+'…'
    for line in lines:
        xx=x
        if align!='left':
            b=d.textbbox((0,0), line, font=fnt)
            tw=b[2]-b[0]
            if align=='center': xx=x-tw/2
            elif align=='right': xx=x-tw
        d.text((xx,y), line, font=fnt, fill=fill)
        y += line_h(fnt,line or '가') + gap
    return y

def logo(d, dark=True):
    c = CREAM if dark else INK
    sub = MUTED if dark else '#8090A8'
    d.text((724,122), '{ vibe.lab }', font=F['brand'], fill=c)
    d.text((848,148), '.', font=F['brand'], fill=GREEN)
    d.line((742,240,938,240), fill=sub, width=3)
    d.line((805,240,812,232,820,250,826,240), fill=sub, width=3)
    d.line((880,240,888,228,896,252,904,240), fill=sub, width=3)
    d.text((752,268), 'SNUBH · ESTABLISHED CLINICIANS', font=F['tiny'], fill=sub)

def footer(d, idx, total, dark=True):
    c = MUTED if dark else SLATE
    d.text((96,1776), f'{idx:02d} · {total:02d}', font=F['mono_sm'], fill=c)
    d.text((836,1776), 'SWIPE →', font=F['mono_sm'], fill=c)

def bg(kind='dark'):
    base = NAVY if kind=='dark' else CREAM
    im=Image.new('RGB',(W,H),base)
    d=ImageDraw.Draw(im)
    if kind=='dark':
        for r,col in [(780,'#153456'),(520,'#193C63'),(300,'#1D4B78')]:
            d.ellipse((W-r//2,-r//3,W+r//2,r), fill=col)
        d.rectangle((0,0,W,H), fill=(0,0,0,0))
    else:
        d.rounded_rectangle((650,120,1000,390), radius=36, fill='#F7F3EA')
        d.ellipse((-220,1180,360,1760), fill='#E8F5EF')
        d.rectangle((0,0,W,H), outline=None)
    return im

def tag(d, text, xy, fill=GREEN, dark=True):
    x,y=xy
    b=d.textbbox((0,0), text, font=F['kicker'])
    d.rounded_rectangle((x-18,y-12,x+b[2]+28,y+b[3]+18), radius=18, fill=fill)
    d.text((x,y), text, font=F['kicker'], fill=INK)

def card_box(d, xy, text, title=None, fill=WHITE, accent=GREEN, icon='>'):
    x1,y1,x2,y2=xy
    d.rounded_rectangle(xy, radius=28, fill=fill, outline='#D8DFE8', width=2)
    d.rectangle((x1,y1,x1+12,y2), fill=accent)
    d.text((x1+34,y1+32), icon, font=F['mono'], fill=accent)
    y=y1+30
    if title:
        d.text((x1+88,y), title, font=F['body_sm'], fill=INK)
        y += 76
    draw_text(d, text, (x1+88,y), F['cap'], SLATE, width=23, gap=10, max_lines=4)

def terminal_box(d, xy, lines):
    x1,y1,x2,y2=xy
    d.rounded_rectangle(xy, radius=30, fill='#0B1C31', outline='#31506E', width=3)
    for i,c in enumerate(['#FF5F56','#FFBD2E','#27C93F']):
        d.ellipse((x1+34+i*38,y1+32,x1+58+i*38,y1+56), fill=c)
    y=y1+94
    for line in lines:
        color=GREEN if line.startswith('$') or line.startswith('>') else CREAM
        d.text((x1+44,y), line, font=F['code'], fill=color)
        y += 56

def stamp(d, xy, text='VL CHECK'):
    x,y=xy
    d.rounded_rectangle((x,y,x+260,y+82), radius=18, outline=GREEN, width=5)
    d.text((x+30,y+22), text, font=F['badge'], fill=GREEN)

def make(kind, topic_no, slide_no, total, section, title, subtitle='', body=None, bullets=None, code=None, callout=None, filename='x.png'):
    dark = kind in ['cover','dark','terminal']
    im=bg('dark' if dark else 'light')
    d=ImageDraw.Draw(im)
    logo(d, dark=dark)
    footer(d, slide_no, total, dark=dark)
    if kind=='cover':
        d.text((96,330), f'// 2026.06 · CARD NEWS', font=F['mono'], fill=MUTED)
        d.text((96,665), f'{topic_no:02d} · {section.upper()}', font=F['kicker'], fill=GREEN)
        draw_text(d, title, (96,790), F['title'], CREAM, width=9, gap=22, max_lines=3)
        draw_text(d, subtitle, (96,1320), F['body_sm'], MUTED, width=19, gap=16, max_lines=3)
        d.line((96,1255,260,1255), fill=MUTED, width=3)
    elif kind=='rule':
        d.text((96,285), f'// {section.upper()} · {slide_no:02d}', font=F['mono_sm'], fill=SLATE)
        tag(d, 'POINT', (96,390))
        draw_text(d, title, (96,520), F['title_mid'], INK, width=10, gap=20, max_lines=3)
        if subtitle:
            draw_text(d, subtitle, (96,850), F['body_sm'], SLATE, width=19, gap=15, max_lines=3)
        if bullets:
            y=1110
            for b in bullets:
                card_box(d,(96,y,984,y+165),b,fill=WHITE,accent=GREEN)
                y+=198
    elif kind=='compare':
        d.text((96,285), f'// {section.upper()} · {slide_no:02d}', font=F['mono_sm'], fill=SLATE)
        draw_text(d, title, (96,390), F['title_mid'], INK, width=11, gap=18, max_lines=2)
        card_box(d,(96,720,984,1045),body[0],title='흔한 요청',fill='#FFF8F4',accent='#FF7A59',icon='×')
        card_box(d,(96,1105,984,1450),body[1],title='좋은 요청',fill='#F4FFF8',accent=GREEN,icon='✓')
        if callout:
            draw_text(d, callout, (96,1532), F['cap'], SLATE, width=24, gap=12, max_lines=2)
    elif kind=='terminal':
        d.text((96,300), f'// {section.upper()} · {slide_no:02d}', font=F['mono_sm'], fill=MUTED)
        draw_text(d, title, (96,430), F['title_mid'], CREAM, width=10, gap=18, max_lines=2)
        terminal_box(d,(96,820,984,1340),code or [])
        if callout:
            d.rounded_rectangle((96,1415,984,1605), radius=28, fill='#17365A', outline='#31506E', width=2)
            draw_text(d, callout, (136,1460), F['cap'], CREAM, width=24, gap=12, max_lines=3)
    elif kind=='check':
        d.text((96,285), f'// {section.upper()} · {slide_no:02d}', font=F['mono_sm'], fill=SLATE)
        draw_text(d, title, (96,390), F['title_mid'], INK, width=10, gap=18, max_lines=2)
        y=700
        for i,b in enumerate(bullets or [],1):
            d.rounded_rectangle((96,y,984,y+158), radius=24, fill=[SKY,MINT,LILAC,YELLOW,CORAL][(i-1)%5], outline='#D8DFE8', width=2)
            d.text((130,y+42), f'{i:02d}', font=F['mono'], fill=GREEN)
            draw_text(d,b,(230,y+38),F['cap'],INK,width=22,gap=8,max_lines=2)
            y += 188
        if callout:
            stamp(d,(96,1560))
            draw_text(d, callout, (390,1564), F['cap'], SLATE, width=16, gap=10, max_lines=2)
    im.save(OUT/filename, quality=96)
    return OUT/filename

topics=[
('file-first','고칠 파일부터 찍어주기','“전체를 알아서”보다 “여기만 고쳐줘”가 정확합니다.',[
('cover','고칠 파일부터\n찍어주기','AI에게 일을 작게 잘라 맡기는 첫 습관',None,None,None),
('compare','요청 범위를\n좁혀주세요','파일과 함수가 보이면 추측이 줄어듭니다.',['“로그인 기능 만들어줘”\n→ 관련 파일을 AI가 추측하고 여러 곳을 건드립니다.','“LoginForm의 submit 함수만 고쳐줘”\n→ 수정 범위가 작고 리뷰하기 쉽습니다.'],None,'큰 부탁보다 작은 지시가 더 빠릅니다.'),
('rule','파일 · 함수 · 결과','세 가지를 같이 적으면 충분합니다.',['파일: `src/LoginForm.tsx`','함수: `handleSubmit()`','결과: 실패 메시지를 화면에 표시'],None,None),
('terminal','복붙 프롬프트','',None,['$ 수정 범위: src/LoginForm.tsx','> handleSubmit만 수정','> CSS와 DB는 건드리지 말 것','> npm test로 확인'], '“어디를 고칠지”를 먼저 정하면 바이브 코딩이 안정됩니다.'),
('check','기억할 한 줄','',None,['AI는 프로젝트 전체보다 작은 맥락에서 강합니다.','먼저 파일을 찍고, 그 다음 수정시킵니다.','리뷰 가능한 크기로 일을 쪼갭니다.'],'작게 맡기기')]),
('3-line-brief','요구사항은 3줄로 쪼개기','목적 · 제약 · 확인방법만 분리해도 결과가 달라집니다.',[
('cover','요구사항은\n3줄이면 충분합니다','목적 / 제약 / 확인방법',None,None,None),
('rule','1줄째: 목적','무엇을 만들지 한 문장으로 씁니다.',['환자 목록에 검색 필터 추가','카드뉴스 제목 5개 제안','회의록에서 액션 아이템 추출'],None,None),
('rule','2줄째: 제약','하지 말아야 할 일을 먼저 알려줍니다.',['기존 UI 유지','DB schema 변경 금지','외부 API 호출 금지'],None,None),
('rule','3줄째: 확인','완료 기준을 숫자와 명령으로 정합니다.',['테스트 명령: `npm test`','결과 형식: 변경 파일 / 실행 결과','스크린샷 또는 미리보기 포함'],None,None),
('terminal','복붙 프롬프트','',None,['$ 목적: 표 필터 추가','> 제약: 디자인 변경 금지','> 확인: 테스트와 스크린샷','> 보고: 파일/명령/결과'], '좋은 프롬프트는 길이가 아니라 구조입니다.')]),
('read-first','수정 전에 읽기만 시키기','첫 턴은 고치지 말고 구조를 읽게 하세요.',[
('cover','수정 전에\n읽기만 시키기','Agentic AI 안전 습관',None,None,None),
('compare','바로 수정은\n위험합니다','',['“에러 고쳐줘”\n→ 비슷한 파일을 잘못 건드릴 수 있습니다.','“관련 파일 찾고 구조만 요약해줘”\n→ 수정 전 판단 근거가 생깁니다.'],None,'조사와 수정을 한 턴에 섞지 마세요.'),
('check','읽기 전용 지시','',None,['수정하지 말 것','관련 파일 3~5개만 찾기','데이터 흐름 요약','위험한 변경점 표시'],'첫 턴은 조사') ,
('terminal','다음 턴에서\n수정 승인','',None,['$ 2번 파일만 수정해줘','> 삭제/이동 금지','> 테스트는 이 명령으로','> 실패하면 멈추고 보고'], '읽기 → 승인 → 수정 순서가 안전합니다.'),
('check','기억할 한 줄','',None,['AI가 먼저 읽으면 수정 범위가 줄어듭니다.','요약을 보고 사람이 방향을 잡습니다.','수정은 두 번째 턴부터 시작합니다.'],'먼저 읽기')]),
('permission','Agent에게 권한 경계 주기','자율성이 높을수록 금지선을 먼저 줘야 합니다.',[
('cover','Agent에게\n권한 경계를 주세요','허용 / 금지 / 확인',None,None,None),
('rule','허용할 일','여기까지는 스스로 해도 됩니다.',['파일 읽기','지정 파일 수정','테스트 실행','로컬 미리보기 생성'],None,None),
('rule','금지할 일','자동으로 하면 안 되는 일을 명확히 합니다.',['배포 금지','실데이터 삭제 금지','비밀키 출력 금지','메일 발송 금지'],None,None),
('rule','확인받을 일','한 번 더 묻고 진행해야 합니다.',['외부 전송','DB migration','권한 변경','대량 파일 수정'],None,None),
('terminal','복붙 프롬프트','',None,['$ 허용: 파일 읽기/테스트','> 금지: 배포/삭제/전송','> 확인: DB/권한/대량변경','> 보고: 변경·검증·리스크'], 'Agentic AI의 핵심은 자율성 + 안전장치입니다.')]),
('evidence','“안 돼” 대신 증거를 주기','로그·스크린샷·재현 순서가 해결률을 올립니다.',[
('cover','“안 돼” 대신\n증거를 주세요','디버깅 프롬프트 팁',None,None,None),
('check','최소 3종 세트','',None,['에러 마지막 30~50줄','문제가 보이는 스크린샷','클릭/입력 재현 순서'],'증거 3종'),
('rule','좋은 설명','상황을 재현 가능하게 만듭니다.',['무엇을 눌렀는지','기대한 화면은 무엇인지','실제로 나온 에러는 무엇인지'],None,None),
('rule','빼야 할 것','증거는 주되 비밀은 지웁니다.',['비밀번호','API key / token','주민번호','환자정보'],None,None),
('terminal','복붙 프롬프트','',None,['$ 재현: A 클릭 → B 입력','> 에러: console 50줄','> 기대: 목록이 갱신되어야 함','> 비밀값은 [REDACTED]'], 'AI는 감보다 증거를 잘 읽습니다.')]),
('report','결과 보고 형식을 정해두기','“완료했습니다” 대신 검증 가능한 보고를 받습니다.',[
('cover','결과 보고는\n형식을 정해두기','변경 / 실행 / 결과 / 리스크',None,None,None),
('rule','보고 4칸','이 네 가지를 항상 요구하세요.',['무엇을 바꿨나','무슨 명령을 실행했나','실제 결과는 무엇인가','남은 위험은 무엇인가'],None,None),
('compare','나쁜 보고와\n좋은 보고','',['“수정 완료했습니다.”\n→ 무엇이 바뀌었는지 검증하기 어렵습니다.','“3개 파일 수정, 47 tests passed.”\n→ 바로 리뷰할 수 있습니다.'],None,'숫자와 명령이 들어간 보고가 좋습니다.'),
('terminal','복붙 프롬프트','',None,['$ 보고 형식','> 변경 파일','> 실행 명령','> 실제 출력','> 남은 리스크'], '결과보다 중요한 건 검증의 흔적입니다.'),
('check','기억할 한 줄','',None,['보고를 짧게 받아도 됩니다.','단, 실행한 명령과 결과는 빠지면 안 됩니다.','실패한 시도도 함께 남깁니다.'],'검증 가능한 완료')]),
('template','자주 쓰는 지시는 템플릿으로 저장','반복 프롬프트는 개인 노하우가 아니라 팀 자산입니다.',[
('cover','자주 쓰는 지시는\n템플릿으로 저장','나만의 AI 업무 레시피',None,None,None),
('rule','템플릿 후보','반복되는 일을 고릅니다.',['버그 수정','회의자료 만들기','카드뉴스 제작','메일 답장 초안'],None,None),
('rule','템플릿 구성','네 칸이면 충분합니다.',['역할','입력자료','출력형식','금지사항'],None,None),
('terminal','짧은 템플릿 예시','',None,['$ 역할: 코드 리뷰어','> 입력: diff와 에러 로그','> 출력: 위험도별 목록','> 금지: 코드 수정'], '잘 된 지시문은 저장해두고 다음에 재사용합니다.'),
('check','팀으로 확장','',None,['README에 사용법 저장','templates/에 지시문 모으기','examples/에 좋은 결과 보관','체크리스트로 리뷰 기준 통일'],'프롬프트도 운영 자산')])
]

made=[]
for ti,(code,main,sub,slides) in enumerate(topics,1):
    for si,(kind,title,subtitle,body,bullets,callout) in enumerate(slides,1):
        if kind in ['rule','check'] and bullets is None and isinstance(body, list):
            bullets, body = body, None
        made.append(make(kind,ti,si,5,code,title,subtitle,body,bullets,bullets if kind=='terminal' else None,callout,f'Cardnews_20260613_vibe_tip_{ti:02d}_{si:02d}.png'))

cols=5; tw,th=216,384; rows=math.ceil(len(made)/cols)
sheet=Image.new('RGB',(cols*tw,rows*th),CREAM)
for i,p in enumerate(made):
    im=Image.open(p).resize((tw,th), Image.Resampling.LANCZOS)
    sheet.paste(im,((i%cols)*tw,(i//cols)*th))
sheet.save(OUT/'contact_sheet_vibe_tips.png', quality=94)

readme=['# Vibe Coding & Agentic AI Tips Cardnews','', '기존 월례모임 발표 주제형 안은 폐기하고, 바로 따라 할 수 있는 바이브 코딩·agentic AI 실전 팁 카드뉴스로 재작성했습니다.', '', '- 총 7개 토픽 × 5장 = 35장', '- 기존 6월 카드뉴스의 navy/cream/green 팔레트와 vibe.lab 브랜딩을 맞췄습니다.', '- 각 묶음은 cover → principle → example → template → VL check 흐름을 따릅니다.', '', '## Topics']
for i,(code,main,sub,slides) in enumerate(topics,1):
    readme.append(f'{i}. {main} — 5 cards')
readme += ['', '## Preview', '', '![contact sheet](contact_sheet_vibe_tips.png)']
(OUT/'README.md').write_text('\n'.join(readme), encoding='utf-8')
print('generated',len(made),'cards')
print(OUT/'contact_sheet_vibe_tips.png')
