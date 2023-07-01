
/* Small screens */ 
document.addEventListener('DOMContentLoaded', () => {
    if (window.matchMedia("(max-width: 500px)").matches) {
        console.log('small screen');
        update();
    }
});

document.addEventListener('DOMContentLoaded', () => {
    window.addEventListener('resize', () => {
        /* Small screens */ 
        if (window.matchMedia("(max-width: 500px)").matches) {
            console.log('small screen');
            update();
        }

        /* Small screens */ 
        if (window.matchMedia("(min-width: 501px)").matches) {
            console.log('Large screen');

            document.querySelector('.part_2').style.height = '100vh';
            document.querySelector('.part_2').style.minHeight = '600px';

            /**/
            document.querySelector('.content_container').style.height = 'auto';

            document.querySelectorAll('.input_p_1').forEach((el) => {
                el.style.marginRight = '10px';
            });
        }

    });
});

/* Updates */
function update(){
    /* Expand the height of the screen */
    document.querySelector('.part_2').style.height = '105vh';
    document.querySelector('.part_2').style.minHeight = '850px';

    /**/
    document.querySelector('.content_container').style.height = '800px';

    document.querySelectorAll('.input_p_1').forEach((el) => {
        el.style.marginRight = '0';
    });
}
