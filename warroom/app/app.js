/* War Room shell: loads the generated brain, renders the panels, wires nav. */
(function () {
  'use strict';

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var G = null, S = null, view = null;

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  /* Extracted cells keep their inline markdown so nothing is flattened on the
     way out of the source documents. Render just the marks that occur. */
  function md(s) {
    return esc(s)
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/~~([^~]+)~~/g, '<s>$1</s>');
  }

  function prov(src, extra) {
    if (!src) return '';
    var age = src.ageDays == null ? '?'
      : (src.ageDays === 0 ? 'today' : src.ageDays + 'd old');
    return src.doc + ' · ' + age + (extra ? ' · ' + extra : '');
  }

  function row(n, title, detail, tagHtml) {
    return '<div class="row"><div class="n">' + esc(n) + '</div><div>' +
      '<div class="t">' + (tagHtml || '') + md(title) + '</div>' +
      (detail ? '<div class="d">' + md(detail) + '</div>' : '') +
      '</div></div>';
  }

  var CLASS_TAG = {
    'OWNER DECISION': 'owner', 'CONTENT': 'content',
    'OPERATIONAL': 'op', 'LEGAL REVIEW': 'legal'
  };

  /* ---------- command ---------- */

  var classFilter = null;

  function renderTiles() {
    var b = S.panels.blockers, cat = S.panels.catalog.items;
    function look(re) {
      var hit = cat.filter(function (k) { return re.test(k.k); })[0];
      return hit ? hit.v.replace(/[`*]/g, '') : '—';
    }
    var tiles = [
      ['is-bad', b.total, 'blockers'],
      ['is-owner', b.byClass['OWNER DECISION'] || 0, 'owner decisions'],
      ['is-warn', S.panels.issues.items.length, 'open issues'],
      ['is-ok', G.stats.docs, 'documents'],
      ['', G.stats.edges, 'graph edges'],
      ['is-warn', G.stats.orphans, 'orphan docs'],
      ['is-bad', look(/^Orders/i), 'orders, all time'],
      ['', look(/^Active products/i).split(' ')[0], 'active products']
    ];
    $('#tiles').innerHTML = tiles.map(function (t) {
      return '<div class="tile ' + t[0] + '"><b>' + esc(t[1]) + '</b><span>' +
        esc(t[2]) + '</span></div>';
    }).join('');
  }

  function renderBlockers() {
    var b = S.panels.blockers;
    var classes = Object.keys(b.byClass).filter(function (c) { return b.byClass[c]; });
    $('#classFilter').innerHTML = ['ALL'].concat(classes).map(function (c) {
      var on = (classFilter === null && c === 'ALL') || classFilter === c;
      var n = c === 'ALL' ? b.total : b.byClass[c];
      return '<button class="chip" data-class="' + esc(c) + '" aria-pressed="' + on +
        '">' + esc(c) + ' <em style="font-style:normal;opacity:.6">' + n + '</em></button>';
    }).join('');

    var items = b.items.filter(function (i) { return !classFilter || i.class === classFilter; });
    $('#blockers').innerHTML = items.map(function (i) {
      var tag = '<span class="tag ' + (CLASS_TAG[i.class] || 'op') + '">' +
        esc(i.classRaw) + '</span>';
      return row(i.id, i.title, i.detail, tag);
    }).join('') || '<p class="sub">Nothing in this class.</p>';

    $('#blockSrc').textContent = prov(b.source, 'not authoritative');
  }

  function renderCommand() {
    $('#stateWarn').textContent = S.warning;
    renderTiles();
    renderBlockers();

    $('#issues').innerHTML = S.panels.issues.items.map(function (i) {
      return row(i.id, i.issue, i.state);
    }).join('');
    $('#issueSrc').textContent = prov(S.panels.issues.source);

    $('#ownerBlocked').innerHTML = S.panels.ownerBlocked.items.map(function (i) {
      return row(i.id, i.item, i.action || i.why);
    }).join('');
    $('#ownerSrc').textContent = prov(S.panels.ownerBlocked.source);
  }

  /* ---------- graph ---------- */

  function inspect(n) {
    var box = $('#inspect');
    if (!n) { box.hidden = true; return; }
    var ins = G.edges.filter(function (e) { return e.t === n.id; })
      .map(function (e) { return e.s; });
    var outs = G.edges.filter(function (e) { return e.s === n.id; })
      .map(function (e) { return e.t; });

    function list(arr) {
      if (!arr.length) return '<ul><li style="cursor:default;opacity:.5">none</li></ul>';
      return '<ul>' + arr.slice(0, 14).map(function (id) {
        return '<li data-goto-node="' + esc(id) + '">' +
          esc(id.split('/').pop()) + '</li>';
      }).join('') + '</ul>';
    }

    box.innerHTML =
      '<button class="x" aria-label="Close">×</button>' +
      '<h3>' + esc(n.title) + '</h3>' +
      '<div class="path">' + esc(n.id) + '</div>' +
      '<div class="metaline"><span>in ' + n.inDeg + '</span><span>out ' + n.outDeg +
      '</span><span>' + n.words.toLocaleString() + 'w</span><span>' +
      esc((n.updated || '').slice(0, 10)) + '</span></div>' +
      (n.excerpt ? '<p class="ex">' + esc(n.excerpt) + '…</p>' : '') +
      '<h4>Referenced by (' + ins.length + ')</h4>' + list(ins) +
      '<h4>References (' + outs.length + ')</h4>' + list(outs);
    box.hidden = false;
  }

  function renderGraph() {
    $('#graphMeta').textContent =
      G.stats.docs + ' documents · ' + G.stats.edges + ' references · ' +
      G.stats.clusters + ' clusters · ' + G.stats.orphans + ' orphans · ' +
      G.stats.words.toLocaleString() + ' words';

    $('#legend').innerHTML = G.clusters.map(function (c) {
      return '<i><b style="background:' + GraphView.colorFor(c.id) + '"></b>' +
        esc(c.id) + ' ' + c.count + '</i>';
    }).join('');

    view = new GraphView($('#canvas'), G, { onSelect: inspect });
    view.start();

    $('#gSearch').addEventListener('input', function () { view.setQuery(this.value); });
    $('#gReset').addEventListener('click', function () {
      $('#gSearch').value = ''; view.setQuery(''); view.selected = null;
      inspect(null); view.reset();
    });
    $('#inspect').addEventListener('click', function (ev) {
      if (ev.target.classList.contains('x')) { view.selected = null; inspect(null); return; }
      var id = ev.target.getAttribute('data-goto-node');
      if (id) view.focus(id);
    });
  }

  /* ---------- documents ---------- */

  function renderDocs() {
    var q = $('#dSearch').value.trim().toLowerCase();
    var orphansOnly = $('#dOrphans').checked;
    var orphanSet = {};
    G.orphans.forEach(function (o) { orphanSet[o] = 1; });

    var list = G.nodes.filter(function (n) {
      if (orphansOnly && !orphanSet[n.id]) return false;
      if (!q) return true;
      var hay = n.title + ' ' + n.id + ' ' + n.tags.join(' ') + ' ' +
        n.headings.map(function (h) { return h.text; }).join(' ');
      return hay.toLowerCase().indexOf(q) !== -1;
    }).sort(function (a, b) { return b.inDeg - a.inDeg || a.id.localeCompare(b.id); });

    $('#dCount').textContent = list.length + ' of ' + G.nodes.length + ' documents';
    $('#docList').innerHTML = list.map(function (n) {
      return '<article class="doc' + (orphanSet[n.id] ? ' orphan' : '') +
        '" data-open="' + esc(n.id) + '">' +
        '<h3>' + esc(n.title) + '</h3>' +
        '<div class="path">' + esc(n.id) + '</div>' +
        (n.excerpt ? '<p class="ex">' + esc(n.excerpt) + '</p>' : '') +
        '<div class="metaline"><span style="color:' + GraphView.colorFor(n.cluster) +
        '">' + esc(n.cluster) + '</span><span>in ' + n.inDeg + '</span><span>out ' +
        n.outDeg + '</span><span>' + n.words.toLocaleString() + 'w</span></div>' +
        '</article>';
    }).join('') || '<p class="sub">No documents match.</p>';
  }

  function renderDangling() {
    $('#dangling').innerHTML = G.unresolved.length
      ? G.unresolved.map(function (u, i) {
          return row(i + 1, '`' + u.ref + '`',
            'named ' + u.n + '× but no such document exists');
        }).join('')
      : '<p class="sub">Every reference resolves.</p>';
  }

  /* ---------- safety ---------- */

  function renderSafety() {
    var t = S.panels.themes;
    $('#themeSrc').textContent = prov(t.source, 'DO NOT TRUST');
    $('#themeNote').innerHTML = md(t.note);
    $('#themes').innerHTML = t.items.map(function (x, i) {
      var tag = '<span class="tag ' + (x.isMain ? 'main' : 'unpub') + '">' +
        esc(x.role) + '</span>';
      return row(i + 1, '`' + x.id + '`', x.name, tag);
    }).join('');

    $('#safeSrc').textContent = prov(S.panels.safety.source);
    $('#steps').innerHTML = S.panels.safety.steps.map(function (s) {
      return '<li>' + md(s.text) + '</li>';
    }).join('');

    $('#catSrc').textContent = prov(S.panels.catalog.source);
    $('#catalog').innerHTML = S.panels.catalog.items.map(function (k, i) {
      return row(i + 1, k.k, k.v);
    }).join('');
  }

  /* ---------- nav ---------- */

  function goto(name) {
    document.documentElement.setAttribute('data-view', name);
    [].forEach.call(document.querySelectorAll('.view'), function (v) {
      v.hidden = v.getAttribute('data-view') !== name;
    });
    [].forEach.call(document.querySelectorAll('.nav'), function (b) {
      b.setAttribute('aria-current', String(b.getAttribute('data-goto') === name));
    });
    if (name === 'graph' && view) view._resize();
    location.hash = name;
  }

  function wire() {
    document.addEventListener('click', function (ev) {
      var nav = ev.target.closest('.nav');
      if (nav) return goto(nav.getAttribute('data-goto'));

      var chip = ev.target.closest('.chip');
      if (chip) {
        var c = chip.getAttribute('data-class');
        classFilter = (c === 'ALL' || classFilter === c) ? null : c;
        return renderBlockers();
      }

      var doc = ev.target.closest('.doc');
      if (doc) { goto('graph'); view.focus(doc.getAttribute('data-open')); }
    });
    $('#dSearch').addEventListener('input', renderDocs);
    $('#dOrphans').addEventListener('change', renderDocs);
  }

  /* ---------- boot ---------- */

  Promise.all([
    fetch('data/graph.json').then(function (r) { return r.json(); }),
    fetch('data/state.json').then(function (r) { return r.json(); })
  ]).then(function (res) {
    G = res[0]; S = res[1];

    $('#railStamp').textContent = G.generated.replace('T', ' ').replace('+00:00', 'Z');
    $('#cBlockers').textContent = S.panels.blockers.total;
    $('#cDocs').textContent = G.stats.docs;
    $('#cOrphans').textContent = G.stats.orphans;
    $('#cSteps').textContent = S.panels.safety.steps.length;

    renderCommand();
    renderGraph();
    renderDocs();
    renderDangling();
    renderSafety();
    wire();

    $('#boot').hidden = true;
    $('#shell').hidden = false;
    goto((location.hash || '#command').slice(1));
  }).catch(function (e) {
    $('#boot').textContent =
      'Failed to load the brain: ' + e.message +
      ' — run: python3 warroom/graphify.py && python3 warroom/extract_state.py';
  });
})();
