
document.addEventListener('DOMContentLoaded', () => {
    console.log('loaded');

    /* After 3sec show the other part of the animation */
    setTimeout(() => {
        console.log('3s');
        /* hide the first part */
        document.querySelector('.part_1').style.display = 'none';

        /* Show the other part */
        document.querySelector('.part_2').style.display = 'flex';
    }, 2500);
});
