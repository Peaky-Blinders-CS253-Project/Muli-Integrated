document.addEventListener('DOMContentLoaded', () => {
    const cancelButton = document.getElementById('cancelButton');
    const bookButton = document.getElementById('bookButton');

    cancelButton.addEventListener('click', () => {
        const cancelDate = document.getElementById('cancelDate').value;
        const cancelTime = document.getElementById('cancelTime').value;
        // Cancel logic here. This can be an AJAX request or a form submission.
        alert('Cancellation for ' + cancelDate + ' at ' + cancelTime + ' has been processed.');
    });

    bookButton.addEventListener('click', () => {
        const extraDate = document.getElementById('extraDate').value;
        const extraTime = document.getElementById('extraTime').value;
        const extra = document.getElementById('extra').value;
        // Booking logic here. This can be an AJAX request or a form submission.
        alert('Extra booking for ' + extraDate + ' at ' + extraTime + ' for ' + extra + ' has been processed.');
    });
});
