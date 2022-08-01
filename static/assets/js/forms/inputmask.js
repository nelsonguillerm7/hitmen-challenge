
const init_inputmask = selector => {
    let elem = selector ? $(selector) : $(document)
    elem.find(".input-mask").inputmask();

    document.querySelectorAll(".btn-today").forEach(btn => {
        btn.addEventListener("click", event => {
            let date = new Date()
            let input = event.currentTarget.closest(".input-group").querySelector('.input-mask');
            let value = date.toLocaleDateString()
            let day = parseInt(value.split("/")[0])
            if (day < 10) {
                value = `0${value}`
            }
            input.value = value
        });
    });
}


document.addEventListener("DOMContentLoaded", () => {
    init_inputmask();
});