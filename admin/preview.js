/* Live preview for the Decap editor: shows the page as it will look while you type. */
(function () {
  if (!window.CMS) return;
  var h = window.h;
  CMS.registerPreviewStyle('/style.css');
  CMS.registerPreviewStyle('/admin/preview.css');
  function arr(v) { return v && v.toJS ? v.toJS() : (v || []); }
  function asset(props, p) { if (!p) return ''; try { var a = props.getAsset(p); return a ? a.toString() : p; } catch (e) { return p; } }

  var Project = createClass({
    render: function () {
      var props = this.props, d = props.entry.get('data');
      var g = function (k) { return d.get(k); };
      var hero = g('hero'); hero = hero && hero.toJS ? hero.toJS() : (hero || {});
      var heroEl = hero.video
        ? h('video', { src: asset(props, hero.video), poster: asset(props, hero.poster), autoPlay: true, muted: true, loop: true, playsInline: true, className: 'pv-hero' })
        : h('img', { src: asset(props, hero.image || (hero.slides && hero.slides[0]) || ''), className: 'pv-hero' });
      var bricks = arr(g('bricks'));
      var sections = arr(g('sections')).map(function (s, i) {
        var stats = (s.stats || []).filter(function (x) { return x.figure; });
        return h('div', { className: 'pv-sec', key: i },
          h('h3', {}, ('0' + (i + 1)).slice(-2) + '  ' + (s.type || '')),
          stats.length ? h('div', { className: 'stats' }, stats.map(function (x, j) { return h('div', { key: j }, h('b', {}, x.figure), h('span', {}, x.label)); })) : null,
          h('p', { className: 'lede' }, s.text || ''),
          (s.deck || []).length ? h('div', { className: 'pv-deck' }, s.deck.map(function (x, j) { return h('img', { key: j, src: asset(props, x.image) }); })) : null,
          h('div', { className: 'pv-gal' },
            (s.videos || []).map(function (v, j) { return h('figure', { key: 'v' + j }, h('div', { className: 'pv-t' }, v.poster ? h('img', { src: asset(props, v.poster) }) : h('video', { src: asset(props, v.video), muted: true })), h('figcaption', {}, '▶ ' + (v.caption || ''))); }),
            (s.images || []).map(function (x, j) { return h('figure', { key: j }, h('div', { className: 'pv-t' + (x.cutout ? ' c' : '') }, h('img', { src: asset(props, x.image) })), h('figcaption', {}, x.caption || '')); })
          ));
      });
      var labels = arr(g('labels'));
      return h('div', { className: 'pv', style: { background: g('background') || '#fff', color: g('text_colour') || '#0b0b0b' } },
        h('div', { className: 'pv-top' }, heroEl, h('div', { className: 'pv-title' }, h('h1', {}, g('name') || 'Project name'), h('div', {}, [g('kind'), g('city'), g('years')].filter(Boolean).join(' · ')))),
        h('div', { className: 'pv-body' },
          h('p', { className: 'pv-intro' }, g('intro') || ''),
          g('credit') ? h('p', { className: 'pv-credit' }, g('credit')) : null,
          h('dl', { className: 'pv-meta' }, h('dt', {}, 'Role'), h('dd', {}, g('role') || '')),
          bricks.length ? h('div', { className: 'pv-block' }, h('div', { className: 'lbl' }, g('bricks_heading') || 'Story'), bricks.map(function (b, j) { return h('div', { className: 'pv-step', key: j }, h('img', { src: asset(props, b.image) }), h('p', {}, b.text)); })) : null,
          labels.length ? h('div', { className: 'pv-block' }, h('div', { className: 'lbl' }, labels.length + ' labels'), h('div', { className: 'pv-labs' }, labels.map(function (l, j) { return h('img', { key: j, src: asset(props, l.image), title: l.name }); }))) : null,
          h('div', { className: 'lbl', style: { marginTop: '40px' } }, 'What I did'),
          sections));
    }
  });
  CMS.registerPreviewTemplate('projects', Project);

  var Home = createClass({
    render: function () {
      var d = this.props.entry.get('data'), g = function (k) { return d.get(k); };
      return h('div', { className: 'pv', style: { background: '#fff', color: '#0b0b0b' } },
        h('div', { className: 'pv-body' },
          h('h1', { className: 'pv-big' }, g('name')),
          h('p', { className: 'pv-intro' }, g('intro')),
          h('div', { className: 'lbl', style: { marginTop: '40px' } }, 'In numbers'),
          h('div', { className: 'stats' }, arr(g('numbers')).map(function (n, i) { return h('div', { key: i }, h('b', {}, n.figure), h('span', {}, n.label)); })),
          h('div', { className: 'lbl', style: { marginTop: '40px' } }, 'About'),
          h('h3', {}, g('about_heading')),
          arr(g('about')).map(function (p, i) { return h('p', { key: i }, p); }),
          h('div', { className: 'lbl', style: { marginTop: '40px' } }, 'Contact'),
          h('h2', { className: 'pv-big' }, g('contact_heading')),
          h('p', {}, g('contact_text')), h('p', {}, g('email'))));
    }
  });
  CMS.registerPreviewTemplate('home', Home);
})();
