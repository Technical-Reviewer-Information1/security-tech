(function () {
  'use strict';
  const T = window.Tools, $ = id => document.getElementById(id);
  const NS = 'http://www.w3.org/2000/svg';
  function el(n, a, t) { const e = document.createElementNS(NS, n); for (const k in a) if (a[k] != null) e.setAttribute(k, a[k]); if (t != null) e.textContent = t; return e; }
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };

  /* ---------- STEP1 フィルタリング ---------- */
  const SITES = [
    { n: 'WebサイトA', c: '数学' }, { n: 'WebサイトB', c: 'SNS' },
    { n: 'WebサイトC', c: 'ゲーム' }, { n: 'WebサイトD', c: '情報' }
  ];
  const CATS = ['数学', 'SNS', 'ゲーム', '情報'];
  let listCats = new Set(['情報']), listSites = new Set(['WebサイトA', 'WebサイトC']);
  let fmode = 'white';

  function inList(s) { return listSites.has(s.n) || listCats.has(s.c); }
  function drawFilter() {
    const box = $('listEdit'); box.innerHTML = '<span style="font-size:.82rem;color:var(--ink-2);font-weight:700">カテゴリ：</span>';
    CATS.forEach(c => {
      const b = document.createElement('span');
      b.className = 'chip' + (listCats.has(c) ? '' : ' off');
      b.textContent = c;
      b.addEventListener('click', () => { listCats.has(c) ? listCats.delete(c) : listCats.add(c); drawFilter(); });
      box.appendChild(b);
    });
    const sp = document.createElement('span');
    sp.style.cssText = 'font-size:.82rem;color:var(--ink-2);font-weight:700;margin-left:10px';
    sp.textContent = 'サイト：';
    box.appendChild(sp);
    SITES.forEach(s => {
      const b = document.createElement('span');
      b.className = 'chip' + (listSites.has(s.n) ? '' : ' off');
      b.textContent = s.n.replace('Webサイト', '');
      b.addEventListener('click', () => { listSites.has(s.n) ? listSites.delete(s.n) : listSites.add(s.n); drawFilter(); });
      box.appendChild(b);
    });

    ['mWhite', 'mBlack', 'mBoth'].forEach((id, i) =>
      $(id).setAttribute('aria-pressed', fmode === ['white', 'black', 'both'][i]));
    const both = fmode === 'both';
    let h = '<thead><tr><th>サイト名</th><th>カテゴリ</th><th>リストに載っているか</th>';
    h += both ? '<th>ホワイトリスト方式</th><th>ブラックリスト方式</th>'
      : '<th>' + (fmode === 'white' ? 'ホワイトリスト方式' : 'ブラックリスト方式') + '</th>';
    h += '</tr></thead><tbody>';
    SITES.forEach(s => {
      const inL = inList(s);
      const w = inL, b = !inL;
      h += '<tr><td>' + s.n + '</td><td>' + s.c + '</td><td>' +
        (inL ? '載っている（' + (listSites.has(s.n) ? 'サイト' : 'カテゴリ') + '）' : '載っていない') + '</td>';
      if (both) h += '<td class="' + (w ? 'ok' : 'ng') + '">' + (w ? '○' : '×') + '</td><td class="' + (b ? 'ok' : 'ng') + '">' + (b ? '○' : '×') + '</td>';
      else { const v = fmode === 'white' ? w : b; h += '<td class="' + (v ? 'ok' : 'ng') + '">' + (v ? '○' : '×') + '</td>'; }
      h += '</tr>';
    });
    $('filtTable').innerHTML = h + '</tbody>';
    const n = $('filtNote');
    n.className = 'note info';
    n.innerHTML = both
      ? '<strong>同じリストなのに結果が正反対</strong>になっていることを確かめてください。' +
        'ホワイトリスト方式で○のものは、ブラックリスト方式では必ず×になります。'
      : (fmode === 'white'
        ? 'リストに載っているものだけ<strong>アクセスできます</strong>。載っていないB（SNS）は×です。'
        : 'リストに載っているものだけ<strong>アクセスできません</strong>。載っていないB（SNS）は○です。');
  }

  /* ---------- STEP2 ファイアウォール ---------- */
  const RULES = [
    { no: 1, dir: '外部→内部', port: '80・443（Web）', act: '許可' },
    { no: 2, dir: '外部→内部', port: '22（遠隔操作）', act: '拒否' },
    { no: 3, dir: '外部→内部', port: 'その他すべて', act: '拒否' },
    { no: 4, dir: '内部→外部', port: 'すべて', act: '許可' }
  ];
  const PORTS = [
    { p: 80, n: 'Web閲覧' }, { p: 443, n: 'Web閲覧（暗号化）' }, { p: 22, n: '遠隔操作' },
    { p: 25, n: 'メール送信' }, { p: 3389, n: 'リモートデスクトップ' }, { p: 8080, n: '不明なサービス' }
  ];
  let fwLog = [];
  function drawRules() {
    $('ruleTable').innerHTML = '<thead><tr><th>#</th><th>向き</th><th>対象</th><th>動作</th></tr></thead><tbody>' +
      RULES.map(r => '<tr><td>' + r.no + '</td><td>' + r.dir + '</td><td>' + r.port + '</td><td style="color:' +
        (r.act === '許可' ? 'var(--ok)' : 'var(--ng)') + ';font-weight:700">' + r.act + '</td></tr>').join('') + '</tbody>';
  }
  function judgeFw(dir, port) {
    if (dir === '内部→外部') return { act: '許可', rule: 4 };
    if (port === 80 || port === 443) return { act: '許可', rule: 1 };
    if (port === 22) return { act: '拒否', rule: 2 };
    return { act: '拒否', rule: 3 };
  }
  function sendPkt(n) {
    for (let i = 0; i < n; i++) {
      const dir = Math.random() < .6 ? '外部→内部' : '内部→外部';
      const p = PORTS[Math.floor(Math.random() * PORTS.length)];
      const j = judgeFw(dir, p.p);
      fwLog.unshift({ dir, port: p.p, name: p.n, act: j.act, rule: j.rule });
    }
    fwLog = fwLog.slice(0, 12);
    $('fwTable').innerHTML = '<thead><tr><th>向き</th><th>ポート</th><th>内容</th><th>結果</th><th>適用ルール</th></tr></thead><tbody>' +
      fwLog.map(l => '<tr><td>' + l.dir + '</td><td>' + l.port + '</td><td>' + l.name + '</td><td style="color:' +
        (l.act === '許可' ? 'var(--ok)' : 'var(--ng)') + ';font-weight:700">' + l.act + '</td><td>#' + l.rule + '</td></tr>').join('') + '</tbody>';
    const blocked = fwLog.filter(l => l.act === '拒否').length;
    const n2 = $('fwNote');
    n2.className = 'note info';
    n2.innerHTML = '直近 ' + fwLog.length + ' 件のうち <strong>' + blocked + ' 件を拒否</strong>しました。' +
      '<strong>外から中への通信は必要なものだけ通し、それ以外は止める</strong>のが基本の考え方です。' +
      '中から外への通信は許可されているので、生徒がWebを見ることはできます。';
  }

  /* ---------- STEP3 VLAN ---------- */
  const PCS = [
    { n: '職員室PC', v: 'A', x: 110, y: 60 }, { n: '事務室PC', v: 'A', x: 110, y: 190 },
    { n: '教室PC1', v: 'B', x: 550, y: 60 }, { n: '教室PC2', v: 'B', x: 550, y: 190 }
  ];
  let sel = [];
  function drawVlan() {
    const on = $('vlanOn').checked;
    const W = 660, H = 260;
    const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, width: '100%', role: 'img', 'aria-label': 'VLANの図' });
    svg.appendChild(el('rect', { x: 270, y: 100, width: 120, height: 52, rx: 3, class: 'sw' }));
    svg.appendChild(el('text', { x: 330, y: 122, class: 't' }, 'スイッチ'));
    svg.appendChild(el('text', { x: 330, y: 140, class: 't', 'font-size': 10, fill: '#4a4f57' }, on ? 'VLAN 有効' : 'VLAN 無効'));
    PCS.forEach((p, i) => {
      const canTalk = sel.length === 2 && sel.indexOf(i) >= 0;
      let cls = 'ln';
      if (canTalk) {
        const [a, b] = sel;
        const ok = !on || PCS[a].v === PCS[b].v;
        cls += ok ? ' ok' : ' ng';
      }
      svg.appendChild(el('line', { x1: p.x + (p.x < 330 ? 52 : -52), y1: p.y, x2: 330 + (p.x < 330 ? -60 : 60), y2: 126, class: cls }));
      svg.appendChild(el('rect', { x: p.x - 52, y: p.y - 22, width: 104, height: 44, rx: 3,
        class: 'pcv ' + (on ? p.v.toLowerCase() : 'a') + (sel.indexOf(i) >= 0 ? ' sel' : ''), 'data-i': i }));
      svg.appendChild(el('text', { x: p.x, y: p.y - 2, class: 't' }, p.n));
      svg.appendChild(el('text', { x: p.x, y: p.y + 14, class: 't', 'font-size': 9.5, fill: '#4a4f57' },
        on ? 'VLAN ' + p.v : '同じネットワーク'));
    });
    svg.querySelectorAll('rect[data-i]').forEach(rc => {
      rc.style.cursor = 'pointer';
      rc.addEventListener('click', () => {
        const i = +rc.dataset.i;
        const k = sel.indexOf(i);
        if (k >= 0) sel.splice(k, 1);
        else { if (sel.length >= 2) sel.shift(); sel.push(i); }
        drawVlan();
      });
    });
    const box = $('vlanBox'); box.innerHTML = ''; box.appendChild(svg);
    const n = $('vlanNote');
    if (sel.length < 2) {
      n.className = 'note info';
      n.textContent = '2台をタップして選ぶと、通信できるかどうかがわかります。';
    } else {
      const [a, b] = sel;
      const ok = !on || PCS[a].v === PCS[b].v;
      n.className = 'note ' + (ok ? 'ok' : 'ng');
      n.innerHTML = PCS[a].n + ' と ' + PCS[b].n + ' は <strong>' + (ok ? '通信できます' : '通信できません') + '</strong>。' +
        (!on ? 'VLANを無効にすると、同じスイッチにつながる機器はすべて同じネットワークになるからです。'
             : (ok ? '同じ VLAN ' + PCS[a].v + ' に属しているためです。'
                   : '別のVLAN（' + PCS[a].v + ' と ' + PCS[b].v + '）に分けられているため、物理的には同じスイッチでも届きません。' +
                     '<strong>これがVLANによるセキュリティ向上です。</strong>'));
    }
  }

  /* ---------- STEP4 クイズ ---------- */
  const QUIZ = [
    { t: 'リストに「カテゴリ：情報、サイト：A・C」を設定した。ホワイトリスト方式のとき、数学カテゴリのWebサイトAの閲覧結果はどれか。',
      choices: ['○（アクセスできる）', '×（アクセスできない）'], a: '○（アクセスできる）',
      why: 'ホワイトリスト方式は<strong>リストに載っているものだけ許可</strong>。サイトAはリストに載っているので○です。' },
    { t: '同じリストで、ブラックリスト方式のときのWebサイトAの閲覧結果はどれか。',
      choices: ['×（アクセスできない）', '○（アクセスできる）'], a: '×（アクセスできない）',
      why: 'ブラックリスト方式は<strong>リストに載っているものだけ禁止</strong>。サイトAは載っているので×です。同じリストでも結果は正反対になります。' },
    { t: 'ファイアウォールの説明として最も適当なものはどれか。',
      choices: ['外部ネットワークとの通信を制御し、不正な侵入や攻撃を防ぐ',
                'ネットワーク内のすべてのデータを暗号化する',
                '通信速度を最適化する', '通信障害を自動的に検出し修復する'],
      a: '外部ネットワークとの通信を制御し、不正な侵入や攻撃を防ぐ',
      why: '暗号化はSSL/TLSなどの役割で、ファイアウォールの仕事ではありません。' },
    { t: 'VLANの説明として最も適当なものはどれか。',
      choices: ['同一ネットワーク内でも「教員用」「生徒用」のように論理的に分割する技術',
                '異なるネットワークセグメント間で通信を可能にする技術',
                'トラフィックは分離できるがセキュリティ向上にはつながらない',
                '特定のポート番号の通信だけを遮断する技術'],
      a: '同一ネットワーク内でも「教員用」「生徒用」のように論理的に分割する技術',
      why: '分けることで不要な通信が届かなくなるので、<strong>セキュリティの向上につながります</strong>。異なるネットワークをつなぐのはルータの役割です。' },
    { t: 'ホワイトリスト方式の特徴として正しいものはどれか。',
      choices: ['安全性は高いが、許可するものを1つずつ登録する手間がかかる',
                '手軽だが、新しい危険なサイトには対応できない',
                'すべてのサイトにアクセスできる', 'リストがなくても機能する'],
      a: '安全性は高いが、許可するものを1つずつ登録する手間がかかる',
      why: '2つ目はブラックリスト方式の特徴です。学校では安全性を優先してホワイトリスト方式が使われることもあります。' }
  ];
  let qList = [], qi = 0, qScore = 0;
  function startQuiz() { qList = shuffle(QUIZ); qi = 0; qScore = 0; renderQ(); }
  function renderQ() {
    if (qi >= qList.length) {
      $('qText').textContent = qScore + ' / ' + qList.length + ' 問正解';
      $('qChoices').innerHTML = ''; $('qFb').hidden = true; $('qNext').disabled = true;
      $('qProgress').textContent = qList.length + ' / ' + qList.length; return;
    }
    const it = qList[qi];
    $('qProgress').textContent = (qi + 1) + ' / ' + qList.length;
    $('qScore').textContent = qScore;
    $('qText').textContent = it.t;
    const box = $('qChoices'); box.className = 'choice4'; box.innerHTML = '';
    shuffle(it.choices).forEach(c => {
      const b = document.createElement('button');
      b.className = 'btn'; b.textContent = c; b.dataset.c = c;
      b.addEventListener('click', () => answerQ(c));
      box.appendChild(b);
    });
    $('qFb').hidden = true; $('qNext').disabled = true;
    $('qNext').textContent = (qi === qList.length - 1) ? '結果を見る' : '次の問題';
  }
  function answerQ(c) {
    const it = qList[qi], ok = c === it.a, box = $('qChoices');
    box.classList.add('locked');
    [...box.children].forEach(b => {
      if (b.dataset.c === it.a) b.classList.add('correct');
      else if (b.dataset.c === c) b.classList.add('wrong');
    });
    if (ok) qScore++;
    const fb = $('qFb');
    fb.className = 'note ' + (ok ? 'ok' : 'ng');
    fb.innerHTML = (ok ? '正解。' : '正解は「<strong>' + it.a + '</strong>」。') + it.why;
    fb.hidden = false;
    $('qScore').textContent = qScore; $('qNext').disabled = false;
  }

  /* 本文の問題 */
  function drawBook() {
    if (!document.getElementById('bookBox')) return;
    window.Quiz.choice('bookBox', 'bookNote', [{"k": "ア", "q": "リスト（カテゴリ：情報／サイト：A・C）のとき、ホワイトリスト方式での閲覧結果の組合せは。（A:数学 B:SNS C:ゲーム D:情報）", "ch": ["A○ B○ C× D×", "A× B○ C× D×", "A× B○ C× D○", "A○ B× C○ D○"], "a": 3, "why": "ホワイトリストは<strong>「載っているものだけ許可」</strong>。サイトAとCはリストにあるので○、カテゴリ「情報」のDも○。載っていないBだけ×です。"}, {"k": "イ", "q": "同じリストで、ブラックリスト方式での閲覧結果の組合せは。", "ch": ["A○ B○ C× D×", "A× B○ C× D×", "A× B○ C× D○", "A○ B× C○ D○"], "a": 1, "why": "ブラックリストは<strong>「載っているものだけ禁止」</strong>。A・C・（カテゴリ情報の）Dが×で、載っていないBだけ○です。STEP 1 で切りかえて確かめられます。"}, {"k": "ウ", "q": "ファイアウォールに関する記述として最も適当なものは。", "ch": ["ネットワーク内のすべてのデータを改ざんや盗聴されないように暗号化する", "内部ネットワークの利用状況をクラウド上で可視化し、通信速度を最適化する", "外部ネットワークとの通信を制御し、不正な侵入や攻撃を防ぐ", "ネットワーク機器の通信障害を自動的に検出し、修復する"], "a": 2, "why": "内と外の境目に置いて、通してよい通信だけを通す「関所」です。暗号化はSSL/TLSの役割で、別のものです。"}, {"k": "エ", "q": "VLANに関する記述として最も適当なものは。", "ch": ["異なるネットワークセグメント間で通信が可能になる", "ネットワークのトラフィックを分離できるが、セキュリティ向上にはつながらない", "同一ネットワーク内であっても「教員用」と「生徒用」のように論理的にネットワークを分割する技術である", "スイッチングハブで、特定のポート番号の通信だけを遮断する技術である"], "a": 2, "why": "配線はそのままで<strong>論理的に</strong>分ける技術です。分けることで見えなくなるので、セキュリティの向上にもつながります。STEP 3 で確かめられます。"}], "本文の答えは【ア】③　【イ】①　【ウ】②　【エ】② です。");
  }

  function init() {
    ['mWhite', 'mBlack', 'mBoth'].forEach((id, i) => $(id).addEventListener('click', () => {
      fmode = ['white', 'black', 'both'][i]; drawFilter();
    }));
    $('sendPkt').addEventListener('click', () => sendPkt(1));
    $('send10').addEventListener('click', () => sendPkt(10));
    $('clearFw').addEventListener('click', () => { fwLog = []; sendPkt(0); });
    $('vlanOn').addEventListener('change', drawVlan);
    $('clearSel').addEventListener('click', () => { sel = []; drawVlan(); });
    $('qNext').addEventListener('click', () => { qi++; renderQ(); });
    $('qReset').addEventListener('click', startQuiz);
    window.Terms.glossary($('glossBox'), ['コンテンツフィルタリング', 'ファイアウォール', 'VLAN', 'ルータ', 'スイッチングハブ', 'SSL/TLS', 'LAN']);
    drawFilter(); drawRules(); sendPkt(6); drawVlan(); startQuiz();
    drawBook();
    window.Terms.attach();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
