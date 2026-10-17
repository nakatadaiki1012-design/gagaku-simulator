#!/usr/bin/env python3
"""note記事の元データ。実行すると次の3つを作ります。
  note_paste.txt … noteにそのまま貼る文章（画像の位置とキャプション入り）
  article.md     … Markdown版
  preview.html   … 画像つきの確認用ページ（ブラウザで開くだけ）
"""
import base64, html, io, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
URL = '【ここにURLを貼る】'

# ('h2'|'h3'|'p'|'li'|'img'|'hr', 内容) 。imgは (ファイル名, キャプション)
BODY = [
 ('p', '音楽の授業で雅楽を扱うとき、いつも困ることがありました。'),
 ('p', '録音を聴かせても、「いま鳴っているのはどの楽器？」「笙と篳篥はどうちがうの？」が、生徒にはなかなか伝わらないのです。映像でも、16人が並んで座っていると、誰が音を出しているのか見分けるのは大変です。'),
 ('p', 'そこで、3Dの雅楽隊が『越天楽』を演奏し、いま誰が鳴らしているかが光で見えるWebアプリを作りました。ブラウザで開くだけで、パソコンでもスマホでも動きます。'),
 ('p', '👉 ' + URL),
 ('hr', ''),

 ('h2', '16人の雅楽隊が、目の前で演奏する'),
 ('p', '舞台には、本番と同じ16人の奏者が座っています。後ろの列に吹物（笙・篳篥・龍笛 各3人）、まん中に弾物（琵琶・箏 各2人）、前に打物（鞨鼓・太鼓・鉦鼓）。いわゆる「三管両絃三鼓」の編成です。'),
 ('img', ('01_stage.jpg', '演奏中の画面。音を出している奏者の足もとに光の輪が広がります。吹物は青、弾物は緑、打物は赤')),
 ('p', '演奏している奏者の足もとには、色つきの光の輪が広がります。だから「いま篳篥が旋律を吹いている」「ここで太鼓がドンと鳴った」が、目でわかります。'),
 ('p', '奏者か楽器名をタップすると、その楽器だけ休ませることができます。「吹物だけ」「打物だけ」のように一つのグループだけを聴くこともできるので、パートごとの役割を聴き比べる授業にも使えます。'),

 ('h2', '本物の『越天楽』にこだわりました'),
 ('p', '旋律を想像で作ることはせず、越天楽の楽譜データ（MIDI）から全パートを取り込みました。篳篥・龍笛の旋律、笙の合竹（和音）、琵琶・箏、鞨鼓・太鼓・鉦鼓まで、すべて楽譜どおりです。'),
 ('p', 'さらに、実際の演奏の録音を解析して、本物に近づけました。'),
 ('li', '速さ：1拍およそ1.5秒（♩≒39）。後半の「加拍子」からは少し速くなる（♩≒44）'),
 ('li', '音の高さ：A＝440Hz（平調）'),
 ('li', '音色と音量のバランス：録音の倍音や響きの長さに合わせて調整'),
 ('li', '入りの順番：龍笛の「音頭」の独奏から始まり、打物 → 笙・篳篥 → ほかの管と琵琶 → 箏 と、順に加わっていく'),
 ('p', '休みの奏者は楽器を膝に下ろし、出番が来ると構え直します。音はすべてブラウザの中で合成しているので、録音ファイルは使っていません。'),

 ('h2', '拍子と形式が、ひと目でわかる'),
 ('p', '画面の下には「拍子の輪」と、曲の形式（A A B B C C A A B ＋留）が並んでいます。'),
 ('img', ('02_console.jpg', '左の輪は小拍子の4拍を一周で表します。太鼓・鉦鼓・鞨鼓の打つ位置に印があり、今どこを演奏しているかが一目でわかります')),
 ('p', '雅楽のリズムの要は太鼓です。弱く打つ「図（ずー）」と、2拍あとに強く打つ「百（どう）」。輪の上でその位置を見ながら聴くと、ゆったりした雅楽の拍の流れがつかみやすくなります。A・B・Cのボタンを押せば、好きな段から聴くこともできます。'),

 ('h2', '楽器を手に取るように、拡大して見られる'),
 ('p', '楽器名の「i」ボタンを押すと、その楽器を3Dで拡大して、ぐるぐる回して見られます。奏者ごと表示して、構え方を確かめることもできます。'),
 ('img', ('03_zoom.jpg', '左から 笙（奏者ごと表示）、琵琶、太鼓。部分の名前をタップすると、読み方と説明が出ます')),
 ('p', '笙の吹口、琵琶の撥面や柱、太鼓の火焔の飾りなど、部分ごとの名前と説明つき。教科書の写真だけではわかりにくい楽器の形が、立体でつかめます。'),

 ('h2', '自分も合奏に参加できる'),
 ('p', '右上の「参加」から楽器を選ぶと、その楽器の自動演奏が止まり、あなたの番になります。流れてくる印に合わせてボタン（パソコンならスペースキー）を押すと音が鳴ります。'),
 ('img', ('04_join.jpg', '篳篥で参加しているところ。篳篥や龍笛は、押しているあいだ音がのびます')),
 ('p', '音の高さは自動なので、楽譜が読めなくても大丈夫。タイミングが合うと「良」「可」と判定が出ます。16人の中の一人として越天楽を演奏する体験ができます。'),

 ('h2', '「しくみ」と用語集で、雅楽の世界を知る'),
 ('p', '画面の文字はできるだけ少なくし、説明は「しくみ」ボタンの中にしまってあります。'),
 ('img', ('05_learn.jpg', '左：「しくみ」では、編成や形式、楽器の役割などを順番に学べます。右：用語集。「舞」で検索して「唐楽」を開いたところ')),
 ('p', '用語集には、国風歌舞（くにぶりのうたまい）、左舞・右舞、唐楽・高麗楽、音取、加拍子、留手など、40以上の雅楽の言葉を入れました。検索もできるので、鑑賞の授業で出てきた言葉をその場で調べられます。'),

 ('h2', '庭と、夜の舞台'),
 ('p', '舞台のまわりは、玉砂利を敷いた日本庭園。松や紅葉、竹垣、石灯籠を置きました。視点は「正面」「真上」「横」から選べ、指やマウスで自由に回せます。'),
 ('img', ('06_garden.jpg', '左：パソコンやスマホをダークモードにすると夜の舞台に。かがり火がゆれます。右：横から見たところ')),

 ('h2', 'スマホでも使えます'),
 ('img', ('07_phone.jpg', 'スマホでの表示。生徒が一人1台で使うこともできます')),
 ('p', 'タブレットやスマホでも同じように動くので、生徒が自分の端末で楽器を休ませたり、拡大図を見たりできます。'),

 ('h2', '使い方'),
 ('li', '下のURLを開く（インストールも登録も不要）'),
 ('li', '再生ボタン（▶）を押す'),
 ('li', '奏者や楽器名をタップして、聴き比べたり、拡大して見たりする'),
 ('p', '👉 ' + URL),
 ('p', '※ スマホで音が出ないときは、マナーモード（消音）を解除してください。'),

 ('h2', 'おわりに'),
 ('p', '雅楽は「聴いてもよくわからない」と言われがちですが、誰が何をしているかが見えると、急に面白くなります。'),
 ('p', '今後は、ほかの曲（五常楽急・陪臚など）も、本物の楽譜データがそろい次第入れていく予定です。授業で使ってみた感想や、「こんな機能がほしい」というご意見があれば、ぜひコメントで教えてください。'),
 ('p', '#雅楽 #越天楽 #音楽の授業 #日本の伝統音楽 #Webアプリ #個人開発'),
]

