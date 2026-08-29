/* Force-directed document graph on a plain canvas. No dependencies.
   152 nodes is small enough that naive O(n^2) repulsion runs comfortably at
   60fps, so there is no quadtree here — the simplicity is worth more. */
(function (global) {
  'use strict';

  var PALETTE = {
    'docs': '#4da3ff', 'audit': '#f0b429', 'impulse-rebuild': '#3ecf8e',
    '<root>': '#ff5c5c', 'site': '#c77dff', 'qa': '#ff9f6b',
    'HIVOLT-deliverables': '#5ad4e6', 'tooling': '#8792a6'
  };
  var FALLBACK = '#8792a6';

  function colorFor(cluster) { return PALETTE[cluster] || FALLBACK; }

  function GraphView(canvas, graph, opts) {
    this.cv = canvas;
    this.ctx = canvas.getContext('2d');
    this.opts = opts || {};
    this.tx = 0; this.ty = 0; this.scale = 1;
    this.hover = null; this.selected = null; this.dragNode = null;
    this.panning = false; this.query = '';
    this.setData(graph);
    this._bind();
    this._resize();
  }

  GraphView.prototype.setData = function (graph) {
    var byId = {};
    // Deterministic seeded spiral start beats Math.random(): the same corpus
    // always lays out the same way, so the picture is comparable run to run.
    this.nodes = graph.nodes.map(function (n, i) {
      var a = i * 2.399963, r = 9 * Math.sqrt(i + 1);
      var node = {
        id: n.id, title: n.title, cluster: n.cluster, tags: n.tags,
        inDeg: n.inDeg, outDeg: n.outDeg, words: n.words,
        excerpt: n.excerpt, headings: n.headings, updated: n.updated,
        x: Math.cos(a) * r, y: Math.sin(a) * r, vx: 0, vy: 0,
        r: 3.4 + Math.min(9, Math.sqrt(n.inDeg) * 2.6)
      };
      byId[n.id] = node;
      return node;
    });
    this.byId = byId;
    this.edges = graph.edges.map(function (e) {
      return { s: byId[e.s], t: byId[e.t], n: e.n };
    }).filter(function (e) { return e.s && e.t; });

    var adj = {};
    this.edges.forEach(function (e) {
      (adj[e.s.id] = adj[e.s.id] || []).push(e.t.id);
      (adj[e.t.id] = adj[e.t.id] || []).push(e.s.id);
    });
    this.adj = adj;

    // Give each cluster an anchor on a ring. Without this the layout spreads
    // into an even haze and the clusters that actually exist stop being visible.
    var counts = {};
    this.nodes.forEach(function (n) { counts[n.cluster] = (counts[n.cluster] || 0) + 1; });
    var names = Object.keys(counts).sort(function (a, b) { return counts[b] - counts[a]; });
    var anchors = {};
    names.forEach(function (name, i) {
      var a = (i / names.length) * 6.2832 - 1.5708;
      var r = names.length > 1 ? 190 : 0;
      anchors[name] = { x: Math.cos(a) * r, y: Math.sin(a) * r * 0.72 };
    });
    this.anchors = anchors;
    this.nodes.forEach(function (n) { n.a = anchors[n.cluster]; });

    this._labelOrder = this.nodes.slice().sort(function (a, b) {
      return b.inDeg - a.inDeg || b.words - a.words;
    });

    this.alpha = 1;
    this.fitted = false;
  };

  GraphView.prototype._bind = function () {
    var self = this, cv = this.cv;

    window.addEventListener('resize', function () { self._resize(); });

    cv.addEventListener('mousedown', function (ev) {
      var p = self._world(ev), n = self._hit(p);
      if (n) { self.dragNode = n; n.fx = n.x; n.fy = n.y; }
      else { self.panning = true; cv.classList.add('drag'); }
      self.px = ev.clientX; self.py = ev.clientY;
      self.alpha = Math.max(self.alpha, 0.35);
    });

    window.addEventListener('mousemove', function (ev) {
      if (self.dragNode) {
        var p = self._world(ev);
        self.dragNode.fx = p.x; self.dragNode.fy = p.y;
        self.alpha = Math.max(self.alpha, 0.35);
      } else if (self.panning) {
        self.tx += ev.clientX - self.px; self.ty += ev.clientY - self.py;
        self.px = ev.clientX; self.py = ev.clientY;
      } else if (ev.target === cv) {
        var h = self._hit(self._world(ev));
        if (h !== self.hover) { self.hover = h; cv.style.cursor = h ? 'pointer' : 'grab'; }
      }
    });

    window.addEventListener('mouseup', function () {
      if (self.dragNode) { delete self.dragNode.fx; delete self.dragNode.fy; self.dragNode = null; }
      self.panning = false; cv.classList.remove('drag');
    });

    cv.addEventListener('click', function (ev) {
      var n = self._hit(self._world(ev));
      self.selected = n;
      if (self.opts.onSelect) self.opts.onSelect(n);
    });

    cv.addEventListener('wheel', function (ev) {
      ev.preventDefault();
      var rect = cv.getBoundingClientRect();
      var mx = ev.clientX - rect.left, my = ev.clientY - rect.top;
      var k = Math.exp(-ev.deltaY * 0.0016);
      var ns = Math.min(4, Math.max(0.25, self.scale * k));
      k = ns / self.scale;
      self.tx = mx - (mx - self.tx) * k;
      self.ty = my - (my - self.ty) * k;
      self.scale = ns;
    }, { passive: false });
  };

  GraphView.prototype._resize = function () {
    var dpr = window.devicePixelRatio || 1, r = this.cv.getBoundingClientRect();
    this.w = r.width; this.h = r.height;
    this.cv.width = Math.round(r.width * dpr);
    this.cv.height = Math.round(r.height * dpr);
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (!this._centred && this.w) { this.reset(); this._centred = true; }
  };

  GraphView.prototype.reset = function () {
    this.alpha = 1;
    this.fitted = false;
    this.fit();
  };

  /* Frame the whole layout with a margin, so nothing sits under the toolbar
     or bleeds off the edge regardless of how far the graph spread. */
  GraphView.prototype.fit = function () {
    if (!this.w || !this.nodes.length) return;
    var x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    this.nodes.forEach(function (n) {
      x0 = Math.min(x0, n.x - n.r); y0 = Math.min(y0, n.y - n.r);
      x1 = Math.max(x1, n.x + n.r); y1 = Math.max(y1, n.y + n.r);
    });
    if (!isFinite(x0) || !isFinite(x1) || !isFinite(y0) || !isFinite(y1)) return;
    var pad = 46;
    var k = Math.min((this.w - pad * 2) / (x1 - x0 || 1),
                     (this.h - pad * 2) / (y1 - y0 || 1));
    this.scale = Math.min(2, Math.max(0.3, k));
    this.tx = this.w / 2 - (x0 + x1) / 2 * this.scale;
    this.ty = this.h / 2 - (y0 + y1) / 2 * this.scale;
  };

  GraphView.prototype._world = function (ev) {
    var r = this.cv.getBoundingClientRect();
    return {
      x: (ev.clientX - r.left - this.tx) / this.scale,
      y: (ev.clientY - r.top - this.ty) / this.scale
    };
  };

  GraphView.prototype._hit = function (p) {
    for (var i = this.nodes.length - 1; i >= 0; i--) {
      var n = this.nodes[i], dx = n.x - p.x, dy = n.y - p.y;
      var rr = (n.r + 4 / this.scale);
      if (dx * dx + dy * dy <= rr * rr) return n;
    }
    return null;
  };

  GraphView.prototype.setQuery = function (q) {
    this.query = (q || '').trim().toLowerCase();
    this.alpha = Math.max(this.alpha, 0.25);
  };

  GraphView.prototype._matches = function (n) {
    if (!this.query) return true;
    return (n.title + ' ' + n.id + ' ' + n.cluster + ' ' + n.tags.join(' '))
      .toLowerCase().indexOf(this.query) !== -1;
  };

  GraphView.prototype.focus = function (id) {
    var n = this.byId[id];
    if (!n) return;
    this.selected = n;
    this.tx = this.w / 2 - n.x * this.scale;
    this.ty = this.h / 2 - n.y * this.scale;
    if (this.opts.onSelect) this.opts.onSelect(n);
  };

  GraphView.prototype._tick = function () {
    if (this.alpha < 0.004) {
      if (!this.fitted) { this.fitted = true; this.fit(); }
      return;
    }
    this.alpha *= 0.982;
    var nodes = this.nodes, i, j, n, m, dx, dy, d2, d, f;

    for (i = 0; i < nodes.length; i++) {
      n = nodes[i];
      for (j = i + 1; j < nodes.length; j++) {
        m = nodes[j];
        dx = m.x - n.x; dy = m.y - n.y;
        d2 = dx * dx + dy * dy;
        if (d2 > 90000) continue;              // ignore distant pairs
        // Floor the distance. Cluster anchors stack many nodes on one point,
        // and an unclamped 900/d^2 there diverges the whole layout to NaN.
        if (d2 < 36) { d2 = 36; if (!dx && !dy) { dx = (i % 7) - 3; dy = (j % 7) - 3; } }
        f = 900 / d2;
        d = Math.sqrt(dx * dx + dy * dy) || 1;
        dx = dx / d * f; dy = dy / d * f;
        n.vx -= dx; n.vy -= dy; m.vx += dx; m.vy += dy;
      }
    }

    for (i = 0; i < this.edges.length; i++) {
      var e = this.edges[i]; n = e.s; m = e.t;
      dx = m.x - n.x; dy = m.y - n.y;
      d = Math.sqrt(dx * dx + dy * dy) || 0.01;
      f = (d - 62) * 0.016;
      dx = dx / d * f; dy = dy / d * f;
      n.vx += dx; n.vy += dy; m.vx -= dx; m.vy -= dy;
    }

    for (i = 0; i < nodes.length; i++) {
      n = nodes[i];
      n.vx += (n.a.x - n.x) * 0.010;                // toward its cluster anchor
      n.vy += (n.a.y - n.y) * 0.010;
      n.vx -= n.x * 0.0025; n.vy -= n.y * 0.0025;   // gravity to centre
      if (n.fx !== undefined) { n.x = n.fx; n.y = n.fy; n.vx = n.vy = 0; continue; }
      n.vx *= 0.86; n.vy *= 0.86;
      var sp = Math.sqrt(n.vx * n.vx + n.vy * n.vy);
      if (sp > 30) { n.vx = n.vx / sp * 30; n.vy = n.vy / sp * 30; }
      n.x += n.vx * this.alpha * 3.2;
      n.y += n.vy * this.alpha * 3.2;
    }
  };

  GraphView.prototype._draw = function () {
    var c = this.ctx, self = this;
    c.clearRect(0, 0, this.w, this.h);
    c.save();
    c.translate(this.tx, this.ty);
    c.scale(this.scale, this.scale);

    var focus = this.hover || this.selected;
    var near = focus ? (this.adj[focus.id] || []).concat([focus.id]) : null;
    function lit(id) { return !near || near.indexOf(id) !== -1; }

    c.lineCap = 'round';
    this.edges.forEach(function (e) {
      var on = lit(e.s.id) && lit(e.t.id);
      var vis = self._matches(e.s) || self._matches(e.t);
      c.globalAlpha = on ? (vis ? 0.5 : 0.08) : 0.07;
      c.strokeStyle = on && near ? '#4da3ff' : '#3a465c';
      c.lineWidth = Math.min(2.4, 0.5 + e.n * 0.3) / self.scale;
      c.beginPath(); c.moveTo(e.s.x, e.s.y); c.lineTo(e.t.x, e.t.y); c.stroke();
    });

    this.nodes.forEach(function (n) {
      var vis = self._matches(n), on = lit(n.id);
      c.globalAlpha = vis ? (on ? 1 : 0.22) : 0.1;
      c.beginPath(); c.arc(n.x, n.y, n.r, 0, 6.284);
      c.fillStyle = colorFor(n.cluster); c.fill();
      if (n === self.selected) {
        c.globalAlpha = 1; c.lineWidth = 2 / self.scale;
        c.strokeStyle = '#fff'; c.stroke();
      }
    });

    // 152 labels at once is unreadable. Show hubs always, everything else only
    // once zoomed in, plus whatever neighbourhood is currently focused.
    var showAll = this.scale > 1.5;
    var px = 1 / this.scale;
    c.textAlign = 'center'; c.textBaseline = 'top';
    c.font = (10 * px).toFixed(2) + 'px ui-monospace,Menlo,monospace';

    // Most-referenced first, and drop any label that would overlap one already
    // placed — a label that cannot be read is worse than no label.
    var placed = [];
    this._labelOrder.forEach(function (n) {
      var focused = near && near.indexOf(n.id) !== -1;
      var searched = self.query && self._matches(n);
      if (!(showAll || n.inDeg >= 4 || focused || searched)) return;
      if (!self._matches(n)) return;
      if (near && !focused) return;

      var t = n.title.length > 30 ? n.title.slice(0, 28) + '…' : n.title;
      var w = c.measureText(t).width, h = 12 * px;
      var x0 = n.x - w / 2 - 3 * px, y0 = n.y + n.r + 2 * px;
      var x1 = x0 + w + 6 * px, y1 = y0 + h;

      for (var k = 0; k < placed.length; k++) {
        var r = placed[k];
        if (x0 < r[2] && x1 > r[0] && y0 < r[3] && y1 > r[1]) return;
      }
      placed.push([x0, y0, x1, y1]);

      c.globalAlpha = 0.72;
      c.fillStyle = '#0b0e13';
      c.fillRect(x0, y0, x1 - x0, h);
      c.globalAlpha = 1;
      c.fillStyle = focused ? '#e6ebf4' : '#aab6c9';
      c.fillText(t, n.x, y0 + px);
    });

    c.restore();
    c.globalAlpha = 1;
  };

  GraphView.prototype.start = function () {
    var self = this;
    (function loop() { self._tick(); self._draw(); requestAnimationFrame(loop); })();
  };

  GraphView.colorFor = colorFor;
  global.GraphView = GraphView;
})(window);
