document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.add-to-cart-form').forEach(function(form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const url = form.action;
            const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
            .then(response => {
                if (response.ok) {
                    showCartMessage('Товар добавлен в корзину!');
                } else {
                    showCartMessage('Ошибка при добавлении в корзину', true);
                }
            })
            .catch(() => showCartMessage('Ошибка сети', true));
        });
    });

    function showCartMessage(msg, isError) {
        let el = document.getElementById('cart-message');
        if (!el) {
            el = document.createElement('div');
            el.id = 'cart-message';
            el.style.position = 'fixed';
            el.style.top = '20px';
            el.style.right = '20px';
            el.style.zIndex = 1000;
            el.style.padding = '12px 24px';
            el.style.borderRadius = '8px';
            el.style.fontWeight = 'bold';
            document.body.appendChild(el);
        }
        el.textContent = msg;
        el.style.background = isError ? '#dc3545' : '#28a745';
        el.style.color = '#fff';
        el.style.display = 'block';
        setTimeout(() => { el.style.display = 'none'; }, 2000);
    }
}); 