TITLE = '3Dの雅楽隊と『越天楽』を合奏できるWebアプリを作りました｜いま誰が演奏しているか、光で見える'
HEADER = ('00_header.jpg', '')

def imgs():
    return [HEADER[0]] + [c[0] for k, c in BODY if k == 'img']


def make_txt():
    o = []
    o.append('【使い方】')
    o.append('・タイトルと本文を note の編集画面に貼り付けます（「## 」「### 」の行は見出しにします。貼り付けて見出しにならなかった行は、その行を選んで見出しボタンを押してください）')
    o.append('・「▼画像」の行に来たら、その番号の画像をアップロードし、直後の「キャプション」の文章を画像の下の入力欄に貼ってから、その2行は消します')
    o.append('・見出し画像は 00_header.jpg です（記事の上のカバー画像に設定）')
    o.append('・「【ここにURLを貼る】」はアプリのURLに書き換えてください（2か所）\n・アプリのURLは、たぶん https://nakatadaiki1012-design.github.io/gagaku-simulator/ です（開けるか確かめてから貼ってください）')
    o.append('')
    o.append('==================== ここから下をコピー ====================')
    o.append('')
    o.append('【タイトル】')
    o.append(TITLE)
    o.append('')
    o.append('【本文】')
    o.append('')
    for k, c in BODY:
        if k == 'h2':
            o += ['## ' + c, '']
        elif k == 'h3':
            o += ['### ' + c, '']
        elif k == 'p':
            o += [c, '']
        elif k == 'li':
            o.append('- ' + c)
        elif k == 'hr':
            o += ['---', '']
        elif k == 'img':
            o += ['▼画像 ' + c[0], 'キャプション：' + c[1], '']
        # リストの後ろに空行
        if k == 'li':
            nxt = BODY[BODY.index((k, c)) + 1][0] if BODY.index((k, c)) + 1 < len(BODY) else ''
            if nxt != 'li':
                o.append('')
    o.append('==================== ここまで ====================')
    o.append('')
    o.append('【画像とキャプション一覧】')
    o.append('00_header.jpg … 見出し画像（キャプションなし）')
    for k, c in BODY:
        if k == 'img':
            o.append(f'{c[0]} … {c[1]}')
    return '\n'.join(o) + '\n'


