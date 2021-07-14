document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.entregado').addEventListener('click', desaparecer)
});


function desaparecer(){

    const tarjeta = document.querySelector('.tarjeta-wrapper'); 

    tarjeta.style.animationPlayState = 'running';
    tarjeta.addEventListener('animationend', () =>{
        tarjeta.remove()
    })
}