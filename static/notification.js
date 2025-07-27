document.addEventListener("DOMContentLoaded", function () {
    setTimeout(() => {
        let notifications = document.querySelectorAll(".popup-container");
        notifications.forEach((notification) => {
            notification.style.opacity = "0";
            setTimeout(() => {
                notification.remove();
            }, 500);
        });
    }, 5000);
});

function closeNotification(element) {
    let notification = element.closest(".popup-container");
    if (notification) {
        notification.style.opacity = "0";
        setTimeout(() => {
            notification.remove();
        }, 500);
    }
}

function closePopup(element) {
    let popup = element.closest('.popup');
    if (popup) {
        popup.style.display = 'none'; 
    }
}