(function () {
    document.addEventListener('click', function (e) {
        var target = e.target
        console.log(e)
        if (target.hasAttribute('data-toggle') && target.getAttribute('data-toggle') == 'modal') {
            if (target.hasAttribute('data-target')) {
                var m_ID = target.getAttribute('data-target');
                document.getElementById(m_ID).classList.add('open');
                e.preventDefault();
            }
        }

        if ((target.hasAttribute('data-dismiss') && target.getAttribute('data-dismiss') == 'modal') || target.classList.contains('modal')) {
            var modal = document.querySelector('[class="modal open"]');
            modal.classList.remove('open');
            e.preventDefault();
        }
    }, false);
})()

