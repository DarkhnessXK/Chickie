export class ButtonHandler {
  private element: HTMLButtonElement
  private initialText: string

  constructor (event?: Event, id?: string) {
    if (event) {
      this.element = event.target as HTMLButtonElement
    } else if (id) {
      this.element = document.getElementById(id) as HTMLButtonElement
    } else {
      throw new Error('Nenhum parametro passado')
    }
    this.initialText = this.element.innerHTML
  }

  disable(text: string) {
    this.element.disabled = true
    this.element.innerHTML = text
  }

  enable() {
    this.element.disabled = false
    this.element.innerHTML = this.initialText
  }
}
