// static/js/cart_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["counter"]

  async addToCart(event) {
    const productId = event.currentTarget.dataset.productId
    const response = await fetch('/cart/update/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getCookie('csrftoken')
      },
      body: JSON.stringify({
        product_id: productId,
        action: 'add'
      })
    });
    
    const data = await response.json()
    this.counterTarget.textContent = data.item_count
  }

  getCookie(name) {
    // Cookie retrieval logic
  }
}