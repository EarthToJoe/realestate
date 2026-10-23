// The presenter's notes and spotlights (decision 50): only loaded with "I'm presenting" on. The notes drawer starts
// closed; opening it narrows the content column on a laptop and is a bottom sheet on a phone. Whether it is open
// is remembered on this device ("notes-open" in localStorage).
(function () {
  var notes = document.getElementById('presenter-notes');
  if (!notes) return;
  var KEY = 'notes-open';

  function open() { notes.hidden = false; document.body.classList.add('notes-open'); try { localStorage.setItem(KEY, '1'); } catch (e) {} }
  function close() { notes.hidden = true; document.body.classList.remove('notes-open'); try { localStorage.removeItem(KEY); } catch (e) {} }
  document.querySelectorAll('[data-notes-toggle]').forEach(function (b) {
    b.addEventListener('click', function () {
      var menu = document.getElementById('menu'); if (menu) menu.open = false;
      notes.hidden ? open() : close();
    });
  });
  document.querySelectorAll('[data-notes-close]').forEach(function (b) { b.addEventListener('click', close); });
  var wasOpen = false; try { wasOpen = localStorage.getItem(KEY) === '1'; } catch (e) {}
  if (wasOpen && window.matchMedia('(min-width: 761px)').matches) open();  // a phone always starts closed

  // Spotlight: Driver.js over this screen's elements (steps.yaml `spotlight`), skipping any not on the page now.
  var starts = document.querySelectorAll('[data-spotlight-start]');
  if (!window.driver) return;
  starts.forEach(function (start) {
    start.addEventListener('click', function () {
      var menu = document.getElementById('menu'); if (menu) menu.open = false;
      var list = []; try { list = JSON.parse(notes.dataset.spotlight || '[]'); } catch (e) {}
      var steps = list.filter(function (s) {
        var el = document.querySelector(s.el);
        if (!el) return false;
        for (var f = el.closest('details'); f; f = f.parentElement && f.parentElement.closest('details')) f.open = true;
        return el.getClientRects().length > 0;
      }).map(function (s) { return { element: s.el, popover: { description: s.text } }; });
      if (!steps.length) return;
      var wasNotes = !notes.hidden; close();
      var d = window.driver.js.driver({ showProgress: steps.length > 1, animate: true, steps: steps,
        nextBtnText: 'Next', prevBtnText: 'Back', doneBtnText: 'Done',
        onDestroyed: function () { if (wasNotes) open(); } });
      d.drive();
    });
  });
})();
