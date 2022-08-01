let init_paginator = function () {
    let url = new URL(window.location.href)
    let paginate = document.querySelector('#id_paginate_by');
    if (paginate) {
        let paginate_by = url.searchParams.get('paginate_by')
        paginate.value = paginate_by || '10';
        paginate.addEventListener('change', event => {
            paginate_by = event.currentTarget.value
            /*let search = url.searchParams.get('search');
            url.search = '';
            if (search) {
              url.searchParams.set('search', search);
            }*/
            url.searchParams.set('paginate_by', paginate_by);
            window.location.search = url.search
        });
    }

    let paginator = document.querySelector('#id_paginator');

    if (paginator) {
        paginator.querySelectorAll('a').forEach(pagination => {
            pagination.addEventListener("click", event => {
                let page = event.currentTarget.dataset.page;
                url.searchParams.set("page", page)
                event.target.href = url.search
            })
        })
    }
}

init_paginator()