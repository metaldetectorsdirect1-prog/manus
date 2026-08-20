/* HIVOLT — size guide behaviour (T2)
 *
 * The dialog element does the accessibility work: showModal() traps focus,
 * makes the rest of the page inert, and closes on Escape. This file only
 * connects triggers to dialogs, restores focus on close, and flips the unit.
 *
 * If the browser has no dialog support the trigger is hidden rather than left
 * as a button that does nothing.
 */
(function () {
  'use strict';

  var SUPPORTS_DIALOG =
    typeof window.HTMLDialogElement === 'function' &&
    typeof window.HTMLDialogElement.prototype.showModal === 'function';

  var lastTrigger = null;

  function openGuide(trigger) {
    var dialog = document.getElementById(trigger.getAttribute('data-hv-sg-open'));
    if (!dialog) return;
    lastTrigger = trigger;
    dialog.showModal();
  }

  function closeGuide(dialog) {
    if (dialog.open) dialog.close();
  }

  function setUnit(dialog, unit) {
    dialog.setAttribute('data-active-unit', unit);
  }

  function hideUnsupportedTriggers() {
    var triggers = document.querySelectorAll('[data-hv-sg-open]');
    for (var i = 0; i < triggers.length; i++) {
      triggers[i].hidden = true;
    }
  }

  function onClick(event) {
    var trigger = event.target.closest('[data-hv-sg-open]');
    if (trigger) {
      event.preventDefault();
      openGuide(trigger);
      return;
    }

    var closer = event.target.closest('[data-hv-sg-close]');
    if (closer) {
      event.preventDefault();
      var owner = closer.closest('dialog');
      if (owner) closeGuide(owner);
      return;
    }

    // Clicking the backdrop lands on the dialog element itself, never on the
    // panel inside it.
    if (event.target.matches('dialog.hv-sg')) {
      closeGuide(event.target);
    }
  }

  function onChange(event) {
    var input = event.target.closest('[data-hv-sg-unit]');
    if (!input) return;
    var dialog = input.closest('dialog.hv-sg');
    if (dialog) setUnit(dialog, input.value);
  }

  function onClose(event) {
    if (!event.target.matches || !event.target.matches('dialog.hv-sg')) return;
    if (lastTrigger && document.contains(lastTrigger)) {
      lastTrigger.focus();
    }
    lastTrigger = null;
  }

  function init() {
    if (!SUPPORTS_DIALOG) {
      hideUnsupportedTriggers();
      return;
    }
    document.addEventListener('click', onClick);
    document.addEventListener('change', onChange);
    // `close` does not bubble, so it is captured instead.
    document.addEventListener('close', onClose, true);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Sections re-render in the theme editor; re-hiding is all that is needed
  // because the listeners are delegated from document.
  document.addEventListener('shopify:section:load', function () {
    if (!SUPPORTS_DIALOG) hideUnsupportedTriggers();
  });
})();
