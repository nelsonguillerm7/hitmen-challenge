const initChangeState = () => {
    const changeStates = [...document.getElementsByClassName("change-state")]
    changeStates.map(changeState => {
        changeState.addEventListener("click", event => {
            event.preventDefault();
            fetch(changeState.dataset.url).then(response => {
                if (response.ok) return response.json()
            }).then(response => {
                if (response.hasOwnProperty("error")) {
                    throw new Error(response.error)
                }
                Swal.fire(
                    {
                        'icon': 'success',
                        'title': 'Success',
                        'text': response.message,
                    }
                ).then(_result => window.location.reload())
            }).catch(error => {
                Swal.fire(
                    {'icon': 'error', 'title': 'Transition', 'text': error}
                )
            })
        });
    })
}


document.addEventListener("DOMContentLoaded", () => {
    initChangeState();
});