def make_md():
    o = ['# ' + TITLE, '', '<!-- 見出し画像：images/00_header.jpg -->', '']
    prev = ''
    for k, c in BODY:
        if k == 'li' and prev != 'li':
            pass
        if k == 'h2': o += ['## ' + c, '']
        elif k == 'h3': o += ['### ' + c, '']
        elif k == 'p': o += [c, '']
        elif k == 'hr': o += ['---', '']
        elif k == 'li': o.append('- ' + c)
        elif k == 'img': o += [f'![](images/{c[0]})', f'*{c[1]}*', '']
        if prev == 'li' and k != 'li': o.insert(len(o) - 1, '')
        prev = k
    return '\n'.join(o) + '\n'


def b64(fn, w=1100):
    im = Image.open(os.path.join(HERE, 'images', fn)).convert('RGB')
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)))
    b = io.BytesIO(); im.save(b, 'JPEG', quality=80)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()


def make_html():
    e = html.escape
    o = ['<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
         '<title>noteプレビュー</title><style>body{max-width:720px;margin:2rem auto;padding:0 1rem;font-family:"Hiragino Sans","Noto Sans JP",sans-serif;line-height:1.9;color:#222}',
         'h1{font-size:1.6rem;line-height:1.4}h2{font-size:1.4rem;border-bottom:2px solid #ddd;padding-bottom:.2rem;margin-top:2.4rem}h3{font-size:1.15rem;margin-top:2rem}',
         'figure{margin:1.2rem 0}img{width:100%;border-radius:8px}figcaption{font-size:.85rem;color:#666;text-align:center;margin-top:.4rem}',
         '.note{background:#fff7d6;padding:.6rem 1rem;border-radius:8px;font-size:.85rem}</style>',
         '<p class="note">確認用ページです。noteへは「note_paste.txt」の文章を貼り、画像は images フォルダのファイルをアップロードしてください。</p>',
         f'<figure><img src="{b64(HEADER[0])}"><figcaption>（見出し画像）</figcaption></figure>', f'<h1>{e(TITLE)}</h1>']
    inl = False
    for k, c in BODY:
        if k != 'li' and inl: o.append('</ul>'); inl = False
        if k == 'h2': o.append(f'<h2>{e(c)}</h2>')
        elif k == 'h3': o.append(f'<h3>{e(c)}</h3>')
        elif k == 'p': o.append(f'<p>{e(c)}</p>')
        elif k == 'hr': o.append('<hr>')
        elif k == 'li':
            if not inl: o.append('<ul>'); inl = True
            o.append(f'<li>{e(c)}</li>')
        elif k == 'img': o.append(f'<figure><img src="{b64(c[0])}"><figcaption>{e(c[1])}</figcaption></figure>')
    if inl: o.append('</ul>')
    return '\n'.join(o)


if __name__ == '__main__':
    open(os.path.join(HERE, 'note_paste.txt'), 'w').write(make_txt())
    open(os.path.join(HERE, 'article.md'), 'w').write(make_md())
    open(os.path.join(HERE, 'preview.html'), 'w').write(make_html())
    print('ok', len(imgs()), 'images')
