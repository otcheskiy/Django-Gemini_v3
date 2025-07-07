document.addEventListener('DOMContentLoaded', function() {
    // Обработчики для кнопок увеличения/уменьшения количества
    document.querySelectorAll('.cart-quantity-btn').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            const action = this.dataset.action; // 'increase' или 'decrease'
            const url = this.dataset.url;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const row = this.closest('tr');
                    const quantityCell = row.querySelector('.quantity-display');
                    const totalPriceCell = row.querySelector('.total-price-display');
                    
                    if (data.removed) {
                        // Товар удалён (количество стало 0)
                        row.remove();
                        showCartMessage('Товар удалён из корзины!');
                    } else {
                        // Обновляем количество и сумму
                        quantityCell.textContent = data.quantity;
                        totalPriceCell.textContent = data.total_price.toFixed(2) + ' ₽';
                    }
                    
                    // Обновляем общую сумму корзины
                    updateCartTotal();
                } else {
                    showCartMessage('Ошибка: ' + data.error, true);
                }
            })
            .catch(error => {
                showCartMessage('Ошибка при обновлении корзины', true);
            });
        });
    });
    
    // Функция для обновления общей суммы корзины
    function updateCartTotal() {
        const totalCells = document.querySelectorAll('.total-price-display');
        let total = 0;
        totalCells.forEach(cell => {
            const priceText = cell.textContent.replace(' ₽', '');
            total += parseFloat(priceText);
        });
        
        const cartTotalCell = document.querySelector('.cart-total');
        if (cartTotalCell) {
            cartTotalCell.textContent = total.toFixed(2) + ' ₽';
        }
    }
    
    // Функция для показа сообщений (если её нет в cart_remove.js)
    function showCartMessage(message, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'alert alert-' + (isError ? 'danger' : 'success') + ' alert-dismissible fade show';
        messageDiv.style.position = 'fixed';
        messageDiv.style.top = '20px';
        messageDiv.style.right = '20px';
        messageDiv.style.zIndex = '9999';
        messageDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(messageDiv);
        
        setTimeout(() => {
            messageDiv.remove();
        }, 3000);
    }
}); 