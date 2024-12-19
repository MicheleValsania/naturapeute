/**
 * Extend Trix-editor
 */
document.addEventListener('trix-initialize', (e) => {
  const blockTools = e.target.toolbarElement.querySelector('[data-trix-button-group=block-tools]')
  ;['H3', 'H2', 'H1'].forEach(t => {
    Trix.config.blockAttributes[t] = { tagName: t, terminal: true, breakOnReturn: true, group: false }
    blockTools.insertAdjacentHTML('afterbegin', `<button type="button" class="trix-button" data-trix-attribute="${t}" title="${t}" tabindex="-1">${t}</button>`)
  })
  Trix.config.blockAttributes['html'] = { tagName: "html", terminal: true, breakOnReturn: true, group: false }
  blockTools.insertAdjacentHTML('afterbegin', `<button type="button" class="trix-button" data-trix-attribute="html" title="Convert to HTML" tabindex="-1">HTML</button>`)
})
